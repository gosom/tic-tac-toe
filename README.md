tic-tac-toe
===========

### Introduction

Sample application for the course GameAI Uni Bonn 2014.

### Requirements

    python 2.7.x

    PySide >= 1.2.1
    matplotlib >= 1.3.1
    numpy >= 1.8.1

### How to run the app

    python run-app.py

    Use the --connect4 option to open a connect four board


If the application does not run please make sure:
    a. you installed python
    b. installed the correct python version
    c. you installed the above dependencies

If after installing all the above you still have a problem,
please open an issue with some information about your computer.
(OS version, kernel version, the versions of the above libraries)

The application is tested on Fedora Linux (3.13.6-100.fc19.i686)
with python version 2.7.5 and libraries as specified above.


### Credits

Parts of the code ( in tictac/lib/gamestate.py mainly) are taken from sample code
provided by [Prof. Dr. Christian Bauckhage](http://mmprec.iais.fraunhofer.de/bauckhage)

The TicTacToeButton in tictac/gui/widgets is based on a gist of
the user [https://github.com/niklasf]

About the negamax algorithm here: http://www.hamedahmadi.com/gametree/#negamax


### Contributors:

    Dimitris Nikolaou
    Helma Torkamaan
    Giorgos Komninos
    Alexandr Sapunji
