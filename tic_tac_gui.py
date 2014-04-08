#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
import threading
import time
import Queue
try:
   import cPickle as pickle
except:
   import pickle

try:
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
except ImportError:
    sys.exit('pyside is required!')
try:
    import matplotlib
    matplotlib.use('Qt4Agg')
    matplotlib.rcParams['backend.qt4']='PySide'

    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.pylab import axes, pie
except ImportError:
    sys.exit('matplotlib is required!')

try:
    import numpy as np
except ImportError:
    sys.exit('numpy is required!')

from tic_tac_toe import *


class TournamentStats(object):

    def __init__(self, rounds,):
        self.log = logging.getLogger(self.__class__.__name__)
        self.number_of_rounds = rounds
        self.log.info('Starting Tournament with %d rounds', self.number_of_rounds)
        self.played_rounds = 0
        self.results = []
        self.winning_positions = {}
        for i in xrange(3):
            for j in xrange(3):
                self.winning_positions[(i,j)] = 0
        self.log.debug('TournamentStats initial winning:\n%s',
                       self.winning_positions)
        self.x_wins, self.o_wins, self.draws = 0, 0, 0

    @property
    def good_moves(self):
        total_winning_moves = float(sum([v for v in self.winning_positions.itervalues()]))
        if not total_winning_moves:
            return 0
        self.log.debug('sum winning moves %d', total_winning_moves)
        good_moves = [(pos, value/total_winning_moves) for pos, value
            in self.winning_positions.iteritems()]
        return sorted(good_moves, key=lambda e: e[1], reverse=True)

    @property
    def plot_data(self):
        return (self.x_wins, self.o_wins, self.draws), ('X', 'O', 'D')

    def add_round(self, round, stats):
        self.played_rounds += 1
        self.results.append(stats)
        winner = stats.get('winner')
        assert winner in ('x', 'o', None)
        if winner:
            moves = stats[winner][:]
            for m in moves:
                self.winning_positions[m] += 1
            if winner == 'x':
                self.x_wins += 1
            elif winner == 'o':
                self.o_wins += 1
        else:#Draw
            self.draws += 1

    def save_good_moves(self,):
        with open('good_moves.pickle', 'wb') as f:
            pickle.dump(self.good_moves, f)

    def __repr__(self):
        return "#Rounds: %d #x-wins: %d #o-wins: %d #draws: %d" % (
                                                self.played_rounds,
                                                self.x_wins,
                                                self.o_wins,
                                                self.draws)


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
                self.play_game()
            elif command == 'quit':
                break
            elif command == 'random_tournament':
                self.run_tournament(play_type=0)
            elif command == 'prob_tournament':
                self.run_tournament(play_type=1)
            elif command == 'heuristic_tournament':
                self.run_tournament(play_type=2)
            else:
                self.log.warning('Invalid command %s', command)

    def play_game(self, tournament=False, play_type=0):
        if play_type == 1:
            with open('good_moves.pickle', 'rb') as f:
                good_moves = pickle.load(f)

        gameState = np.zeros((3,3), dtype=int)
        self.__reset_buttons()
        # initialize player number, move counter
        player = 1
        mvcntr = 1
        noWinnerYet = True
        already_updated = set()
        stats = {'winner': None, 'x': [], 'o': [], 'moves_num': None}
        while move_still_possible(gameState) and noWinnerYet:
            # get player symbol
            name = symbols[player]
            self.log.info('%s moves', name)
            # let player move at random
            if play_type == 0 or player == -1:
                x, y = get_random_move(gameState, player)
            elif play_type == 1 and player == 1:
                x, y = get_best_random_move(gameState, player, good_moves)
            gameState = make_move(gameState, player, x, y)
            stats[name].append((x, y)) # log move
            #gameState = move_at_random(gameState, player)
            if not tournament:
                self.__draw_state(gameState, already_updated)
            if move_was_winning_move(gameState, player):
                self.log.info('player %s wins after %d moves', name,
                                                              mvcntr)
                noWinnerYet = False
                stats['winner'] = name
                stats['moves_num'] = mvcntr
            player *= -1
            mvcntr +=  1
            if not tournament:
                time.sleep(1)
        return stats

    def run_tournament(self, rounds=2000, play_type=0):
        """Parameters:
        :rounds : # of rounds
        :play_type : 0 for random, 1 for probability, 2 for heuristic
        """
        self.log.debug('Running tournament of type %d', play_type)
        update_every = rounds/100
        progress = 0
        round = 0
        tournament_stats = TournamentStats(rounds)
        while round < rounds:
            stats = self.play_game(tournament=True, play_type=play_type)
            tournament_stats.add_round(round, stats)
            round += 1
            if round % update_every == 0:
                progress += 1
                self.updateProgress.emit(progress)
        self.log.info('Tournament %s finished', repr(tournament_stats))
        self.log.debug('Toournament good moves:\n%s',tournament_stats.good_moves)
        if play_type == 0:
            self.log.info('Saving good moves')
            tournament_stats.save_good_moves()
        self.finishedTournament.emit(tournament_stats)

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


class MatplotlibWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        #create figure
        figwidth = 5.0    # inches
        figheight = 3.5   # inches

        self.figure = Figure(figsize=(figwidth, figheight))
        self.canvas = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.axis.clear()
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)

        savePlotBtn = QtGui.QPushButton("Save")
        self.layoutVertical.addWidget(savePlotBtn)
        savePlotBtn.clicked.connect(self.onSave)

    def add_data(self, values, labels):
        self.axis.clear()
        self.axis.pie(values, labels=labels, explode=None,
                        autopct='%1.1f%%', shadow=True, startangle=90)

    def onSave(self):
        file = QtGui.QFileDialog.getSaveFileName(self, 'Save file', '',)
        fname, _ = file
        self.figure.savefig(fname)


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
        self.newGameAction = QtGui.QAction('New', self)
        self.newGameAction.setShortcut('Ctrl+N')
        self.newGameAction.triggered.connect(self.onNewGame)

        self.newRandomTournamentAction = QtGui.QAction('Random Tournament',
                                                        self)
        self.newRandomTournamentAction.setShortcut('Ctrl+R')
        self.newRandomTournamentAction.triggered.connect(self.onRandomTournament)

        self.newProbTournamentAction = QtGui.QAction('Prob Tournament', self)
        self.newProbTournamentAction.setShortcut('Ctrl+P')
        self.newProbTournamentAction.triggered.connect(self.onProbTournament)

        self.closeAction = QtGui.QAction("Close", self)
        self.closeAction.triggered.connect(self.onClose)

        menu = self.menuBar().addMenu("Game")
        menu.addAction(self.newGameAction)
        menu.addAction(self.newRandomTournamentAction)
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

    def onRandomTournament(self,):
        self.progress.show()
        self.command_q.put('random_tournament')

    def onProbTournament(self,):
        self.progress.show()
        self.command_q.put('prob_tournament')

    def run(self):
        self.show()
        qt_app.exec_()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    qt_app = QtGui.QApplication(sys.argv)
    app = TicTacToeApp()
    app.run()