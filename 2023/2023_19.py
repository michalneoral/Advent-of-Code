import copy
import re
from aocd.models import Puzzle


class SingleRule:
    def __init__(self, rule_string, last=False):
        self.rule_string = rule_string
        self.last = last
        semicol_split = rule_string.split(':')
        self.outkey = semicol_split[-1]
        if not last:
            self.comp_key = semicol_split[0][0]
            self.comp_symbol = semicol_split[0][1]
            self.comp_value = int(semicol_split[0][2:])

    def get_intersection(self, interval1, interval2):
        if interval1 is None or interval2 is None:
            return None
        new_min = max(interval1[0], interval2[0])
        new_max = min(interval1[1], interval2[1])
        return [new_min, new_max] if new_min <= new_max else None

    def __call__(self, part):
        if isinstance(part, PseudoPart):
            if self.last:
                return self.outkey, True, part, None
            else:
                p_value = part.get_key_value(self.comp_key)
                p1 = copy.deepcopy(part)
                p2 = copy.deepcopy(part)
                if self.comp_symbol == '<':
                    p1.change_value(self.comp_key, self.get_intersection(p_value, [1, self.comp_value - 1]))
                    p2.change_value(self.comp_key, self.get_intersection(p_value, [self.comp_value, 4000]))
                    return self.outkey, p1.is_valid(), p1, p2
                else:
                    p1.change_value(self.comp_key, self.get_intersection(p_value, [self.comp_value + 1, 4000]))
                    p2.change_value(self.comp_key, self.get_intersection(p_value, [1, self.comp_value]))
                    return self.outkey, p1.is_valid(), p1, p2
        else:
            if self.last:
                return self.outkey, True
            else:
                p_value = part.get_key_value(self.comp_key)
                if self.comp_symbol == '<':
                    return self.outkey, p_value < self.comp_value
                else:
                    return self.outkey, p_value > self.comp_value

    def __str__(self):
        if self.last:
            return f'{self.outkey}'
        else:
            return f'{self.comp_key} {self.comp_symbol} {self.comp_value} -> {self.outkey}'

    def __repr__(self):
        return f'| {self.__str__()} |'


class Rule:
    def __init__(self, key, rule_string):
        self.key = key
        self.rules = self.parse_rule_string(rule_string)

    def parse_rule_string(self, rule_string):
        rule_splits = rule_string.split(',')
        c_rules = []
        for idx in range(len(rule_splits)-1):
            c_rules.append(SingleRule(rule_splits[idx], last=False))
        c_rules.append(SingleRule(rule_splits[-1], last=True))

        return c_rules

    def __call__(self, part, old_key=None):
        if isinstance(part, PseudoPart):
            for r in self.rules:
                new_key, valid, part, part2 = r(part)
                if valid:
                    if part2 is not None:
                        part2.last_key = old_key
                    return new_key, part, part2
                else:
                    part = part2
            return None, None, None
        else:
            for r in self.rules:
                new_key, valid = r(part)
                if valid:
                    return new_key
            return self.rules[-1].outkey

    def __str__(self):
        return f'[{self.key.rjust(4)}]: {self.rules}'

    def __repr__(self):
        return '\n' + self.__str__()


class Part:
    def __init__(self, part_string):
        if part_string is not None:
            self.x = int(part_string[0][2:])
            self.m = int(part_string[1][2:])
            self.a = int(part_string[2][2:])
            self.s = int(part_string[3][2:])
            self.keys = {'x': self.x, 'm': self.m, 'a': self.a, 's': self.s}
            self.rating = self.x + self.m + self.a + self.s

    def get_key_value(self, key):
        return self.keys[key]

    def __str__(self):
        return f'x={self.x}, m={self.m}, a={self.a}, s={self.s} [{self.rating}]'

    def __repr__(self):
        return '{' + self.__str__() + '}'

    def get_rating(self):
        return self.rating


class PseudoPart(Part):
    def __init__(self):
        super().__init__(None)
        self.keys = {
            'x': [1, 4000],
            'm': [1, 4000],
            'a': [1, 4000],
            's': [1, 4000]
        }
        self.x = self.keys['x']
        self.m = self.keys['m']
        self.a = self.keys['a']
        self.s = self.keys['s']
        self.last_key = 'in'
        self.valid = True

    def is_valid(self):
        return self.valid

    def change_value(self, key, value):
        self.keys[key] = value
        self.x = self.keys['x']
        self.m = self.keys['m']
        self.a = self.keys['a']
        self.s = self.keys['s']
        if value is None:
            self.valid = False

    def __str__(self):
        return f'[{self.last_key.rjust(4)}]:  x={self.x}, m={self.m}, a={self.a}, s={self.s} [{self.get_rating()}]'

    def __repr__(self):
        return '\n{' + self.__str__() + '}'

    def get_rating(self):
        suma = 1
        for k, v in self.keys.items():
            n = v[1]-v[0]+1
            suma *= int(n)
        return suma

    def __eq__(self, other):
        return self.last_key == other.last_key and self.x == other.x and self.m == other.m and self.a == other.a and self.s == other.s


def solver_a(data, b=False):
    blocks = data.split('\n\n')

    rules_lines = blocks[0].split('\n')
    parts_lines = blocks[1].split('\n')

    rules = {}
    for rl in rules_lines:
        key, rule_string = rl.split('{')
        rule_string = rule_string[:-1]
        rules[key] = Rule(key, rule_string)

    parts = []
    R_list = []
    A_list = []
    if b is False:
        for pl in parts_lines:
            pl = re.sub('[{}]', '', pl)
            pl_splits = pl.split(',')
            parts.append(Part(pl_splits))

        for p in parts:
            c_key = 'in'
            while c_key not in ['A', 'R']:
                c_key = rules[c_key](p)
            if c_key == 'A':
                A_list.append(p)
            else:
                R_list.append(p)

    else:
        parts = [PseudoPart()]
        while len(parts) > 0:
            p = parts.pop(0)
            c_key = p.last_key
            while c_key not in ['A', 'R']:
                c_key, p, p2 = rules[c_key](p, c_key)
                if p2 is not None and p2 not in parts:
                    parts.append(p2)
            if c_key == 'A':
                A_list.append(p)
            else:
                R_list.append(p)

    suma = sum([p.get_rating() for p in A_list])
    print(suma)


if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=19)
    # print(puzzle.examples[0].input_data)
    solver_a(puzzle.examples[0].input_data)
    solver_a(puzzle.input_data)
    solver_a(puzzle.examples[0].input_data, True)
    solver_a(puzzle.input_data, True)
