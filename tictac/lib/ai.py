# -*- coding: utf-8 -*-
from copy import deepcopy
import random


def score(gs, pId, level):
    val = gs.evaluation()
    if val == 0:
        return 0
    return level if val == pId else -level


def negamax(gs, pId, level=9):
    if gs.game_over:
        return score(gs, pId, level), None
    max_score = -float('inf')
    best_move = None
    currentGS = deepcopy(gs)
    for move in gs.get_available_moves():
        #currentGS = deepcopy(gs)
        currentGS.do_move(move, pId)
        x, _ = negamax(currentGS, -pId, level-1)
        currentGS.undo_move(move)
        x = -x
        if x > max_score:
            max_score = x
            best_move = move
    return max_score, best_move
    

