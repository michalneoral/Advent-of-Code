from aocd.models import Puzzle
import numpy as np
import itertools
import scipy

def lowest_press(lights, but_m): # FIRST PART ONLY
    for idx in range(len(lights)):
        for combo in itertools.combinations(but_m, idx+1):
            if all(np.sum(combo, axis=0) % 2 == lights):
                return idx+1

def lowest_press2(buttons, joltage): # SECOND PART ONLY
    constraints = scipy.optimize.LinearConstraint(buttons.T, joltage, joltage)
    integrality = np.ones((buttons.shape[0],), dtype=int)
    res = scipy.optimize.milp(c=integrality, constraints=constraints, integrality=integrality)
    return int(np.sum(res.x))

def buttons(data, var='A'): # BOTH PARTS HERE
    data = data.split('\n')
    total = 0
    for d_all in data:
        d = d_all.split(' ')
        lights = np.array([int(dd) for dd in d[0].replace('.', '0').replace('[','').replace('#','1').replace(']', '')])
        buttons = [np.array([int(ddd) for ddd in dd.replace('(', '').replace(')', '').split(',') ]) for dd in d[1:-1]]
        joltage = np.array([int(ddd) for ddd in d[-1].replace('{', '').replace('}', '').split(',') ])
        but_m = np.zeros([len(buttons), lights.size], dtype=int)
        for idx, b in enumerate(buttons):
            but_m[idx, b] = 1
        total += lowest_press(lights, but_m) if var=='A' else lowest_press2(but_m, joltage)
    return total

if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=10)
    print(buttons(puzzle.examples[0].input_data, var='B'))
    print(buttons(puzzle.input_data, 'B'))
