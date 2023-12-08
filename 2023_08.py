from aocd.models import Puzzle
import re
import numpy as np

def solver_a(data):
    data_split = data.split('\n')

    sequence = [0 if l=='L' else 1 for l in list(data_split[0])]
    seq_len = len(sequence)

    jumps = {}
    for idx, d in enumerate(data_split):
        if idx <= 1:
            continue
        V = [n for n in re.sub("[ =(,)]", " ", d).split(' ') if len(n) > 0]
        jumps[V[0]] = [V[1], V[2]]

    ckey = 'AAA'
    step_counter = 0
    while ckey != 'ZZZ':
        for s in sequence:
            ckey = jumps[ckey][s]
        step_counter += 1
    print(step_counter * seq_len)

def solver_b(data):
    data_split = data.split('\n')

    sequence = [0 if l=='L' else 1 for l in list(data_split[0])]
    seq_len = len(sequence)
    data_len = len(data_split) - 2

    jumps = {}
    for idx, d in enumerate(data_split):
        if idx <= 1:
            continue
        V = [n for n in re.sub("[ =(,)]", " ", d).split(' ') if len(n) > 0]
        jumps[V[0]] = [V[1], V[2]]

    # following code is artefact for "speedup", but in the end useless
    tr2num = {k: idx for idx,k in enumerate(jumps)}
    num2tr = {idx: k for idx,k in enumerate(jumps)}
    numjumps = np.zeros([data_len, 2], dtype=int)
    for i in range(data_len):
        key = num2tr[i]
        numjumps[tr2num[key],:] = np.array([tr2num[jumps[key][0]], tr2num[jumps[key][1]]], dtype=int)

    start_nodes = []
    for k, v in jumps.items():
        if k[2] == 'A':
            start_nodes.append(tr2num[k])
    start_nodes = np.array(start_nodes)

    end_nodes = np.zeros(data_len, dtype=bool)
    for idx, k in enumerate(jumps):
        if k[2] == 'Z':
            end_nodes[tr2num[k]] = True

    koefs = []
    for idx, sn in enumerate(start_nodes):
        if idx < 0:
            continue
        step_counter = 0
        cn = sn
        while True:
            s = sequence[step_counter % seq_len]
            step_counter += 1
            cn = numjumps[cn, s]
            if end_nodes[cn]:
                koefs.append(step_counter)
                break

    ck = 1
    for k in koefs:
        ck = np.lcm(ck,k)
    print(ck)

    # # general but newer ending solution
    # step_counter = 0
    # while True:
    #     s = sequence[step_counter % seq_len]
    #     step_counter += 1
    #     start_nodes = numjumps[start_nodes, s]
    #     if np.all(end_nodes[start_nodes]):
    #         break
    # print(step_counter)

def main():
    puzzle = Puzzle(year=2023, day=8)

    print(puzzle.examples[0].input_data)
    solver_a(puzzle.examples[0].input_data)
    solver_a(puzzle.input_data)

    d = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

    solver_b(d)
    solver_b(puzzle.input_data)

if __name__ == '__main__':
    main()