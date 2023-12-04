from aocd.models import Puzzle
import re
import numpy as np
from skimage.morphology import dilation

# I really tried to do it in the most effective way. Initially, I believed it could be achieved through morphological operations. However, I was mistaken.

def string2numbers(data_list):
    numbers = []
    for d in data_list:
        df = re.sub("[^0-9]", ".", d)
        numbers.extend([int(n) for n in df.split('.') if len(n) > 0])
    return numbers

def solver_a(data, return_numbers=False, search_symbol=False):
    data_split = data.split('\n')

    all_numbers = string2numbers(data_split)
    symbol_mask_list = []
    number_mask_list = []
    symbol_mask = []
    number_mask = []

    for d in data_split:
        df = re.sub("[0-9.]", "0", d)
        if search_symbol:
            df = re.sub("[^0-9.X]", "0", df)
            symbol_mask_list.append(re.sub("[X]", "1", df))
        else:
            symbol_mask_list.append(re.sub("[^0-9.]", "1", df))

        symbol_mask.append(np.array(list(symbol_mask_list[-1])).astype(int))

        df = re.sub("[0-9]", "1", d)
        number_mask_list.append(re.sub("[^1]", "0", df))
        number_mask.append(np.array(list(number_mask_list[-1])).astype(int))

    symbol_mask = np.array(symbol_mask)
    number_mask = np.array(number_mask)

    element = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]])

    mask_dil = dilation(symbol_mask, element)

    f = mask_dil[number_mask == 1]
    b = number_mask[number_mask == 1]
    b[f == 1] = 2
    number_mask[number_mask == 1] = b

    valid_numbers = []
    for nn in number_mask:
        cn = ''.join(list(nn.astype(str)))
        cn = re.sub("[0]", ".", cn)
        cn = re.sub("[1]", "0", cn)
        valid_numbers.extend([int(n) for n in cn.split('.') if len(n) > 0])

    valid_numbers = np.array(valid_numbers)
    all_numbers = np.array(all_numbers)

    if return_numbers:
        return all_numbers[valid_numbers > 0]
    print(np.sum(all_numbers[valid_numbers > 0]))


def findch(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def solver_b(data):
    data_split = data.split('\n')

    for idx, d in enumerate(data_split):
        data_split[idx] = re.sub("[^0-9.*]", ".", d)

    sum = 0
    data_len = len(data_split)
    for idx, d in enumerate(data_split):
        astposs = findch(d, '*')

        if len(astposs) == 0:
            continue

        for sp in astposs:
            dd = d[:sp] + 'X' + d[sp + 1:]

            str_list = []
            if idx != 0:
                str_list.append(data_split[idx-1])
            str_list.append(dd)
            if idx != data_len-1:
                str_list.append(data_split[idx+1])

            work_str = '\n'.join(str_list)
            list_val_numbers = solver_a(work_str, return_numbers=True, search_symbol=True)
            if len(list_val_numbers) == 2:
                sum += list_val_numbers[0] * list_val_numbers[1]
    print(sum)


def main():
    puzzle = Puzzle(year=2023, day=3)

    solver_a(puzzle.examples[0].input_data)
    solver_a(puzzle.input_data)
    print("----------------")

    solver_b(puzzle.examples[0].input_data)
    solver_b(puzzle.input_data)

if __name__ == '__main__':
    main()