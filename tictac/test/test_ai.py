# -*- coding: utf-8 -*-

import numpy as np
from ..lib.ai import *
from ..lib import gamestate as gamestate


numLeaves = 0;


def score(gs, level):
    return level * gs.evaluation()


def papari(gs, pId, level=9):
    global numLeaves

    if gs.game_over:
        numLeaves += 1
        return score(gs, level), None
    
    max_score = -float('inf')
    best_move = None

    for move in gs.get_available_moves():
        currentGS = deepcopy(gs)
        currentGS.do_move(move, pId)
        x, _ = papari(currentGS, -pId, level-1)
        #x = -x
        if x > max_score:
            max_score = x
            best_move = move
    return max_score, best_move


def test_minimax():
    gs = gamestate.GameState(gs=np.zeros((3,3), dtype=int),)

    gs.do_move((0, 0), 1)
    #gs.do_move((0, 2), 1)
    gs.do_move((2, 0), 1)

    gs.do_move((0, 1), -1)
    #gs.do_move((1, 2), -1)
    gs.do_move((2, 1), -1)

    print gs

    print papari(gs, 1)

    print numLeaves








