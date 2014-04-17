# -*- coding: utf-8 -*-

import numpy as np
from ..lib.ai import *
from ..lib import gamestate as gamestate


def test_negamax():
    global MOVE
    gs = gamestate.GameState(gs=np.zeros((3,3), dtype=int))
    available_moves = gs.get_available_moves()
    assert len(available_moves) == 9
    best_score = negamax(gs, 9, float('inf'), -float('inf'), 1)
    #assert best_score == 0
    print best_score
    print MOVE
    #assert best_move == (0,0)
    '''
    gs.do_move((0, 0), 1)
    gs.do_move((0, 1), -1)
    gs.do_move((2, 2), 1)
    gs.do_move((2, 1), -1)
    gs.do_move((0, 2), 1)
    best_score, best_move = negamax(gs, 9, float('inf'), -float('inf'), 1)
    print gs
    print best_move
    assert best_move == (2, 0)
    '''









