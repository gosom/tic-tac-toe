# -*- coding: utf-8 -*-

import numpy as np
from ..lib.ai import *
from ..lib import gamestate as gamestate


def test_negamax():
    gs = gamestate.Connect4GameState(gs=np.zeros((6, 7), dtype=int),)


    gs.do_move(0, 1)
    gs.do_move(1, -1)
    gs.do_move(1, 1)

    score, move = negamax(gs, -1, 100, 100-4, True)
    gs.do_move(move, -1)

    gs.do_move(2, 1)

    print gs.score_eval(-1, True)
    print gs

    print score
    



