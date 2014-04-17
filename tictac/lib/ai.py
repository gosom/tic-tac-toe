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

MOVE = None

def negamax(gs, depth, alpha, beta, p):
    global MOVE
    if depth == 0 or gs.game_over:
        score = p * evaluate(gs)
        if score == 0:
            return score
        score = (score - 0.01*depth*abs(score)/score)
        return score
    possible_moves = gs.get_available_moves()
    best_move = possible_moves[0]
    if depth == 9:
        MOVE = best_move
    best_score = -float('inf')
    for move in possible_moves:
        print move, 'eee'
        game = deepcopy(gs)
        game.do_move(move, p)
        move_alpha = - negamax(game, depth-1, -beta, -alpha, -p)
        best_score = max(best_score, move_alpha)
        if alpha < move_alpha:
            alpha = move_alpha
            best_move = move
            if depth == 9:
                MOVE = best_move
            if alpha >= beta:
                break
    print MOVE
    return best_score




