#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
import threading
import time
import Queue

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

import numpy as np

from tic_tac_toe import *


class AIThread(QtCore.QThread):
    updateButton = QtCore.Signal(int, str)

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
                self.play_game()
            elif command == 'quit':
                break
            else:
                self.log.warning('Invalid command %s', command)

    def play_game(self):
        gameState = np.zeros((3,3), dtype=int)
        self.__reset_buttons()
        # initialize player number, move counter
        player = 1
        mvcntr = 1
        noWinnerYet = True
        already_updated = set()
        while move_still_possible(gameState) and noWinnerYet:
            # get player symbol
            name = symbols[player]
            self.log.info('%s moves', name)
            # let player move at random
            gameState = move_at_random(gameState, player)
            self.__draw_state(gameState, already_updated)
            if move_was_winning_move(gameState, player):
                self.log.info('player %s wins after %d moves', name,
                                                              mvcntr)
                noWinnerYet = False
            player *= -1
            mvcntr +=  1
            time.sleep(1)

    def __reset_buttons(self):
        [self.updateButton.emit(i, '') for i in xrange(9)]

    def __draw_state(self, S, already_updated):
        it = np.nditer(S, flags=['multi_index'])
        while not it.finished:
            value = int(it[0])
            if value != 0:
                x, y = it.multi_index
                button_id = x + y * 3
                if button_id not in already_updated:
                    already_updated.add(button_id)
                    self.updateButton.emit(button_id, symbols[value].upper())
                    break
            it.iternext()


class TicTacToeButton(QtGui.QPushButton):

    def __init__(self):
        QtGui.QPushButton.__init__(self)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                       QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)

        font = self.font()
        font.setPixelSize(50)
        self.setFont(font)

    def heightForWidth(self, width):
        return width

    def sizeHint(self):
        return QtCore.QSize(100, 100)

    def setText(self, text):
        palette = self.palette()
        if text == "X":
            palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.red)
            self.setStyleSheet("color: red;")
        elif text == "O":
            palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.blue)
            self.setStyleSheet("color: blue;")
        self.setPalette(palette)
        super(TicTacToeButton, self).setText(text)


class TicTacToeApp(QtGui.QMainWindow):
    ''' tic tac toe'''

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info('Starting %s', self.__class__.__name__)

        vbox = QtGui.QVBoxLayout()

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

        self.newGameAction = QtGui.QAction("New", self)
        self.newGameAction.setShortcut("Ctrl+N")
        self.newGameAction.triggered.connect(self.onNewGame)

        self.closeAction = QtGui.QAction("Close", self)
        self.closeAction.triggered.connect(self.onClose)

        menu = self.menuBar().addMenu("Game")
        menu.addAction(self.newGameAction)
        menu.addAction(self.closeAction)

        self.setWindowTitle('Tic tac toe')
        self.setCentralWidget(QtGui.QWidget())
        self.centralWidget().setLayout(vbox)

        self.command_q = Queue.Queue()
        self.ai_thread = AIThread(q=self.command_q)
        self.ai_thread.updateButton.connect(self.write_button)
        self.ai_thread.start()
        self.log.debug('Gui is ready')

    def onClose(self):
        self.command_q.put('quit')
        while self.ai_thread.isRunning():
            time.sleep(0.2)
        self.close()

    def write_button(self, btn_id, btn_value):
        self.buttons.button(int(btn_id)).setText(btn_value)

    def onNewGame(self):
        self.command_q.put('new')

    def run(self):
        self.show()
        qt_app.exec_()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    qt_app = QtGui.QApplication(sys.argv)
    app = TicTacToeApp()
    app.run()