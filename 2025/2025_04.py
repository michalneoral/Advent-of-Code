from aocd.models import Puzzle
import numpy as np
from scipy.signal import convolve2d

def sum_of_neighbours(data, once=True): # once -> True first part, False second
    data = data.replace('.', '0').replace('@', '1').split('\n')
    mapa = np.array([[dd for dd in d] for d in data], int)
    total = 0
    while True:
        sum_removed, mapa = convolve(mapa)
        total += sum_removed
        if sum_removed == 0 or once: break
    print(total)
    return total

def convolve(mapa):
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    res = convolve2d(mapa, kernel)[1:-1, 1:-1] < 4
    res = res * mapa
    new_mapa = (1 - res) * mapa
    return np.sum(res), new_mapa

if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=4)
    sum_of_neighbours(puzzle.examples[0].input_data, once=False)
    sum_of_neighbours(puzzle.input_data, once=False)
