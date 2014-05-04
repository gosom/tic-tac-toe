# -*- coding: utf-8 -*-
""" this code is based on
Prof. Dr. Christian Bauckhage (http://mmprec.iais.fraunhofer.de/bauckhage)
sample code
"""
from copy import copy, deepcopy
import itertools
import math
import operator

import numpy as np

from ..lib import SYMBOLS

class BaseGameState(object):

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
        raise NotImplementedError

    @property
    def game_over(self):
        raise NotImplementedError

    def evaluation(self):
        raise NotImplementedError

    def is_win(self, p):
        raise NotImplementedError

    def is_draw(self):
        raise NotImplementedError

    def move_still_possible(self):
        raise NotImplementedError

    def get_available_moves(self):
        raise NotImplementedError

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


class Connect4GameState(BaseGameState):

    def __init__(self, gs):
        """
        :gs : numpy array
        """
        BaseGameState.__init__(self, gs)

    @property
    def game_over(self):
        if self.winner in (1, -1):
            return True
        return not self.move_still_possible()

    @property
    def winner(self):
        for p in filter(lambda p: p != 0,SYMBOLS.iterkeys()):
            if self.is_win(p):
                return p
        return None

    def evaluation(self):
        """Returns 0 if we have a draw.
        If we have a winner returns the winner (1 | -1)
        else if there are still available moves returns 100"""
        if self.winner in (-1, 1):
            return self.winner
        if self.move_still_possible():
            return 100
        return 0

    def move_still_possible(self):
        """a move is still possible when there is at least one
        empty slot in each of the columns
        if there is no game then the sum of the absolute values
        of all elements should be  ndarray.size
        """
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
        """
        assert p != 0
        rows =  [self.gameState[i,:].tolist() for i in xrange(0, 6)]
        columns = [self.gameState[:,i].tolist() for i in xrange(0, 7)]
        diags = self.get_diagonals()
        if self.find_score4(rows+columns+diags, p):
            return True
        return False

    def find_score4(self, l, p):
        """Returns True if the l contains 4 in a row"""
        comp_operator = operator.ge if p == 1 else operator.le
        for r in l:
            for k, v in itertools.groupby(r):
                if comp_operator(sum(v), p *4):
                    return True
        return False

    def get_diagonals(self):
        """
        Returns a list of all* the diagonals of the array.
        * Actually we do not return the ones with len()<4 since
        there we cannot have a score4 there.

        Idea modified from here:
        http://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python

        we want lower-left-to-upper-right and upper-left-to-lower right
        diagonals.
        "::-1" returns the rows in reverse. ":" returns the columns as is,
        effectively vertically mirroring the original array so the wanted
        diagonals are# lower-right-to-uppper-left.
        ::-1 -> returns rows reversed.

        """
        # upper diagonals k > 0
        diags = [self.gameState[::-1,:].diagonal(i)
                for i in range(-6, 7)]
        diags.extend(self.gameState.diagonal(i) for i in range(6,-6,-1))
        return filter(lambda e: len(e) > 3, [d.tolist() for d in diags])



class TicTacGameState(BaseGameState):

    def __init__(self, gs):
        """
        :gs : numpy array
        """
        BaseGameState.__init__(self, gs)

    @property
    def winner(self):
        val = self.evaluation()
        assert val == 100
        return val

    @property
    def game_over(self):
        return self.evaluation() != 100

    def evaluation(self):
        for p in filter(lambda x: x != 0, SYMBOLS.iterkeys()):
            if self.is_win(p):
                return p
        if self.has_empty_slot():
            return 100
        return 0

    def is_win(self, p):
        assert p != 0
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
        val == self.evaluation()
        assert val != 100
        return val == 0

    def has_empty_slot(self):
        return not (self.gameState[self.gameState==0].size == 0)

    def move_still_possible(self):
        return self.has_empty_slot()

    def get_available_moves(self):
        xs, ys = np.where(self.gameState==0)
        return tuple(((i, j) for i,j in zip(xs, ys)))

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


