# -*- coding: utf-8 -*-
import logging
import random
import sys

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
        """
        :gs : gameState object """
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
        return move


class RandomConnect4Player(BasePlayer):

    def get_move(self, gs):
        return random.choice(gs.get_available_moves())


class Connect4SmartPlayer(BasePlayer):

    def __init__(self, player, depth=4, use_pruning=True):
        BasePlayer.__init__(self, player)
        self.depth = depth
        self.use_pruning = use_pruning

    def get_move(self, gs):
        if np.absolute(gs.gameState).sum() == 0:
            return 3
        if self.use_pruning:
            inf = float('inf')
            args = (gs, self.player, 100, 100-self.depth, True, -inf, inf, False)
        else:
            args = (gs, self.player, 100, 100-self.depth, True, None, None, False)
        score, move = negamax(*args)
        return move

