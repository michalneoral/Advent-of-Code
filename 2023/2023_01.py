from aocd.models import Puzzle
import re

# HACK: dirty, but it works, so what...
def reformat_str(d):
    d = re.sub('one', 'o1e', d)
    d = re.sub('two', 't2o', d)
    d = re.sub('three', 'th3ee', d)
    d = re.sub('four', 'fo4ur', d)
    d = re.sub('five', 'fi5ve', d)
    d = re.sub('six', 's6x', d)
    d = re.sub('seven', 'se7ven', d)
    d = re.sub('eight', 'eig8ht', d)
    d = re.sub('nine', 'ni9ne', d)
    return d

def solver(data, string_support=False):
    data_split = data.split('\n')

    if string_support:
        for i in range(len(data_split)):
            data_split[i] = reformat_str(data_split[i])

    sum = 0
    for d in data_split:
        v = re.sub("[^0-9]", "", d)
        sum += 10 * int(v[0]) + int(v[-1])
    print(sum)
    return sum


if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=1)

    solver(puzzle.examples[0].input_data)
    solver(puzzle.input_data)
    print("----------------")

    example2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

    solver(example2, string_support=True)
    solver(puzzle.input_data, string_support=True)