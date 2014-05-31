# -*- coding: utf-8 -*-
import logging
import time

import numpy as np

from .gamestate import TicTacGameState, Connect4GameState
from . import SYMBOLS


class TicTacGame(object):

    def __init__(self, player1, player2, connect4=False):
        """
        :p1 : Player object
        :p2 : Player object
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug('Starting new TicTacToe game!')
        self.players = (player1, player2)
        self.player1, self.player2 = player1, player2
        self.connect4 = connect4
        if not connect4:
            GameState = TicTacGameState
            rows, cols = 3, 3
        else:
            self.log.info('Using Connect4GameState')
            GameState = Connect4GameState
            rows, cols = 6, 7
        self.state = GameState(gs=np.zeros((rows, cols), dtype=int))
        self.winner = None
        self.stats = {'winner': None, 'x': [], 'o': [], 'moves_num': None}

    def start(self, draw_signal=None):

         # initialize player number, move counter
        idx = 0
        player = self.players[idx]
        mvcntr = 1

        already_updated = set()
        while self.state.evaluation() == 100:
            self.log.debug('%s moves', repr(player))
            move = player.get_move(self.state)
            self.state.do_move(move, player.player)

            self.stats[repr(player)].append(move) # log move
            self.log.debug('New State:\n%s', repr(self.state))

            if draw_signal:
                self.__draw_state(self.state.gameState, already_updated,
                                  draw_signal)
                time.sleep(1)

            if self.state.is_win(player.player):
                self.log.info('Player %s wins after %d moves',
                    repr(player), mvcntr)
                self.winner = player
                self.stats['moves_num'] = mvcntr
                self.stats['winner'] = repr(player)

            #swap players
            idx += 1
            idx = idx % len(self.players)
            player = self.players[idx]
            mvcntr += 1

        if not self.winner:
            self.log.info('Game ended in a draw')

    def __draw_state(self, S, already_updated, qsignal):
        it = np.nditer(S, flags=['multi_index'])
        btn_val = 3 if not self.connect4 else 6
        while not it.finished:
            value = int(it[0])
            if value != 0:
                x, y = it.multi_index
                button_id = x + y * btn_val
                if button_id not in already_updated:
                    already_updated.add(button_id)
                    qsignal.emit(button_id, SYMBOLS[value].upper())
                    break
            it.iternext()

    def __repr__(self):
        return repr(self.state)
