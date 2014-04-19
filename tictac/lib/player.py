# -*- coding: utf-8 -*-
import logging

import numpy as np
from copy import deepcopy

from . import SYMBOLS
from .ai import negamax


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
        if np.absolute(gs.gameState).sum() == 0:
            return (0, 0)
        score, move = negamax(gs, self.player)
        print 'PLAYES %s' % str(move)
        return move






