from aocd.models import Puzzle
import numpy as np
from rich import print
import re

all_stops = []

def rest_len(s):
    s = ''.join(s)
    sa = re.sub('[#]', '?', s)

    ss = sa.split('.')
    sc = [len(sx) for sx in ss if len(sx) > 0]
    return sum(sc) + len(sc) - 1

def may_be_valid(s, idx, values):
    s2 = s.copy()
    s2[:idx] = 'x'
    p = np.where(s2 == '.')[0][0]
    rl = rest_len(s)
    vl = sum(values) + len(values) - 1

    vc = [len(n) for n in ''.join(s[:p]).split('.') if len(n) > 0]
    aa = re.sub('[?]', '.', ''.join(s[:p]))
    vch = [len(n) for n in aa.split('.') if len(n) > 0]
    ab = re.sub('[?]', '', ''.join(s))
    va = [len(n) for n in ab.split('.') if len(n) > 0]

    if rl < vl:
        all_stops.append(0)
        return False

    max_vc_idx = len(vc) - 1

    if len(vc) > len(values):
        all_stops.append(1)
        return False

    if len(va) > len(values):
        # print(''.join(s))
        # print(va, len(va))
        # print(values, len(values))
        # print('-----')
        all_stops.append(2)
        return False

    if sum(vc) + len(vc) + rest_len(s[p:]) < sum(values) + len(values) - 1:
        all_stops.append(3)
        return False

    for i, vcc in enumerate(vc):
        if i == max_vc_idx:
            if values[i] > vcc:
                all_stops.append(4)
                return False
            if values[i] < vch[max_vc_idx]:
                all_stops.append(5)
                return False
        else:
            if values[i] != vcc:
                all_stops.append(6)
                return False

    return True

def solve_single_line(chars, values):
    # print(chars)
    # print(values)

    comb = [chars.copy()]

    # print('===========================================')
    # print(f'CHARS: {chars}')
    # print(f'VALS:  {values}')
    tc = 0
    for i in range(chars.shape[0]):
        # print('===========')
        if chars[i] == '?':
            comb_tmp = []
            for cc in comb:
                c1 = cc.copy()
                c2 = cc.copy()
                c1[i] = '.'
                c2[i] = '#'
                if may_be_valid(c1, i, values):
                    comb_tmp.append(c1)
                    tc += 1
                    # print(c1)
                if may_be_valid(c2, i, values):
                    comb_tmp.append(c2)
                    tc += 1
                    # print(c2)

            comb = comb_tmp
    # print('======')
    print(f'COMBS: {len(comb)}, TC {tc}')

    # valid = len(comb)
    valid = 0
    for cc in comb:
        cn = [len(n) for n in ''.join(cc).split('.') if len(n) > 0]
        if cn == values:
            valid += 1

    return valid, tc


def solver_a(data, expansion=None):
    lines = data.split('\n')
    map_l = []
    values = []
    for idx, line in enumerate(lines):
        # if idx == 0:
        #     continue

        lsp = line.split(' ')
        linew = lsp[0]
        vals = [int(n) for n in lsp[1].split(',')]
        if expansion is not None:
            linew = '?'.join([linew] * expansion)
            vals = vals * expansion
        linew = linew + '.'
        # print(linew)
        # print(vals)

        map_l.append(np.array(list(linew)))
        values.append(vals)

    sum = 0
    sumtc = 0
    print(f'total lines: {len(values)}')
    for idx, v in enumerate(values):
        c, tc = solve_single_line(map_l[idx], v)
        print(f'line: {idx}: {c}\n----------------')
        sum += c
        sumtc += tc

    print(sum, sumtc)
    print(np.unique(np.array(all_stops), return_counts=True))


class CombBank:
    def __init__(self):
        self.combs = {}


    def __call__(self, split):
        if str(split) not in self.combs:
            self.combs[str(split)] = self.create_combs(split)
        return self.combs[str(split)]

    def create_combs(self, split):
        start_char = 'S' if split.start_plus else '.'
        end_char = 'S' if split.end_plus else '.'
        combs = [start_char]
        for i in range(split.len):
            combs_tmp = []
            for c in combs:
                combs_tmp.append(c + '.')
                combs_tmp.append(c + '?')
            combs = combs_tmp
        combs = [c + end_char for c in combs]
        combs_splits = [create_splits(c) for c in combs]

        combs_counts = {}
        for c in combs_splits:
            key = tuple(c)
            if key not in combs_counts:
                combs_counts[key] = [1, c]
            else:
                combs_counts[key][0] += 1

        comb_list = []
        for k, v in combs_counts.items():
            comb_list.append(v)

        return comb_list



    # def __call__(self, split):
    #     self.combs[str(split)] = self.create_combs(split)
    #     split.set_comb(self.combs[str(split)])
    #     return self.combs[str(split)]
    #
    # def create_combs(self, split):
    #     if split.len in self.combs:
    #         return self.combs[split.len]
    #     combs = {}
    #
    #     for i in range(0,split.len):
    #         s = ''.join(['?']*split.len)
    #         start_char = 'S' if split.start_plus else '.'
    #         end_char = 'S' if split.end_plus else '.'
    #         s = start_char + s[:i] + '.' + s[i+1:] + end_char
    #         spl = create_splits(s)
    #         spl_t = tuple(spl)
    #
    #         if spl_t in combs:
    #             combs[spl_t] += 1
    #         else:
    #             combs[spl_t] = 1
    #         c_count = [ss.len for ss in spl]
    #
    #         sub_combs = []
    #         for spli in spl:
    #             sub_combs.append(self.__call__(spli))
    #
    #
    #     self.combs[str(split)] = combs
    #     return combs

class SplitHash:
    def __init__(self, lenght, start_plus=False, end_plus=False, stype='#'):
        self.len = lenght
        self.start_plus = start_plus
        self.end_plus = end_plus
        self.stype = stype
        self.combs = [[1, [self]]]

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def __str__(self):
        return f'{"+" if self.start_plus else "|"}{self.len}{self.stype}{"+" if self.end_plus else "|"}'

    def __repr__(self):
        return self.__str__()

    def set_comb(self, combs):
        self.combs = combs


class SplitQuest(SplitHash):
    def __init__(self, lenght, start_plus=False, end_plus=False):
        super().__init__(lenght=lenght, start_plus=start_plus, end_plus=end_plus, stype='?')

def create_splits(chars):
    # series_strings = [s for s in chars.split('.') if len(s) > 0]

    splits = []
    counter = 0
    start = False
    for i in range(len(chars) - 1):
        current_char = chars[i]
        next_char = chars[i + 1]

        if current_char == '#':
            if next_char == '#':
                counter += 1
            elif next_char == '?':
                splits.append(SplitHash(counter + 1, start_plus=start, end_plus=i))
                start = i + 1
                counter = 0
            else:
                splits.append(SplitHash(counter + 1, start_plus=start, end_plus=False))
                counter = 0
        elif current_char == '?':
            if next_char == '?':
                counter += 1
            elif next_char == 'S':
                splits.append(SplitQuest(counter + 1, start_plus=start, end_plus=i))
            elif next_char == '#':
                splits.append(SplitQuest(counter + 1, start_plus=start, end_plus=i))
                start = i + 1
                counter = 0
            else:
                splits.append(SplitQuest(counter + 1, start_plus=start, end_plus=False))
                counter = 0
        elif current_char == 'S':
            counter = 0
            start = i + 1
        else:
            # current_char == '.':
            counter = 0
            start = False
    return splits

def split_series(chars, comb_bank):
    splits = create_splits(chars)
    # print(splits)
    for s in splits:
        if s.stype == '?':
            s.set_comb(comb_bank(s))

    # print(chars)
    # print(splits)
    # print(s.combs for s in splits)
    return splits

def merge_combo(c1, c2, values):
    c1 = c1.copy()
    c2 = c2.copy()
    # print(f'{c1} + {c2}')
    c1_last = c1[-1] if len(c1) > 0 else None
    c2_first = c2[0] if len(c2) > 0 else None
    if c1_last is not None and c2_first is not None and c1_last.end_plus and c2_first.start_plus:
        if c1_last.stype == c2_first.stype:
            pass
        else:
            if c1_last.stype == '?':
                pass
            else:
                pass

            c1_last = c1.pop(-1)
            c2_first = c2.pop(0)
            c = SplitHash(c1_last.len + c2_first.len, start_plus=c1_last.start_plus, end_plus=c2_first.end_plus, stype=c2_first.stype)
            c1.append(c)
    c1.extend(c2)

    c_values = [cc.len for cc in c1 if cc.len > 0]

    if len(c_values) > len(values):
        return None
    if c_values[:-1] != values[0:len(c_values[:-1])]:
        return None
    if c_values[-1:] > values[len(c_values)-1:len(c_values)]:
        return None
    # print(c1)
    # print('----')
    return c1

def solve_single_line_b(chars, values, comb_bank):

    series = split_series(chars, comb_bank)

    combs = series[0].combs
    for idx, s in enumerate(series):
        if idx == 0:
            continue
        else:
            c_tmp = []
            for c in combs:
                c_mult = c[0]
                c_combo = c[1]
                for cs in s.combs:
                    cs_mult = cs[0]
                    cs_combo = cs[1]
                    merged_combo = merge_combo(c_combo, cs_combo, values)
                    if merged_combo is not None:
                        c_tmp.append([c_mult * cs_mult, merged_combo])
            combs = c_tmp
    # print(combs)

    suma = 0
    for c in combs:
        c_values = [cc.len for cc in c[1] if cc.len > 0]
        if values == c_values:
            suma += c[0]

    # print(suma)

    return suma


def solver_b(data, expansion=None):
    lines = data.split('\n')
    map_l = []
    values = []

    comb_bank = CombBank()

    for idx, line in enumerate(lines):
        lsp = line.split(' ')
        linew = lsp[0]
        vals = [int(n) for n in lsp[1].split(',')]
        if expansion is not None:
            linew = '?'.join([linew] * expansion)
            vals = vals * expansion
        linew = '.' + linew + '.'

        map_l.append(linew)
        values.append(vals)

    sum = 0
    print(f'total lines: {len(values)}')
    for idx, v in enumerate(values):
        c = solve_single_line_b(map_l[idx], v, comb_bank)
        print(f'line: {idx}: {c}\n----------------')
        sum += c
        # sumtc += tc
    #
    print(sum)
    # print(np.unique(np.array(all_stops), return_counts=True))



if __name__ == '__main__':
    puzzle = Puzzle(year=2023, day=12)

    d = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

    # d = """?###???????? 3,2,1"""
    # print(puzzle.examples[0].input_data)
    # solver_a(puzzle.examples[0].input_data)

    print(d)
    # solver_a(d) # 21 (last comb: 512)
    # solver_a(puzzle.input_data) # 7922
    # solver_a(d, expansion=3)
    # solver_a(puzzle.input_data, expansion=5)
    solver_b(d)
    # solver_b(d, expansion=5)
    # solver_b(puzzle.input_data)
    # solver_b(puzzle.input_data, expansion=5)