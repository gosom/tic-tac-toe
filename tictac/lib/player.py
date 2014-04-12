# -*- coding: utf-8 -*-
import logging

import numpy as np
from copy import deepcopy

from . import SYMBOLS


class BasePlayer(object):

    def __init__(self, player):
        self.log = logging.getLogger(self.__class__.__name__)
        self.player = player

    def get_move(self, gs):
        raise NotImplementedError

    def __repr__(self):
        return SYMBOLS[self.player]


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
        move = self.minimax(gs, self.player)
        return move

    def evaluate(self, state):
        if state.winner is None:
            return 0
        return 1 if state.winner == self.player else -1

    def minimax(self, gs, p):
        """from here:
        http://www.giocc.com/concise-implementation-of-minimax-through-higher-order-functions.html
        """
        moves = gs.get_available_moves()
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            clone = deepcopy(gs)
            clone.do_move(move, p)
            score = self.min_play(clone)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def min_play(self, gs):
        if gs.move_still_possible():
            return self.evaluate(gs)
        moves = gs.get_available_moves()
        best_score = float('inf')
        for move in moves:
            clone = deepcopy(gs)
            score = self.max_play(clone)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    def max_play(self, gs):
        if gs.move_still_possible():
            return self.evaluate(gs)
        moves = gs.get_available_moves()
        best_score = float('-inf')
        for move in moves:
            clone = deepcopy(gs)
            score = self.min_play(clone)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score
