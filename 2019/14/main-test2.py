import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util
import math

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

reacts = []
amts = {}

def find_reaction_with_output(name):
    for r in reacts:
        if r.output.name == name:
            return r

def recurse(reaction, need=1):
    eqn = '%0d*(' % need
    ratio = math.ceil(need / reaction.output.quantity)
    for i in reaction.inputs:
        if i.name not in amts:
            amts[i.name] = 0
        print('asdf0', i.name, i.quantity, need, reaction.output.quantity)
        # add = i.quantity
        add = i.quantity * ratio
        eqn += '%0d+' % i.quantity
        print('     adding', add, i.name)
        amts[i.name] += add
        print(amts)
        r = find_reaction_with_output(i.name)
        if r is not None:
            eqn += recurse(r, i.quantity * ratio)
            # recurse(r, i.quantity)
    eqn += ')'
    return eqn

def correct_ore():
    total = 0
    for r in reacts:
        if 'ORE' in [x.name for x in r.inputs]:
            new = math.ceil(amts[r.output.name] / r.output.quantity) * r.inputs[0].quantity
            print('asdf', r, new)
            total += new
    print('Total:', total)
    return total

def run(text):
    fuel_reaction = None
    for line in text.strip().splitlines():
        inputs, output = line.strip().split(' => ')
        ri = []
        for i in inputs.split(', '):
            q, n = i.split(' ')
            ri.append(Element(n,q))
        q, n = output.split(' ')
        ro = Element(n,q)
        reaction = Reaction(ri, ro)
        if n == 'FUEL':
            fuel_reaction = reaction
        reacts.append(reaction)
    print([str(x) for x in reacts])

    eqn = recurse(fuel_reaction)
    # print(eqn)

    # if not 'ORE' in extras:
    #     extras['ORE'] = 0
    # ore = amts['ORE'] + extras['ORE']
    # print('Total ORE:', ore)
    print('Total ORE:', amts['ORE'])
    ore = correct_ore()
    return ore


def test0():
    assert run(r"""10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL""") == 31
    exit(0)

def test1():
    print('\n' * 10)
    assert run(r"""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""") == 165
    exit(0)

def test2():
    assert run(r"""
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
    exit(0)

def test3():
    assert run(r"""
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
    exit(0)

test0()
# test1()
# test2()
# test3()

with open('input.txt', 'r') as f:
    # with open('test.txt', 'r') as f:
    input = f.read().strip()
    # program_code = [int(x) for x in f.read().split(',')]
    # computer = IntcodeComputer(debug=False)
    # inputs = deque()
    # computer.run(program_code, inputs)

    run(input)


# 1693718 too high