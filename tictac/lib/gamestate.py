# -*- coding: utf-8 -*-
""" this code is based on
Prof. Dr. Christian Bauckhage (http://mmprec.iais.fraunhofer.de/bauckhage)
sample code
"""
from copy import copy, deepcopy

import numpy as np

from ..lib import SYMBOLS

class GameState(object):

    def __init__(self, gs):
        """
        :gs : numpy array
        """
        self.gameState = deepcopy(gs)

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k == 'gameState':
                result.gameState = np.copy(self.gameState)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    def __eq__(self, other):
        return (self.gameState == other.gameState).all()

    def __repr__(self):
        B = np.copy(self.gameState).astype(object)
        for n, p in SYMBOLS.iteritems():
            B[B==n] = p
        return repr(B)

    @property
    def winner(self):
        for p in SYMBOLS.iterkeys():
            if self.is_win(p):
                return p
        return None

    @property
    def game_over(self):
        return not self.move_still_possible()

    def is_win(self, p):
        if np.max((np.sum(self.gameState, axis=0)) * p) == 3:
            return True
        if np.max((np.sum(self.gameState, axis=1)) * p) == 3:
            return True
        if (np.sum(np.diag(self.gameState)) * p) == 3:
            return True
        if (np.sum(np.diag(np.rot90(self.gameState))) * p) == 3:
            return True
        return False

    def is_draw(self):
        if self.move_still_possible():
            return False
        return not any([self.is_win(p) for p in SYMBOLS.iterkeys()])

    def move_still_possible(self):
        return not (self.gameState[self.gameState==0].size == 0)

    def get_available_moves(self):
        xs, ys = np.where(self.gameState==0)
        return tuple(((i, j) for i,j in zip(xs, ys)))
        #return np.array(np.where(self.gameState==0)).T

    def get_random_move(self):
        xs, ys = np.where(self.gameState==0)
        i = np.random.permutation(np.arange(xs.size))[0]
        return xs[i], ys[i]

    def get_best_random_move(self, good_moves):
        xs, ys = np.where(self.gameState==0)
        for e in good_moves:
            for x, y in zip(xs, ys):
                i, j = int(x), int(y)
                if e[0] == (i, j):
                    return e[0]
        return (None, None)

    def do_move(self, move, player):
        """
        Modifies the gameState inplace !
        :move : tuple|list (x, y)
        :player : Player object
        """
        x, y = move
        self.gameState[x, y] = player

    def undo_move(self, move):
        x, y = move
        self.gameState[x, y] = 0



