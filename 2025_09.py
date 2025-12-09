from aocd.models import Puzzle
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import heapq
from matplotlib import pyplot as plt

def rectangle(data): # BOTH PARTS HERE
    positions = np.array([[int(dd) for dd in d.split(',')] for d in data.split('\n')])
    area = np.abs((1+np.abs(positions[:,0:1]-positions[:,0:1].T)) * (1+np.abs(positions[:,1:2]-positions[:,1:2].T)))
    print('first part area:', np.max(area))

    polygon = Polygon(positions.astype(float))
    index = 0

    area_sorted = []
    for r in range(area.shape[0]):
        for c in range(r+1, area.shape[1]):
            heapq.heappush(area_sorted, (-area[r, c], r, c))

    while True:
        area_max, idx1, idx2 = heapq.heappop(area_sorted)
        pos1 = positions[idx1,:].astype(float)
        pos2 = positions[idx2,:].astype(float)

        c_polygon = Polygon([pos1, [pos2[0], pos1[1]], pos2, [pos1[0], pos2[1]]])

        if polygon.buffer(0.5).contains(c_polygon):
            plt.plot(*polygon.exterior.xy, 'b')
            plt.plot(*c_polygon.exterior.xy, 'r')
            plt.title(f'{index:06}')
            plt.tight_layout()
            plt.savefig(f'outputs/{index:06}.png')
            plt.close()
            return np.abs(area_max)


if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=9)
    # print(rectangle(puzzle.examples[0].input_data))
    print(rectangle(puzzle.input_data))
