# -*- coding: utf-8 -*-
from copy import deepcopy
import random

def evaluate(state):
    """
    :state: GameState
    """
    if state.winner is None:
        return 0
    return 1

def negamax(gs, depth, alpha, beta, p):
    if depth == 0 or gs.game_over:
        return p * evaluate(gs)
    best_value = -float('inf')
    available_moves = gs.get_available_moves()
    if not available_moves:
        return p * evaluate(gs)
    for m in gs.get_available_moves():
        tmp_gs = deepcopy(gs)
        tmp_gs.do_move(m, p)
        val = - negamax(tmp_gs, depth-1, -beta, -alpha, -p)
        best_value = max(best_value, val)
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return best_value




