from aocd.models import Puzzle
import re
import numpy as np

class Game:
    def __init__(self, game_data, with_joker):
        self.n_jokers = 0
        self.game_bid = int(game_data.split(' ')[-1])
        self.keys = game_data.split(' ')[0]
        self.values = self.chars2vals(self.keys, with_joker=with_joker)
        self.power = self.compute_power(self.values, with_joker=with_joker)

    def __str__(self):
        return f'{self.power}: {self.values}'

    def __lt__(self, other):
        if self.power == other.power:
            for idx, v in enumerate(self.values):
                if v < other.values[idx]:
                    return True
                elif v > other.values[idx]:
                    return False
            return False
        return self.power < other.power

    def compute_power(self, values, with_joker=False):
        values_wout_joker = values
        joker_count = 0

        if with_joker:
            values_wout_joker = list(filter(lambda a: a != 1, values))
            joker_count = np.sum(np.array(values) == 1)
            self.n_jokers = joker_count
        if joker_count == 5:
            return 100

        vals, count = np.unique(np.array(values_wout_joker), return_counts=True)
        self.count = count
        count_max = np.max(count)
        if count_max + joker_count == 5:
            return 100 # FIVE OF KIND
        elif count_max + joker_count == 4:
            return 80 # FOUR OF KIND
        elif (count_max==2 and np.sum(count==2)==2) and joker_count==1:
            return 70 # FULL HOUSE
        elif 3 in count and 2 in count:
            return 70 # FULL HOUSE
        elif count_max + joker_count == 3:
            return 60 # THREE OF KIND
        elif count_max + joker_count == 2:
            if np.sum(count==2) == 2:
                return 50 # TWO PAIRS
            return 30 # PAIR
        else:
            return 20 # HIGH NUMBER

    def chars2vals(self, chars, with_joker=False):
        vals = []
        kd = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        if with_joker:
            kd['J'] = 1

        for cidx in range(len(chars)):
            if chars[cidx] in kd:
                vals.append(kd[chars[cidx]])
            else:
                vals.append(int(chars[cidx]))
        return vals

def string2numbers(data_list):
    numbers = []
    for d in data_list:
        df = re.sub("[^0-9]", ".", d)
        numbers.extend([int(n) for n in df.split('.') if len(n) > 0])
    return numbers

def solver_a(data, with_joker=False):
    data_split = data.split('\n')

    games = []
    for d in data_split:
        games.append(Game(d, with_joker=with_joker))
    games = sorted(games)

    sum = 0
    for idx, g in enumerate(games):
        sum += (idx+1) * g.game_bid
    print(sum)

if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=7)

    print(puzzle.examples[0].input_data)
    # solver_a(puzzle.examples[0].input_data)
    # solver_a(puzzle.input_data)
    # print(puzzle.input_data)
    # print("----------------")

    d="""J462A 3
JJJ77 1
JJ332 5
J3322 10
22222 1
AJAJ4 2
KKKJK 1
JJJJJ 1
K2K33 2
KKK33 1
A2A2A 1
222AA 1"""
    # solver_a(d, with_joker=True)
    # solver_a(puzzle.examples[0].input_data, with_joker=True)
    solver_a(puzzle.input_data, with_joker=True)