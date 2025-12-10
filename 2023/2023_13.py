from aocd.models import Puzzle
import numpy as np
from rich import print


def edge_perfect_horizontal_reflection(mapa, diff):
    max_index = 0
    max_value = 0
    for i in range(1, mapa.shape[1] - 1):
        m1 = mapa[:, :i]
        m2 = mapa[:, i:][:, ::-1]
        comp_size = min(m1.shape[1], m2.shape[1])
        comp = np.sum(np.abs(m1[:, -comp_size:] - m2[:, -comp_size:]))
        if comp == diff and max_value < comp_size:
            max_value = comp_size
            max_index = i
    return max_index, max_value


def horizontal_reflection(mapa, diff):
    mi, mv = edge_perfect_horizontal_reflection(mapa, diff)
    mi2, mv2 = edge_perfect_horizontal_reflection(mapa[:,::-1], diff)
    if mv2 > mv:
        mi = mapa.shape[1] - mi2
    return mi


def solver_a(data, diff=0):
    blocks = data.split('\n\n')
    maps = []
    for b in blocks:
        bs = b.split('\n')
        lines = []
        for bc in bs:
            lines.append(np.array([int(c == '#') for c in list(bc)]))
        maps.append(np.stack(lines, axis=0))

    suma = 0
    for m in maps:
        hi = horizontal_reflection(m, diff)
        vi = horizontal_reflection(m.T, diff)
        if vi > hi:
            suma += 100 * vi
        else:
            suma += hi

    print(suma)


if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=13)
    solver_a(puzzle.examples[0].input_data, diff=1)
    solver_a(puzzle.input_data, diff=1)
