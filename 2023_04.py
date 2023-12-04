from aocd.models import Puzzle
import re
import numpy as np

class Game:
    def __init__(self, game_data):
        self.game_id = int(game_data.split(':')[0].split(' ')[-1])
        winning_str = game_data.split(':')[1].split('|')[0]
        owned_str = game_data.split(':')[1].split('|')[1]
        self.winning_num = np.array([int(n) for n in winning_str.split(' ') if len(n) > 0])
        self.owned_num = np.array([int(n) for n in owned_str.split(' ') if len(n) > 0])

    def power_of_set(self):
        un = np.intersect1d(self.owned_num, self.winning_num, assume_unique=True)
        n = len(un) - 1
        if n < 0:
            return 0
        return 2**n

    def n_of_winning_numbers(self):
        un = np.intersect1d(self.owned_num, self.winning_num, assume_unique=False)
        return len(un)

def solver_a(data):
    data_split = data.split('\n')
    sum = 0
    for d in data_split:
        game = Game(d)
        sum += game.power_of_set()
    print(sum)

def solver_b(data):
    data_split = data.split('\n')
    counter = np.ones(len(data_split), dtype=int)
    for d in data_split:
        game = Game(d)
        nwc = game.n_of_winning_numbers()
        nmax = min(len(data_split), game.game_id + nwc)
        counter[game.game_id:nmax] += counter[game.game_id - 1]
    print(np.sum(counter))

if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=4)

    print(puzzle.examples[0].input_data)
    solver_a(puzzle.examples[0].input_data)
    solver_a(puzzle.input_data)
    print("----------------")
    solver_b(puzzle.examples[0].input_data)
    solver_b(puzzle.input_data)