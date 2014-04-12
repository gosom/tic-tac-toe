# -*- coding: utf-8 -*-
from ..lib import gamestate as gamestate
import numpy as np

def test_eq():
    gs = gamestate.GameState(gs=np.zeros((3,3), dtype=int), player=1)
    gs2 = gamestate.GameState(gs=np.ones((3, 3), dtype=int), player=-1)
    assert gs != gs2
    gs3 = gamestate.GameState(gs=np.zeros((3, 3), dtype=int), player=1)
    assert gs == gs3

def test_move_still_possible():
    gs = gamestate.GameState(gs=np.zeros((3,3), dtype=int), player=1)
    assert gs.move_still_possible() is True
    gs = gamestate.GameState(gs=np.ones((3, 3), dtype=int), player=-1)
    assert gs.move_still_possible() is False

