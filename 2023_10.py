from aocd.models import Puzzle
import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import flood, flood_fill


def navigator(direction, y_pos, x_pos, lines):
    # -, 7, J
    c = lines[y_pos][x_pos]
    if direction == 'right':
        if c == '-':
            return 'right', y_pos, x_pos + 1
        elif c == '7':
            return 'down', y_pos + 1, x_pos
        elif c == 'J':
            return 'up', y_pos - 1, x_pos
    # -, F, L
    elif direction == 'left':
        if c == '-':
            return 'left', y_pos, x_pos -1
        elif c == 'F':
            return 'down', y_pos + 1, x_pos
        elif c == 'L':
            return 'up', y_pos - 1, x_pos
    # |, F, 7
    elif direction == 'up':
        if c == '|':
            return 'up', y_pos - 1, x_pos
        elif c == 'F':
            return 'right', y_pos, x_pos + 1
        elif c == '7':
            return 'left', y_pos, x_pos - 1
    # |, L, J
    else: # down
        if c == '|':
            return 'down', y_pos + 1, x_pos
        elif c == 'L':
            return 'right', y_pos, x_pos + 1
        elif c == 'J':
            return 'left', y_pos, x_pos - 1
    return None, None, None


def solver_a(data, reverse=False):
    lines = data.split('\n')
    x_pos, y_pos = None, None
    for idx, line in enumerate(lines):
        x_pos = line.find('S')
        if x_pos != -1:
            y_pos = idx
            break
    assert y_pos is not None
    assert x_pos is not None

    mapa = np.zeros([len(lines), len(lines[0])], dtype=int)
    mapa[y_pos, x_pos] = 1

    if y_pos != 0 and navigator('up', y_pos - 1, x_pos, lines)[0] is not None:
        direction = 'up'
        y_pos -= 1
    elif x_pos != len(lines[0])-1 and navigator('right', y_pos, x_pos+1, lines)[0] is not None:
        direction = 'right'
        x_pos += 1
    elif x_pos != 0 and navigator('left', y_pos, x_pos-1, lines)[0] is not None:
        direction = 'left'
        x_pos -= 1
    else:
        direction = 'down'
        y_pos += 1

    path_lenght = 1
    while True:
        mapa[y_pos, x_pos] = path_lenght + 1
        direction, y_pos, x_pos = navigator(direction, y_pos, x_pos, lines)
        if lines[y_pos][x_pos] == 'S':
            break
        path_lenght += 1
    print(path_lenght//2 + path_lenght%2)

    return mapa

def solver_b(data):
    mapa = solver_a(data)
    mm = mapa.max() //2 + mapa.max()%2
    mapa[mapa != 0] = np.abs(mapa[mapa!=0] - mm) + 10

    kmap = mapa.copy()
    kmap[mapa!=0] += 10
    vmap = kmap[:,:-1] - kmap[:,1:]
    vmap = 1 * (np.logical_and(np.abs(vmap) <= 1, vmap != 0))

    map1 = (vmap * mapa[:,:-1] + vmap * mapa[:,1:]) / 2
    mapv = np.concatenate([np.stack([mapa[:,idx], map1[:, idx]], axis=1) for idx in range(map1.shape[1])], axis=1)
    mapv = np.concatenate([mapv, mapa[:,-1:]], axis=1)

    kmap = mapv.copy()
    kmap[kmap!=0] += 10
    hmap = kmap[:-1,:] - kmap[1:,:]
    hmap = 1 * (np.logical_and(np.abs(hmap) <= 1, hmap != 0))

    map2 = (hmap * mapv[:-1,:] + hmap * mapv[1:,:]) / 2
    maph = np.concatenate([np.stack([mapv[idx,:], map2[idx,:]], axis=0) for idx in range(map2.shape[0])], axis=0)
    maph = np.concatenate([maph, mapv[-1:,:]], axis=0)

    p = np.pad(1 * (maph > 0), ((1, 1), (1, 1)), mode='constant', constant_values=0)

    filled = flood_fill(p, (0, 0), 2, tolerance=0)

    filled = filled[:,1::2]
    filled = filled[1::2,:]

    plt.imshow(filled)
    plt.show()
    print(np.sum(filled==0))




if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=10)

    # _ = solver_a(puzzle.input_data)
    solver_b(puzzle.input_data)