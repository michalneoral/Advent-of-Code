from aocd.models import Puzzle
import re


class Game:
    def __init__(self, game_data):
        self.game_id = int(game_data.split(':')[0].split(' ')[1])
        round_str = game_data.split(': ')[1].split('; ')

        self.max_cubes =  {'blue': 0, 'red': 0, 'green': 0}
        for r in round_str:
            cubes = {c.split(' ')[1]: int(c.split(' ')[0]) for c in r.split(', ')}
            for k,v in cubes.items():
                self.max_cubes[k] = max(self.max_cubes[k], v)

    def is_possible(self, rules):
        for k,v in rules.items():
            if self.max_cubes[k] > v:
                return 0
        return self.game_id

    def get_power_of_set(self):
        power = 1
        for k,v in self.max_cubes.items():
            power *= v
        return power

def solver_a(data, rules):
    data_split = data.split('\n')

    sum = 0
    for d in data_split:
        game = Game(d)
        sum += game.is_possible(rules)
    print(sum)


def solver_b(data):
    data_split = data.split('\n')

    sum = 0
    for d in data_split:
        game = Game(d)
        sum += game.get_power_of_set()
    print(sum)


def main():
    puzzle = Puzzle(year=2023, day=2)
    rules = {'blue': 14, 'red': 12, 'green': 13}

    solver_a(puzzle.examples[0].input_data, rules=rules)
    solver_a(puzzle.input_data, rules=rules)
    print("----------------")

    solver_b(puzzle.examples[0].input_data)
    solver_b(puzzle.input_data)

if __name__ == '__main__':
    main()