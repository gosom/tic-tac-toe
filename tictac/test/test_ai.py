# -*- coding: utf-8 -*-

import numpy as np
from ..lib.ai import *
from ..lib import gamestate as gamestate


def test_negamax():
    gs = gamestate.GameState(gs=np.zeros((3,3), dtype=int),)

    gs.do_move((0, 0), 1)
    #gs.do_move((0, 2), 1)
    gs.do_move((2, 0), 1)

    gs.do_move((0, 1), -1)
    #gs.do_move((1, 2), -1)
    gs.do_move((2, 1), -1)

    best_score, best_move = negamax(gs, 1)

    assert best_score == 8
    assert best_move == (1, 0)









