from aocd.models import Puzzle
import numpy as np
from scipy.spatial import distance_matrix
from scipy.sparse.csgraph import connected_components

def shortest_connections(data, max_connections): # BOTH PARTS HERE
    junctions = np.array([[int(dd) for dd in d.split(',')] for d in data.split('\n')])
    path_lengths = np.triu(distance_matrix(junctions, junctions))
    max_len = np.max(path_lengths) + 1
    path_lengths[path_lengths == 0] = max_len
    h, w = path_lengths.shape
    n_connections = 0
    gr = np.zeros_like(path_lengths, dtype=int)
    while True:
        min_con = np.argmin(path_lengths)
        jA, jB = min_con // h, min_con % h
        cc_num, cc = connected_components(gr, directed=False)
        if cc_num == 2: # <- only for second part
            con_path_lengths = distance_matrix(junctions[cc==0], junctions[cc==1])
            con_path_lengths[con_path_lengths == 0] = max_len
            ex_min_con_path = np.argmin(con_path_lengths)
            jA, jB = ex_min_con_path // con_path_lengths.shape[0], ex_min_con_path % con_path_lengths.shape[0]
            return junctions[cc==0][jB][0] * junctions[cc==1][jA][0]

        if cc[jA] != cc[jB]:
            gr[jA, jB] = 1
        n_connections += 1
        path_lengths[jA, jB] = max_len
        if n_connections >= max_connections:
            break

    cc_num, cc = connected_components(gr, directed=False)
    unique, counts = np.unique(cc, return_counts=True, sorted=True)
    return np.prod(np.sort(counts)[-3:])

if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=8)
    print(shortest_connections(puzzle.input_data, 1000)) # FIRST PART
    print(shortest_connections(puzzle.input_data, 1000000)) # SECOND PART
