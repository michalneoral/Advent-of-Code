import re

from aocd.models import Puzzle
import numpy as np


def navi(current_pos, step):
    x, y = current_pos
    r = {
        'R': [x + step[1], y],
        'L': [x - step[1], y],
        'D': [x, y + step[1]],
        'U': [x, y - step[1]]
    }
    new_step = r[step[0]]
    return new_step


def solver_a(data, b=False):
    lines = data.split('\n')
    digs = []

    # PARSING INPUTS
    if not b:
        for idx, line in enumerate(lines):
            s = line.split(' ')
            digs.append((s[0], int(s[1]), re.sub('[()#]', '', s[2])))
    else:
        dnav = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
        for idx, line in enumerate(lines):
            s = line.split(' ')
            color_string = re.sub('[()#]', '', s[2])
            hex_string = color_string[:-1]
            direction = color_string[-1]
            digs.append((dnav[direction], int(hex_string, 16)))

    current = [0, 0]
    steps = [np.array(current, int)]
    for d in digs:
        current = navi(current, d)
        steps.append(np.array(current, int))

    points = np.stack(steps, axis=0)

    # area of polygon
    area_tmp = np.sum((points[:-1,0] * points[1:,1])) - np.sum((points[1:,0] * points[:-1,1]))
    line_lenght = np.sum(np.abs(points[:-1,:] - points[1:,:])) / 2 + 1
    area = np.abs(area_tmp)/2 + line_lenght
    print(int(area))


if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=18)
    solver_a(puzzle.examples[0].input_data)
    solver_a(puzzle.input_data)
    solver_a(puzzle.examples[0].input_data, True)
    solver_a(puzzle.input_data, True)
