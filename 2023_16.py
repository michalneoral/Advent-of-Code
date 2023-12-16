from aocd.models import Puzzle
import numpy as np


class Direction:
    def __init__(self, direction, x, y):
        self.direction = direction
        self.x = x
        self.y = y


class Navigator:
    def __init__(self, mapa):
        self.mapa = mapa

    def __call__(self, cd):
        y = cd.y
        x = cd.x
        cd_direction = cd.direction
        symbol = self.mapa[y, x]
        change_of_direction = {
            ('right', '.'): ['right'],
            ('right', '-'): ['right'],
            ('right', '\\'): ['down'],
            ('right', '/'): ['up'],
            ('right', '|'): ['up', 'down'],

            ('left', '.'): ['left'],
            ('left', '-'): ['left'],
            ('left', '\\'): ['up'],
            ('left', '/'): ['down'],
            ('left', '|'): ['up', 'down'],

            ('up', '.'): ['up'],
            ('up', '-'): ['left', 'right'],
            ('up', '\\'): ['left'],
            ('up', '/'): ['right'],
            ('up', '|'): ['up'],

            ('down', '.'): ['down'],
            ('down', '-'): ['left', 'right'],
            ('down', '\\'): ['right'],
            ('down', '/'): ['left'],
            ('down', '|'): ['down'],
        }
        new_direction = {
            'right': Direction('right', x + 1, y),
            'left': Direction('left', x - 1, y),
            'up': Direction('up', x, y - 1),
            'down': Direction('down', x, y + 1)
        }

        if (cd_direction, symbol) not in change_of_direction:
            return []
        all_new_directions = change_of_direction[(cd_direction, symbol)]

        new_direction_list = []
        for nd in all_new_directions:
            new_direction_list.append(new_direction[nd])
        return new_direction_list


def solver_a(data, start_direction):
    lines = data.split('\n')
    mapa_list = [np.array(list(l)) for l in lines]
    mapa = np.stack(mapa_list, axis=0)
    mapa = np.pad(mapa, ((1, 1), (1, 1)), mode='constant', constant_values='X')
    navi = Navigator(mapa)

    energized_mapa = np.zeros_like(mapa, dtype=int)
    path = [[{} for __ in range(mapa.shape[1])] for _ in range(mapa.shape[0])]

    current_paths = [start_direction]
    while len(current_paths) > 0:
        cd = current_paths.pop(0)
        energized_mapa[cd.y, cd.x] = 1
        cp_list = navi(cd)
        for cd in cp_list:
            if cd.direction in path[cd.y][cd.x]:
                continue
            path[cd.y][cd.x][cd.direction] = True
            current_paths.append(cd)

    energized_mapa = energized_mapa[1:-1,1:-1]
    return np.sum(energized_mapa)


def solver_b(data):

    max_value = 0

    lines = data.split('\n')
    mapa_list = [np.array(list(l)) for l in lines]
    mapa = np.stack(mapa_list, axis=0)

    for i in range(mapa.shape[0]):
        c_value = max(solver_a(data, Direction('right', 1, i + 1)),
                      solver_a(data, Direction('left', mapa.shape[1], i + 1)))
        if c_value > max_value:
            max_value = c_value

    for i in range(mapa.shape[1]):
        c_value = max(solver_a(data, Direction('down', i+1, 1)),
                      solver_a(data, Direction('up', i+1, mapa.shape[0])))
        if c_value > max_value:
            max_value = c_value

    print(max_value)


if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=16)
    # print(solver_a(puzzle.examples[0].input_data, Direction('right', 1, 1)))
    # print(solver_a(puzzle.input_data, Direction('right', 1, 1))) # 6795
    solver_b(puzzle.examples[0].input_data)
    solver_b(puzzle.input_data)
