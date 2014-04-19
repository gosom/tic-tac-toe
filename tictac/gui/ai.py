#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

try:
    import PySide.QtCore as QtCore
except ImportError:
    sys.exit('pyside is required!')

from ..lib.game import TicTacGame
from ..lib.player import RandomPlayer, ProbRandomPlayer, SmartPlayer
from ..lib.tournament import Tournament, TournamentStats
from ..lib import get_good_moves

class AIThread(QtCore.QThread):
    updateButton = QtCore.Signal(int, str)
    updateProgress = QtCore.Signal(int)
    finishedTournament = QtCore.Signal(TournamentStats)

    def __init__(self, q):
        QtCore.QThread.__init__(self)
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug('Starting %s', self.__class__.__name__)
        self.daemon = True
        self.q = q

    def run(self):
        while True:
            command = self.q.get(block=True)
            if command == 'new':
                self.play_game(play_type=0)
            elif command == 'smart':
                self.play_game(play_type=2)
            elif command == 'quit':
                break
            elif command == 'random_tournament':
                self.run_tournament(play_type=0)
            elif command == 'prob_tournament':
                self.run_tournament(play_type=1)
            elif command == 'smart_tournament':
                self.run_tournament(play_type=2)
            else:
                self.log.warning('Invalid command %s', command)

    def play_game(self, tournament=False, play_type=0):
        if play_type == 0:
            p1 = RandomPlayer(1)
        elif play_type == 1:
            p1 = ProbRandomPlayer(1, get_good_moves())
        elif play_type == 2:
            p1 = SmartPlayer(1)
        else:
            raise Exception('Invalid play_type')
        p2 = RandomPlayer(-1)
        thegame = TicTacGame(player1=p1, player2=p2)
        self.__reset_buttons()
        thegame.start(draw_signal=self.updateButton)

    def run_tournament(self, play_type):
        t = Tournament(play_type=play_type)
        t.start(qsignal=self.updateProgress)
        self.finishedTournament.emit(t.tournament_stats)

    def __reset_buttons(self):
        [self.updateButton.emit(i, '') for i in xrange(9)]



