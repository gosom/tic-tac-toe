# -*- coding: utf-8 -*-
import logging

import numpy as np
from copy import deepcopy

from . import SYMBOLS
#from .ai import negamax


class BasePlayer(object):

    def __init__(self, player):
        self.log = logging.getLogger(self.__class__.__name__)
        self.player = player

    def get_move(self, gs):
        raise NotImplementedError

    def __repr__(self):
        return SYMBOLS[self.player]

    @property
    def opponent(self):
        return -1*self.player


class RandomPlayer(BasePlayer):

    def get_move(self, gs):
        return gs.get_random_move()


class ProbRandomPlayer(BasePlayer):

    def __init__(self, player, good_moves):
        BasePlayer.__init__(self, player)
        self.good_moves = good_moves

    def get_move(self, gs):
        return gs.get_best_random_move(self.good_moves)


class SmartPlayer(BasePlayer):

    def get_move(self, gs):
        move = None
        def negamax(gs, p, depth, alpha=float('inf'), beta=-9999):
            global move
            if gs.game_over:
                return self.evaluate(gs, p)
            opponent = -p
            for m in gs.get_available_moves():
                tmp = deepcopy(gs)
                tmp.do_move(m, p)
                score = - negamax(tmp, opponent, depth+1, -beta, -alpha)
                print score
                if score > alpha:
                    print 'eee'
                    alpha = score
                    if depth == 1:
                        print 'edd'
                        move = m
                if alpha >= beta:
                    break
            return alpha
        negamax(gs, self.player, 0,)
        print move
        return move

    def evaluate(self, state, p):
        """
        :state: GameState
        """
        if state.winner is None:
            return 0
        return 1 if state.winner == p else -1



