# -*- coding: utf-8 -*-
import logging

import sys
import numpy as np
from ..lib.ai import *
from ..lib import gamestate as gamestate


def test_3ples():

    gs = gamestate.Connect4GameState(gs=np.zeros((6, 7), dtype=int),)

    gs.do_move(0, -1)
    gs.do_move(0, -1)
    gs.do_move(0, -1)

    gs.do_move(4, 1)
    gs.do_move(5, 1)
    gs.do_move(6, 1)

    gs.do_move(1, -1)

    print gs

    print gs.find_num_free_nples(1, 3)
    print gs.find_num_free_nples(-1, 3)

    print gs.find_num_free_nples(1, 2)
    print gs.find_num_free_nples(-1, 2)
    #print n