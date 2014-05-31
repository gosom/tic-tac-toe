# -*- coding: utf-8 -*-
import logging

import sys
import numpy as np
from ..lib.ai import *
from ..lib import gamestate as gamestate

logging.basicConfig(level=logging.DEBUG)

depth = 4

inf = float('inf')

def get_negamax_move(gs, p, debug=False):
    score, move = negamax(gs, p, level=100, min_level=100-depth, c4=True, alpha=-inf, beta=inf, debug=debug)
    print 'Player {} should do move {} with score {}'.format(p, move, score)
    return move, score


def evaluate_available_moves(gs, p):
    for m in gs.get_available_moves():
        gs.do_move(m, p)
        val = gs.score_eval(p)
        print 'Player {} evaluation for move {} = {}'.format(p, m, val)
        gs.undo_move(m)


def test_fill_winning():
    print 'Testing test_fill_winning'
    gs = gamestate.Connect4GameState(gs=np.zeros((6, 7), dtype=int),)
    
    gs.do_move(0, 1)
    gs.do_move(6, -1)
    gs.do_move(3, 1)
    gs.do_move(5, -1)
    gs.do_move(4, 1)
    gs.do_move(6, -1)
    gs.do_move(2, 1)
    gs.do_move(6, -1)

    '(1{2}0{2,})|(0{2,}1{2})|(1{1}0)'

    print gs
    
    assert gs.evaluation() == 100
    
    move, score = get_negamax_move(gs, 1) 

    assert move == 1


def test_block_winning_move():
    print 'Testing test_block_winning_move'
    
    gs = gamestate.Connect4GameState(gs=np.zeros((6, 7), dtype=int),)
    
    gs.do_move(0, 1)
    gs.do_move(6, -1)
    gs.do_move(3, 1)
    gs.do_move(5, -1)
    gs.do_move(4, 1)
    gs.do_move(6, -1)
    gs.do_move(2, 1)
    gs.do_move(6, -1)
    gs.do_move(6, 1)
    
    print gs
    assert gs.evaluation() == 100
    #evaluate_available_moves(gs, -1)
    #assert gs.score_eval(1) == 3
    
    move, score = get_negamax_move(gs, -1) 
    assert move == 1
    #assert move == 1 and score == 9900000
    
    gs = gamestate.Connect4GameState(gs=np.zeros((6, 7), dtype=int),)

    gs.do_move(6, 1)
    gs.do_move(0, -1)
    gs.do_move(4, 1)
    gs.do_move(0, -1)
    gs.do_move(5, 1)
    gs.do_move(0, -1)

    print gs
    move, score = get_negamax_move(gs, -1, debug=True)
    assert move == 0


def test_choose_winning_move():
    print 'testing test_choose_winning_move'
    gs = gamestate.Connect4GameState(gs=np.zeros((6, 7), dtype=int),)
    
    gs.do_move(0, 1)
    gs.do_move(6, -1)
    gs.do_move(3, 1)
    gs.do_move(5, -1)
    gs.do_move(4, 1)
    gs.do_move(6, -1)
    gs.do_move(2, 1)
    gs.do_move(6, -1)
    gs.do_move(6, 1)
    gs.do_move(1, -1)
    gs.do_move(3, 1)
    gs.do_move(5, -1)
    gs.do_move(3, 1)
    gs.do_move(5, -1)
    
    print gs
    move, score = get_negamax_move(gs, 1)
    #assert move == 3

    gs = gamestate.Connect4GameState(gs=np.zeros((6, 7), dtype=int),)

    gs.do_move(3, 1)
    gs.do_move(0, -1)
    gs.do_move(4, 1)
    gs.do_move(0, -1)
    gs.do_move(5, 1)
    gs.do_move(0, -1)

    print gs
    move, score = get_negamax_move(gs, 1)




