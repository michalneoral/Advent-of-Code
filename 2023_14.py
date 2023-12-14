from aocd.models import Puzzle
import numpy as np
from rich import print

# TODO: optimize?
def move_platform(mlines):
    for _ in mlines:
        for idx in reversed(range(1, mlines.shape[0])):
            O_sutr = mlines[idx] == 1
            empty_space = mlines[idx-1] == 0
            move_sutr = np.logical_and(O_sutr, empty_space)
            mlines[idx][move_sutr] = 0
            mlines[idx-1][move_sutr] = 1
    return mlines


def cycle_platform(mlines):
    for i in range(4):
        mlines = move_platform(mlines)
        mlines = np.rot90(mlines, k=3)
    return mlines


def cycle_and_count(mlines, H):
    mlines = cycle_platform(mlines)
    suma = count_weight(mlines, H)
    return suma, mlines


def count_weight(mlines, H):
    suma = 0
    for idx, l in enumerate(mlines):
        suma += np.sum(l == 1) * (H - idx)
    return suma


def non_optimal_seq_len_counter(sequence):
    max_lenght = int(len(sequence) / 2)
    for i in range(2, max_lenght):
        if sequence[0:i] == sequence[i:2 * i]:
            return i
    return 1


def solver_a(data, task_a=True):
    lines = data.split('\n')

    trans = {'O': 1, '.': 0, '#': 2}
    mlines = []
    for l in lines:
        mlines.append(np.array([trans[c] for c in l], dtype=int))

    H = len(mlines)
    mlines = np.stack(mlines, axis=0)

    if task_a:
        mlines = move_platform(mlines)
        print(count_weight(mlines, H))
        return

    prev_c = []
    sum_c = []

    max_try = 300
    # TODO: HERE WE SHOULD HAVE TERMINATE CONDITION, BUT HAVE NO TIME TO FIND WHICH ONE
    for i in range(max_try):
        s, mlines = cycle_and_count(mlines, H)
        # print(i, s)
        prev_c.append(hash(str(mlines * s)))
        sum_c.append(s)

    max_c = 0
    max_i = 0
    for i in range(max_try):
        longest = non_optimal_seq_len_counter(prev_c[i:])
        if longest > max_c:
            max_c = longest
            max_i = i

    repeated_sequence = (1000000000 - max_i) % max_c + max_i - 1
    print(sum_c[repeated_sequence])


if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=14)

    # solver_a(puzzle.examples[0].input_data, False)
    solver_a(puzzle.input_data, False)
