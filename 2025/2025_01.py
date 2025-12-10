import copy
import re
from aocd.models import Puzzle


class Dial:
    def __init__(self, dial_number=50, method='A', debug=False, max_value=100):
        self.dial_number = dial_number
        self.zero_counter = 0
        self.max_value = max_value
        self.debug = debug
        self.method = method

    def turn_dial(self, comb):
        direction = -1 if comb[0] == 'L' else 1
        value = int(comb[1:])
        start_at_zero = self.dial_number == 0

        self.dial_number += direction * value
        rotations = abs(self.dial_number // self.max_value)
        if self.dial_number == 0 and direction == -1:
            rotations += 1
        if start_at_zero and direction == -1 and value < self.max_value:
            rotations -= 1

        self.dial_number %= self.max_value
        if self.method == 'A':
            if self.dial_number == 0:
                self.zero_counter += 1
        else:
            self.zero_counter += rotations

    def add_all_data(self, data):
        for d in data:
            self.turn_dial(d)

    def get_zero_counter(self):
        return self.zero_counter

if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=1)
    # print(puzzle.input_data)

    dial = Dial(debug=True, method='B')
    # dial.add_all_data(puzzle.examples[0].input_data.split('\n'))
    dial.add_all_data(puzzle.input_data.split('\n'))
    print(dial.get_zero_counter())
