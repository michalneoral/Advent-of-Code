from aocd.models import Puzzle
import numpy as np
import heapq


class Node:
    def __init__(self, orientation, x, y, len_streight=0, val=0):
        self.orientation = orientation
        self.x = x
        self.y = y
        self.len_streight = len_streight
        self.val = val

    def __str__(self):
        return f'{self.orientation}: {self.x}, {self.y} ({self.val}, {self.len_streight})'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return f'{self.orientation}: {self.x} _ {self.y} _ {self.len_streight}'

    def __lt__(self, other):
        return (self.val - self.x - self.y) < (other.val - other.x - other.y)


def next_paths(node, mapa, second_scenario=False):
    mapa_shape = mapa.shape
    max_y = mapa_shape[0]
    max_x = mapa_shape[1]
    r = {
        'right': [Node('right', node.x + 1, node.y, node.len_streight+1),
                 Node('up', node.x, node.y - 1),
                 Node('down', node.x, node.y + 1)],
        'left': [Node('left', node.x - 1, node.y, node.len_streight+1),
                  Node('up', node.x, node.y - 1),
                  Node('down', node.x, node.y + 1)],
        'up': [Node('up', node.x, node.y - 1, node.len_streight+1),
                  Node('left', node.x - 1, node.y),
                  Node('right', node.x + 1, node.y)],
        'down': [Node('down', node.x, node.y + 1, node.len_streight + 1),
               Node('right', node.x + 1, node.y),
               Node('left', node.x - 1, node.y)],
    }
    r2 = {
        'right': [Node('right', node.x + 1, node.y, node.len_streight + 1)],
        'left': [Node('left', node.x - 1, node.y, node.len_streight + 1)],
        'up': [Node('up', node.x, node.y - 1, node.len_streight + 1)],
        'down': [Node('down', node.x, node.y + 1, node.len_streight + 1)],
    }

    if second_scenario and node.len_streight < 3:
        r = r2

    new_nodes = r[node.orientation]
    new_nodes = [n for n in new_nodes if 0 <= n.x < max_x]
    new_nodes = [n for n in new_nodes if 0 <= n.y < max_y]
    if second_scenario:
        new_nodes = [n for n in new_nodes if n.len_streight < 10]
    else:
        new_nodes = [n for n in new_nodes if n.len_streight < 3]
    for n in new_nodes:
        n.val = node.val + mapa[n.y, n.x]
    return new_nodes

def solver_a(data, second_scenario=False):
    lines = data.split('\n')
    mapa_list = [np.array([int(k) for k in list(l)], dtype=np.int64) for l in lines]
    mapa = np.stack(mapa_list, axis=0)

    path_nodes = [Node('right', 0, 0), Node('down', 0, 0)]
    heapq.heapify(path_nodes)
    visited = {}

    min_path_len = 100000000000
    idx = 0
    while len(path_nodes) > 0:
        idx += 1
        c_node = heapq.heappop(path_nodes)
        # if idx % 1000 == 0:
        #     print(f'{idx:10d}: {c_node}')
        if c_node.__hash__() in visited:
            continue
        visited[c_node.__hash__()] = True
        next_nodes = next_paths(c_node, mapa, second_scenario)
        for n in next_nodes:
            if n.__hash__() in visited:
                continue

            if n.val > min_path_len:
                continue
            if n.x == mapa.shape[1] - 1 and n.y == mapa.shape[0] - 1:
                if min_path_len > n.val:
                    min_path_len = n.val
                    continue
                else:
                    continue
            heapq.heappush(path_nodes, n)

    print(f'max iter: {idx}')
    print(min_path_len)


if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=17)
    solver_a(puzzle.examples[0].input_data)
    solver_a(puzzle.input_data)
    solver_a(puzzle.examples[0].input_data, second_scenario=True)
    solver_a(puzzle.input_data, second_scenario=True)
