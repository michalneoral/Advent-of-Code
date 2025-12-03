from aocd.models import Puzzle
import numpy as np

def find_biggest_voltage(banks, nums=2):
    banks_list = banks.split('\n')
    total = 0
    for bank_str in banks_list:
        bank = (np.array([b for b in bank_str], dtype=int))

        c_nums = nums
        for i in range(nums):
            c_nums -= 1
            c_bank = bank[:(len(bank)-c_nums)]
            idx = np.argmax(c_bank)
            value = c_bank[idx]
            bank[:(idx+1)] = 0
            total += (value * 10**c_nums)

    print(f"Biggest voltage: {total}")

if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=3)
    # find_biggest_voltage(puzzle.examples[0].input_data, nums=12)
    find_biggest_voltage(puzzle.input_data, 12)
