from aocd.models import Puzzle
import numpy as np

def beam_splitter(data): # BOTH PARTS HERE
    beams = np.array([[int(dd) for dd in d.replace('.', '0').replace('S','1').replace('^','0')] for d in data.split('\n')])
    splitters = np.array([[int(dd) for dd in d.replace('.', '0').replace('S','0').replace('^','1')] for d in data.split('\n')])
    total = 0
    for idx in range(1,len(beams)):
        active_sp = splitters[idx] * beams[idx-1]
        beams[idx] = beams[idx-1] - active_sp + np.array([0,*active_sp[:-1]]) + np.array([*active_sp[1:], 0])
        total += np.sum(active_sp > 0) # This is only for first part
    return total, np.sum(beams[-1])

if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=7)
    # print(beam_splitter(puzzle.examples[0].input_data))
    print(beam_splitter(puzzle.input_data))
