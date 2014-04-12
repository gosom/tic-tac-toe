# -*- coding: utf-8 -*-
"""
Let two players play tic tac toe in the command line
Use option -h for help
"""
import logging
import argparse

from tictac.lib.game import TicTacGame
from tictac.lib.player import RandomPlayer, SmartPlayer

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', '--smart', action='store_true',
                        help='Use to allow player1 to play smart',
                        default=False)
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, help='Use to see more output')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    #logging.basicConfig(level=loglevel)
    p1 = SmartPlayer(1) if args.smart else RandomPlayer(1)
    thegame = TicTacGame(player1=p1, player2=RandomPlayer(-1))

    logging.debug('Initial state:\n%s', repr(thegame))
    thegame.start()
    print thegame.stats

