# -*- coding: utf-8 -*-
try:
   import cPickle as pickle
except:
   import pickle


SYMBOLS = {1:'x', -1:'o', 0:' '}

F_GOOD_MOVES = 'good_moves.pickle'


def get_good_moves(fname=F_GOOD_MOVES):
    with open(fname, 'rb') as f:
        good_moves = pickle.load(f)
    return good_moves


def save_good_moves(good_moves, fname=F_GOOD_MOVES):
    with open(fname, 'wb') as f:
        pickle.dump(good_moves, f)