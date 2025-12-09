from aocd.models import Puzzle
import numpy as np
from rich import print
from collections import OrderedDict

def hashmap(chars):
    current_value = 0
    for c in list(chars):
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256
    return current_value

def solver_a(data):
    lines = data.split('\n')[0].split(',')

    sum = 0
    for l in lines:
        sum += hashmap(l)
    return sum

def solver_b(data):
    print(data)
    lines = data.split('\n')[0].split(',')
    boxes = [OrderedDict() for _ in range(256)]
    for l in lines:
        if l[-1] == '-':
            lens_name = l[:-1]
            cbox = hashmap(lens_name)
            if lens_name in boxes[cbox]:
                del boxes[cbox][lens_name]
        else:
            lens_name = l[:-2]
            cbox = hashmap(lens_name)
            boxes[cbox][lens_name] = int(l[-1])

    sum = 0
    for idx, b in enumerate(boxes):
        if len(b) > 0:
            sidx = 0
            for k, v in b.items():
                sidx += 1
                sum += (idx+1) * sidx * v
    print(sum)

if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=15)

    # solver_a("""HASH""")
    # print(puzzle.examples[0].input_data)
    # solver_a(puzzle.examples[0].input_data)
    # print(solver_a(puzzle.input_data))
    solver_b(puzzle.examples[0].input_data)
    solver_b(puzzle.input_data)