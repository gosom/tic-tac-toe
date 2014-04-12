#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
import time
import Queue

try:
    import PySide.QtGui as QtGui
except ImportError:
    sys.exit('pyside is required!')

from .widgets import MatplotlibWidget, TicTacToeButton
from ..lib.tournament import TournamentStats
from .ai import AIThread


class TicTacToeApp(QtGui.QMainWindow):
    ''' tic tac toe'''

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info('Starting %s', self.__class__.__name__)

        vbox = QtGui.QVBoxLayout()
        # Progress dialog
        self.progress = QtGui.QProgressDialog("Starting Tournament",
                                              "Cancel", 0, 100, self)
        # tournament stats window
        self.init_stats_window()

        # we gonna use a grid 3 x 3
        grid = QtGui.QGridLayout()
        self.buttons = QtGui.QButtonGroup()
        self.buttons.setExclusive(False)
        for i in xrange(3):
            for j in xrange(3):
                button = TicTacToeButton()
                self.buttons.addButton(button, i + j * 3)
                grid.addWidget(button, i, j, 0)
        vbox.addLayout(grid)

        # menu actions
        self.newGameAction = QtGui.QAction('New Random Game', self)
        self.newGameAction.setShortcut('Ctrl+N')
        self.newGameAction.triggered.connect(self.onNewGame)

        self.newSmartGameAction = QtGui.QAction('New Smart Game', self)
        self.newSmartGameAction.setShortcut('Ctrl+H')
        self.newSmartGameAction.triggered.connect(self.onNewSmartGame)

        self.newRandomTournamentAction = QtGui.QAction('Random Tournament',
                                                        self)
        self.newRandomTournamentAction.setShortcut('Ctrl+R')
        self.newRandomTournamentAction.triggered.connect(self.onRandomTournament)

        self.newProbTournamentAction = QtGui.QAction('Prob Tournament', self)
        self.newProbTournamentAction.setShortcut('Ctrl+P')
        self.newProbTournamentAction.triggered.connect(self.onProbTournament)

        self.newSmartTournamentAction = QtGui.QAction('Heuristic Tournament', self)
        self.newSmartTournamentAction.setShortcut('Ctrl+P')
        self.newSmartTournamentAction.triggered.connect(self.onSmartTournament)

        self.closeAction = QtGui.QAction("Close", self)
        self.closeAction.triggered.connect(self.onClose)

        menu = self.menuBar().addMenu("Game")
        menu.addAction(self.newGameAction)
        menu.addAction(self.newSmartGameAction)
        menu.addAction(self.newRandomTournamentAction)
        menu.addAction(self.newSmartTournamentAction)
        menu.addAction(self.newProbTournamentAction)
        menu.addAction(self.closeAction)
        # end menu actions


        self.setWindowTitle('Tic tac toe')
        self.setCentralWidget(QtGui.QWidget())
        self.centralWidget().setLayout(vbox)

        # configure background thread
        self.command_q = Queue.Queue()
        self.ai_thread = AIThread(q=self.command_q)
        self.ai_thread.updateButton.connect(self.write_button)
        self.ai_thread.updateProgress.connect(self.update_progress)
        self.ai_thread.finishedTournament.connect(self.onTournamentFinish)
        self.ai_thread.start()
        # end

        self.log.debug('Gui is ready')

    def init_stats_window(self):
        self.stats_window = QtGui.QWidget()
        self.stats_window.resize(300, 400)
        self.stats_window.setWindowTitle('Tournament statistics')

    def onClose(self):
        self.command_q.put('quit')
        while self.ai_thread.isRunning():
            time.sleep(0.2)
        self.close()

    def write_button(self, btn_id, btn_value):
        self.buttons.button(int(btn_id)).setText(btn_value)

    def update_progress(self, value):
        self.progress.setValue(value)

    def onTournamentFinish(self, tournament):
        values, labels = tournament.plot_data
        matplotlibWidget = MatplotlibWidget(self.stats_window)
        matplotlibWidget.add_data(values, labels)
        self.stats_window.show()

    def onNewGame(self):
        self.command_q.put('new')

    def onNewSmartGame(self):
        self.command_q.put('smart')

    def onRandomTournament(self,):
        self.progress.show()
        self.command_q.put('random_tournament')

    def onProbTournament(self,):
        self.progress.show()
        self.command_q.put('prob_tournament')

    def onSmartTournament(self):
        self.progress.show()
        self.command_q.put('smart_tournament')
