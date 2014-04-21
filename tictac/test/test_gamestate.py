# -*- coding: utf-8 -*-
import random

import numpy as np

from ..lib.gamestate import Connect4GameState, TicTacGameState

def test_eq():
    gs = TicTacGameState(gs=np.zeros((3,3), dtype=int),)
    gs2 = TicTacGameState(gs=np.ones((3, 3), dtype=int),)
    assert gs != gs2
    gs3 = TicTacGameState(gs=np.zeros((3, 3), dtype=int))
    assert gs == gs3

def test_move_still_possible():
    gs = TicTacGameState(gs=np.zeros((3,3), dtype=int))
    assert gs.move_still_possible() is True
    gs = TicTacGameState(gs=np.ones((3, 3), dtype=int))
    assert gs.move_still_possible() is False

def testc4_moves():
    gs = Connect4GameState(gs=np.zeros((6, 7), dtype=int),)
    gs.gameState[5, 0] = -1
    gs.gameState[4, 0] = -1
    gs.gameState[4, 4] = -1
    assert gs.move_still_possible() == True
    assert gs.get_available_moves() == tuple(range(0, 7))
    assert gs.game_over == False

    gs2 = Connect4GameState(gs=np.ones((6, 7), dtype=int),)
    # put some random -1s
    for _ in xrange(21):
        x = random.randint(0, 5)
        y = random.randint(0, 6)
        gs2.gameState[x, y] = -1
    assert gs2.move_still_possible() == False
    assert not gs2.get_available_moves()

    gs2.gameState[0,0] = 0
    assert gs2.get_available_moves() == (0,)

    gs2.gameState[0,0] = 1

    assert gs2.game_over == True

    try:
        gs2.do_move(0, 1)
        assert 1 == -1
    except AssertionError:
        assert 1 == 1

    gs2.gameState[0,0] = 0
    gs2.do_move(0, 1)
    assert gs2.game_over == True

def test_winner():
    gs = Connect4GameState(gs=np.zeros((6, 7), dtype=int),)
    # setup playe1 moves
    gs.do_move(0, 1)
    gs.do_move(0, 1)
    gs.do_move(0, 1)
    gs.do_move(0, 1)
    gs.do_move(1, -1)
    assert gs.is_win(1) == True
    assert gs.is_win(-1) == False

    gs.do_move(2, -1)
    gs.do_move(3, -1)
    assert gs.is_win(-1) == False
    gs.do_move(6, -1)
    assert gs.is_win(-1) == False
    gs.do_move(4, -1)
    assert gs.is_win(-1) == True

    gs = Connect4GameState(gs=np.zeros((6, 7), dtype=int),)
    gs.do_move(2, -1)
    gs.do_move(3, 1)
    gs.do_move(3, -1)
    gs.do_move(4, 1)
    gs.do_move(4, -1)
    gs.do_move(4, -1)
    for _ in xrange(3):
        gs.do_move(5, 1)
    gs.do_move(4, 1)
    assert gs.is_win(-1) == False
    gs.do_move(5, -1) # now he should win
    assert gs.is_win(1) == False
    assert gs.is_win(-1) == True
    assert gs.winner == -1

def test_diagonals():
    gs = Connect4GameState(gs=np.zeros((6, 7), dtype=int),)
    gs.do_move(0, 1)
    gs.do_move(5, 1)
    gs.do_move(6, 1)
    assert len(gs.get_diagonals()) == 25

