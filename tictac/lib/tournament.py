import logging
import time

from .game import TicTacGame
from .player import RandomPlayer, ProbRandomPlayer, SmartPlayer,\
                    RandomConnect4Player, Connect4SmartPlayer
from . import save_good_moves, get_good_moves

class Tournament(object):

    def __init__(self, rounds=100, play_type=0, connect4=False, depth=4):
        self.log = logging.getLogger(self.__class__.__name__)
        self.rounds = rounds
        self.play_type = play_type
        self.connect4 = connect4
        player_constructor = RandomPlayer if not self.connect4 else RandomConnect4Player
        if play_type == 0:
            p1 = player_constructor(1)
        elif play_type == 1:
            p1 = ProbRandomPlayer(1, get_good_moves())
        elif play_type == 2:
            p1 = SmartPlayer(1) if not self.connect4 else Connect4SmartPlayer(1, depth=depth)
        else:
            raise Exception('Invalid play_type')
        p2 = player_constructor(-1)
        self.players = (p1, p2)
        self.tournament_stats = TournamentStats(self.rounds, connect4)


    def start(self, qsignal=None):
        self.log.debug('Running tournament of type %d', self.play_type)
        update_every = max(1, self.rounds/100)
        progress = 0
        round_num = 0
        start_time = time.time()
        while round_num < self.rounds:
            game = TicTacGame(*self.players, connect4=self.connect4)
            game.start()
            self.tournament_stats.add_round(round_num, game.stats)
            round_num += 1
            if round_num % update_every == 0:
                progress += 1
                if qsignal:
                    qsignal.emit(progress)
        self.tournament_stats.duration = time.time() - start_time
        self.tournament_stats.avg_duration = self.tournament_stats.duration/self.rounds
        self.log.info('Tournament %s finished',
                        repr(self.tournament_stats))
        self.log.debug('Toournament good moves:\n%s',
                       self.tournament_stats.good_moves)
        if self.play_type == 0 and not self.connect4:
            self.log.info('Saving good moves')
            save_good_moves(self.tournament_stats.good_moves)


class TournamentStats(object):

    def __init__(self, rounds, connect4=False):
        self.log = logging.getLogger(self.__class__.__name__)
        self.number_of_rounds = rounds
        self.log.info('Starting Tournament with %d rounds', self.number_of_rounds)
        self.played_rounds = 0
        self.results = []
        self.winning_positions = {}
        if not connect4:
            for i in xrange(3):
                for j in xrange(3):
                    self.winning_positions[(i,j)] = 0
        else:
            self.winning_positions = {i:0 for i in xrange(7)}
        self.log.debug('TournamentStats initial winning:\n%s',
                       self.winning_positions)
        self.x_wins, self.o_wins, self.draws = 0, 0, 0

    @property
    def good_moves(self):
        total_winning_moves = float(sum([v for v in self.winning_positions.itervalues()]))
        if not total_winning_moves:
            return 0
        self.log.debug('sum winning moves %d', total_winning_moves)
        good_moves = [(pos, value/total_winning_moves) for pos, value
            in self.winning_positions.iteritems()]
        return sorted(good_moves, key=lambda e: e[1], reverse=True)

    @property
    def plot_data(self):
        return (self.x_wins, self.o_wins, self.draws), ('X', 'O', 'D')

    def add_round(self, round, stats):
        self.played_rounds += 1
        self.results.append(stats)
        winner = stats.get('winner')
        assert winner in ('x', 'o', None,)
        if winner:
            moves = stats[winner][:]
            for m in moves:
                self.winning_positions[m] += 1
            if winner == 'x':
                self.x_wins += 1
            elif winner == 'o':
                self.o_wins += 1
        else:#Draw
            self.draws += 1

    def __repr__(self):
        return "#Rounds: %d #x-wins: %d #o-wins: %d #draws: %d" % (
                                                self.played_rounds,
                                                self.x_wins,
                                                self.o_wins,
                                                self.draws)


