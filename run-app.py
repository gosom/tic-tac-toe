#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Opens the tictac/connect4 window!
Use option -h for help
"""
import logging
import argparse
import sys

try:
    import PySide.QtGui as QtGui
except ImportError:
    sys.exit('pyside is required!')

from tictac.gui.app import TicTacToeApp

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--connect4', help='Use to open a connect4 board',
                        action='store_true', default=False)
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False)
    parser.add_argument('-n', '--nopruning', action='store_true', default=False)
    args = parser.parse_args()
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=loglevel)

    qt_app = QtGui.QApplication(sys.argv)

    app = TicTacToeApp(connect4=args.connect4, nopruning=args.nopruning)
    app.show()

    sys.exit(qt_app.exec_())
