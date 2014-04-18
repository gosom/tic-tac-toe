# -*- coding: utf-8 -*-
from copy import copy, deepcopy
import itertools
import math

import numpy as np

from tictac.lib import SYMBOLS


class GameState(object):

    def __init__(self, gs):
        """ 6 x 7 """
        self.gameState = deepcopy(gs)

    @property
    def game_over(self):
        return not self.move_still_possible()

    @property
    def winner(self):
        for p in filter(lambda p: p != 0,SYMBOLS.iterkeys()):
            if self.is_win(p):
                return p
        return None

    def move_still_possible(self):
        """a move is still possible when there is at least one
        empty slot in each of the columns
        if there is no game then the sum of the absolute values
        of all elements should be  ndarray.size
        """
        #print self.gameState.sum()
        return np.absolute(self.gameState).sum() < self.gameState.size

    def get_available_moves(self):
        """Here we want all the columns with sum (of the abs values) < 0
        """
        column_sum = np.absolute(self.gameState).sum(axis=0).T
        return tuple(i for i, v in enumerate(tuple(column_sum)) if v < 6 )

    def do_move(self, move, player):
        """
        Modifies the gameState inplace !
        :move : column
        :player : Player object

        The players is placed in the first emppty cell starting
        from (5, move) then (4, move) until one available
        """
        assert move in xrange(0, 7)
        assert move in self.get_available_moves()
        for row in xrange(5, -1, -1):
            if self.gameState[row, move] == 0:
                self.gameState[row, move] = player
                break

    def is_win(self, p):
        """Determine if the player has a 4 in a row in:
            - columns, rows, diagonals
            http://docs.scipy.org/doc/numpy/reference/generated/numpy.diag.html
        """
        assert p != 0
        # fist for rows:
        #rows_array = np.array_split(self.gameState, 6, axis=0)
        rows =  [self.gameState[i,:].tolist() for i in xrange(0, 6)]
        columns = [self.gameState[:,i].tolist() for i in xrange(0, 7)]
        diags = self.get_diagonals()
        if self.find_score4(rows+columns+diags, p):
            return True
        return False

    def find_score4(self, l, p):
        for r in l:
            for k, v in itertools.groupby(r):
                if sum(v) == p * 4:
                    return True
        return False

    def get_diagonals(self):
        """"""
        # upper diagonals k > 0
        diags = [self.gameState[::-1,:].diagonal(i)
                for i in range(-6, 7)]
        diags.extend(self.gameState.diagonal(i) for i in range(6,-6,-1))
        return list(d.tolist() for d in diags)

    def __repr__(self):
        B = np.copy(self.gameState).astype(object)
        for n, p in SYMBOLS.iteritems():
            B[B==n] = p
        return repr(B)

