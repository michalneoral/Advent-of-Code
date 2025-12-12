from aocd.models import Puzzle

def merge_nodes(k, counter, skips, end):
    c_counter = counter[k]
    n_counter = {}
    skipped_list = [end]
    skipped_list.extend(skips)
    for c in c_counter.keys():
        if c in skipped_list:
            if c in n_counter:
                n_counter[c] += c_counter[c]
            else:
                n_counter[c] = c_counter[c]
        else:
            for cc in counter[c].keys():
                if cc in n_counter:
                    n_counter[cc] += c_counter[c] * counter[c][cc]
                else:
                    n_counter[cc] = c_counter[c] * counter[c][cc]
    counter[k] = n_counter
    return counter

def remove_unused(counter, start):
    used_keys = [start]
    for c in counter.keys():
        for cc in counter[c].keys():
            used_keys.append(cc)
    used_keys = list(set(used_keys))
    n_counter = {}
    for c in used_keys:
        if c in counter:
            n_counter[c] = counter[c]
    return n_counter

def reactor(data, var='A'):
    data = data.split('\n')
    nodes = {s.split(':')[0]: [ss for ss in s.split(':')[1].split(' ') if len(ss) > 0] for s in data}
    skips = ['fft', 'dac'] if var == 'B' else []
    start = 'svr' if var == 'B' else 'you'
    counter = {k:{c:1 for c in v} for k,v in nodes.items()}

    while True:
        for k in counter.keys():
            counter = merge_nodes(k, counter, skips, 'out')
        b_len = len(counter)
        counter = remove_unused(counter, start)
        if len(counter) == b_len:
            break

    if var == 'A':
        return counter[start]['out']
    return counter['svr']['fft'] * counter['fft']['dac'] * counter['dac']['out']


if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=11)
    # print(reactor(puzzle.examples[0].input_data, var='B'))
    print(reactor(puzzle.input_data, 'B'))
