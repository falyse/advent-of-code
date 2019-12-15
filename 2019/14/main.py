import sys
sys.path.append('../intcode')
sys.path.append('..')
import util
import math

reacts = []

class Element():
    def __init__(self, name, quantity):
        self.name =name
        self.quantity = int(quantity)
    def __str__(self):
        return str(self.quantity) + ' ' + self.name

class Reaction():
    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output
    def __str__(self):
        return 'Reaction: ' + ' '.join([str(x) for x in self.inputs]) + ' -> ' + str(self.output)

def find_reaction_with_output(name):
    for r in reacts:
        if r.output.name == name:
            return r


def recurse_replace(nums, levels, level):
    print(nums)
    print('Replace level', level)
    new = []
    for k,v in nums:
        if levels[k] == level:
            r = find_reaction_with_output(k)
            for i in r.inputs:
                new.append((i.name, i.quantity*math.ceil(v/r.output.quantity)))
        else:
            new.append((k,v))
    final = {}

    for ele,cnt in new:
        if ele not in final:
            final[ele] = 0
        final[ele] += cnt
    print(' counts:', final)
    new = list(final.items())

    if len(final.keys()) > 1:
        new,final = recurse_replace(list(new), levels, level+1)

    return new, final


def parse_reactions(text):
    reacts = []
    fuel_reaction = None
    for line in text.strip().splitlines():
        inputs, output = line.strip().split(' => ')
        ri = []
        for i in inputs.split(', '):
            q, n = i.split(' ')
            ri.append(Element(n,q))
        q, n = output.split(' ')
        ro = Element(n,q)
        # eles[n] = 0
        reaction = Reaction(ri, ro)
        if n == 'FUEL':
            fuel_reaction = reaction
        reacts.append(reaction)
    print([str(x) for x in reacts])
    return reacts

def get_levels(reacts, levels=None, start='FUEL', depth=0):
    if levels is None:
        levels = {}
    if start not in levels:
        levels[start] = 0
    levels[start] = max(depth, levels[start])
    for r in reacts:
        if r.output.name == start:
            for i in r.inputs:
                get_levels(reacts, levels, i.name, depth+1)
    return levels



def part2(text):
    fuel = max_fuel_from_ore_value(text, 1000000000000)
    assert fuel == 2267486



def get_total_ore(text, fuel=1):
    global reacts
    reacts = parse_reactions(text)

    levels = get_levels(reacts)
    print('Levels', levels)

    # nums = [('FUEL', 2267000)]
    nums = [('FUEL', fuel)]
    nums, final = recurse_replace(list(nums), levels, levels['FUEL'])
    print(nums)
    print(final)

    total_ore = final['ORE']
    print('Total ORE:', total_ore)
    return total_ore

def max_fuel_from_ore_value(text, ore):
    for i in range(2267000, 2268000):
        total_ore = get_total_ore(text, i)
        ratio = (total_ore/ore)
        print (ratio)
        if ratio > 1:
            return i - 1



def test0():
    assert get_total_ore(r"""10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL""") == 31

def test1():
    print('\n' * 10)
    assert get_total_ore(r"""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""") == 165

def test2():
    assert get_total_ore(r"""
    157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
    """) == 13312

def test3():
    assert get_total_ore(r"""
   2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF 
    """) == 180697

def test():
    test0()
    test1()
    test2()
    test3()
    # exit(0)
test()


with open('input.txt', 'r') as f:
    input = f.read().strip()

    # Part 1
    total_ore = get_total_ore(input)
    assert total_ore == 1582325

    # Part 2
    part2(input)
