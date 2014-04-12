# -*- coding: utf-8 -*-
"""
Let two players play tic tac toe in the command line
Use option -h for help
"""
import logging
import sys

try:
    import PySide.QtGui as QtGui
except ImportError:
    sys.exit('pyside is required!')

from tictac.gui.app import TicTacToeApp

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    qt_app = QtGui.QApplication(sys.argv)
    app = TicTacToeApp()
    app.show()
    sys.exit(qt_app.exec_())
