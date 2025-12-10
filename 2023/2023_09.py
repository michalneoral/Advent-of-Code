from aocd.models import Puzzle
import numpy as np

def recur(s):
    if np.sum(np.abs(s)) == 0:
        return 0
    diff = s[1:] - s[:-1]
    return recur(diff) + diff[-1]

def solver_a(data, reverse=False):
    data_split = data.split('\n')

    sum = 0
    for d in data_split:
        sequence = np.array([int(n) for n in d.split(' ')], dtype=int)
        if reverse: # magic
            sequence = sequence[::-1]
        sum += recur(sequence) + sequence[-1]
    print(sum)

if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=9)

    print(puzzle.examples[0].input_data)
    # solver_a(puzzle.examples[0].input_data)
    # solver_a(puzzle.input_data)
    solver_a(puzzle.examples[0].input_data, reverse=True)
    solver_a(puzzle.input_data, reverse=True)