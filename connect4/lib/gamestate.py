# -*- coding: utf-8 -*-
from copy import copy, deepcopy

import numpy as np

from tictac.lib import SYMBOLS


class GameState(object):

    def __init__(self, gs):
        """ 6 x 7 """
        self.gameState = deepcopy(gs)

    @property
    def game_over(self):
        return not self.move_still_possible()

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


    def __repr__(self):
        B = np.copy(self.gameState).astype(object)
        for n, p in SYMBOLS.iteritems():
            B[B==n] = p
        return repr(B)

