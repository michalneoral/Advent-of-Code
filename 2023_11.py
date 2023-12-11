from aocd.models import Puzzle
import numpy as np

def solver_a(data, expansion=1):
    lines = data.split('\n')
    map_l = []
    for idx, line in enumerate(lines):
        map_l.append(np.array(list(line)))
    mapa_tmp = np.stack(map_l, axis=0)
    mapa = np.zeros_like(mapa_tmp, dtype=int)
    mapa[mapa_tmp=='#'] = 1

    indexes = np.where(mapa)

    rows = sorted(np.unique(indexes[0]))
    collums = sorted(np.unique(indexes[1]))

    idx_y, idx_x = np.where(mapa)
    for i in reversed(range(mapa.shape[1])):
        if i not in collums:
            idx_x[i <= idx_x] += expansion

    for i in reversed(range(mapa.shape[0])):
        if i not in rows:
            idx_y[i <= idx_y] += expansion

    dist = np.abs(idx_x.reshape(1,-1) - idx_x.reshape(-1,1)) + np.abs(np.abs(idx_y.reshape(1,-1) - idx_y.reshape(-1,1)))
    sum = np.sum(dist)/2
    print(int(sum))

if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=11)
    solver_a(puzzle.examples[0].input_data, 999999)
    solver_a(puzzle.input_data, 999999)