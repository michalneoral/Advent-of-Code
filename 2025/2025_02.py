import copy
import re
from aocd.models import Puzzle

class PrimesNumbers:
    def __init__(self):
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                        73, 79, 83, 89, 97]
        self.buffer = {}

    def __call__(self, number):
        if number not in self.buffer:
            primes = self._get_primes(number)
            div_numbers = set([p1 * p2 for p1 in primes for p2 in primes]).union(set(primes))
            self.buffer[number] = [dv for dv in list(div_numbers) if dv <= number]
        return self.buffer[number]

    def _get_primes(self, n):
        if n > 100:
            raise ValueError('n must be less than 100')
        if n < 2:
            return []
        return [p for p in self.primes if n >= p and n % p == 0]

class InvalidID:
    def __init__(self, data, part='A'):
        self.data = data.split(',')
        self.sum_invalid = 0
        self.Primes = PrimesNumbers()
        if part == 'A':
            for d in self.data:
                self.add_invalid_from_range(d)
        elif part == 'B':
            for d in self.data:
                self.add_invalid_from_range_at_least(d)
        print(self.sum_invalid)

    def add_invalid_from_range_at_least(self, data_range):
        r = data_range.split('-')
        for number in range(int(r[0]), int(r[1]) + 1):
            str_number = str(number)
            lsn = len(str_number)
            primes = self.Primes(lsn)
            if self.check_pattern(str_number, primes, lsn):
                self.sum_invalid += number

    def check_pattern(self, str_number, primes, lsn):
        for p in primes:
            parts = [str_number[i:i + lsn//p] for i in range(0, lsn, lsn//p)]
            if len(set(parts)) == 1:
                print(f'{str_number}: {p} x {parts[0]}')
                return True
        return False

    def add_invalid_from_range(self, data_range):
        r = data_range.split('-')
        for number in range(int(r[0]), int(r[1]) + 1):
            str_number = str(number)
            lsn = len(str_number)
            if lsn % 2 == 0:
                if str_number[:lsn//2] == str_number[lsn//2:]:
                    self.sum_invalid += number

if __name__ == '__main__':
    puzzle = Puzzle(year=2025, day=2)
    print(puzzle.examples[0].input_data)
    InvalidID(puzzle.examples[0].input_data, part='B')
    InvalidID(puzzle.input_data, part='B')


