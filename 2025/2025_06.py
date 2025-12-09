from aocd.models import Puzzle
import numpy as np

def strange_calculatore2(data):
    d_list = np.array(data.split('\n'), dtype=str)
    nums_str = d_list.view('U1').reshape((d_list.size, -1)).T
    nums_str = np.concatenate([nums_str, np.array([[' '] for _ in range(nums_str.shape[1])]).T])
    total, op, nums = 0, None, []
    for n in nums_str:
        op = n[-1] if n[-1] != ' ' else op
        if all([' ' == c for c in n]):
            total += np.sum(nums) if op == '+' else np.prod(nums)
            nums = []
        else:
            c_num = int(''.join(n[:-1]))
            nums.append(c_num)
    return total

def strange_calculatore(data):
    d_list = [d.split(' ') for d in data.split('\n')]
    nums = np.array([[int(dd) for dd in d if len(dd) > 0] for d in d_list[:-1]])
    ops = [dd for dd in d_list[-1] if len(dd) > 0]
    total = 0
    for idx, op in enumerate(ops):
        total += np.sum(nums[:,idx]) if op == '+' else np.prod(nums[:,idx])
    return total

if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=6)
    # print(strange_calculatore2(puzzle.examples[0].input_data))
    print(strange_calculatore2(puzzle.input_data))
