# -*- coding: utf-8 -*-
from copy import deepcopy
import random

def evaluate(state, p):
    """
    :state: GameState
    :p : player number
    """
    if state.winner is None:
        return 0
    return 1 if state.winner == p else -1

import sys
def negamax(gs, p, depth, max_depth):
    """
    :gs : GameStateObject
    :p : player number 1 or -1
    :depth : number of moves to look ahead
    """
    available_moves = gs.get_available_moves()
    if depth == max_depth or not available_moves:
        print available_moves
        score =  evaluate(gs, p)
        print '-------'
        print gs
        print score
        print '-------'
        return evaluate(gs, p)
    max_score, best_moves = -float('inf'), []

    #if len(available_moves) == 1:
    #    return evaluate(gs, p), available_moves[0]
    for move in available_moves:
        print 'doing move %s for %d' % (str(move), p)
        #tmp_gs = deepcopy(gs)
        gs.do_move(move, p)
        score = -negamax(gs, -1*p, depth+1, max_depth)
        gs.undo_move(move)
        #score = - score
        max_score = max(score, max_score)
        #if score > max_score:
        #    #if depth == 1:
        #    #    return score, pot_move
        #    max_score = score
        #    best_moves.append((score, pot_move))
        sys.exit()
    #to_return = random.choice(filter(lambda e: e[0] == max_score, best_moves))
    #print 'Returning ', repr(to_return)
    return max_score



