# -*- coding: utf-8 -*-
import random
import numpy as np

from ..lib.gamestate import GameState


def test_moves():
    gs = GameState(gs=np.zeros((6, 7), dtype=int),)
    gs.gameState[5, 0] = -1
    gs.gameState[4, 0] = -1
    gs.gameState[4, 4] = -1
    assert gs.move_still_possible() == True
    assert gs.get_available_moves() == tuple(range(0, 7))
    assert gs.game_over == False

    gs2 = GameState(gs=np.ones((6, 7), dtype=int),)
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

