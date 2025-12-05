from aocd.models import Puzzle

def prepare_data(data_in):
    ranges_str, ids_str = data_in.split('\n\n')
    ranges  = [[int(cid) for cid in c_ranges.split('-')] for c_ranges in ranges_str.split('\n')]
    ids = [int(cid) for cid in ids_str.split('\n')]
    return ranges, ids

def first_brute_force(ranges, ids):
    total_valid = 0
    for cid in ids:
        for r in ranges:
            if r[0] <= cid <= r[1]:
                total_valid += 1
                break
    return total_valid

def merge_ranges(ranges, add_range):
    new_ranges = []
    old_ranges = []
    for r in ranges:
        if r[0] <= add_range[0] <= r[1]:
            new_ranges.append([r[0], max(r[1], add_range[1])])
        elif r[0] <= add_range[1] <= r[1]:
            new_ranges.append([min(r[0], add_range[0]), r[1]])
        elif add_range[0] <= r[1] <= add_range[1] <= add_range[1]:
            new_ranges.append(add_range)
        else:
            old_ranges.append(r)

    if len(new_ranges) == 0:
        old_ranges.append(add_range)
    elif len(new_ranges) == 1:
        old_ranges.append(new_ranges[0])
    else:
        old_ranges.extend(merge_ranges(new_ranges[1:], new_ranges[0]))
    return old_ranges

def second_brute_force(ranges):
    total_valid = 0
    new_ranges = []
    for idx, r in enumerate(ranges):
        new_ranges = merge_ranges(new_ranges, r)
    for r in new_ranges:
        total_valid += r[1] - r[0] + 1
    return total_valid

if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=5)
    # ranges, ids = prepare_data(puzzle.examples[0].input_data)
    ranges, ids = prepare_data(puzzle.input_data)
    print(second_brute_force(ranges))
