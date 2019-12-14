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
extras = {}

def find_reaction_with_output(name):
    for r in reacts:
        if r.output.name == name:
            return r

def recurse(reaction, need=1):
    print('recurse', reaction, 'need', need)
    ratio = math.ceil(need / reaction.output.quantity)
    extra_out = reaction.output.quantity * ratio - need
    if reaction.output.name not in extras:
        extras[reaction.output.name] = 0
    extras[reaction.output.name] += extra_out
    for i in reaction.inputs:
        extra = reaction.output.quantity - need
        # extra = need % reaction.output.quantity
        print('   extra', extra, reaction.output.quantity, i.name)
        if i.name not in amts:
            amts[i.name] = 0
        if i.name in extras and extras[i.name] + extra >= i.quantity:
            print('   used extra', i.quantity, i.name)
            extras[i.name] -= i.quantity
        else:
            print('asdf0', i.name, i.quantity, need, reaction.output.quantity)
            # add = i.quantity
            add = i.quantity * ratio
            print('     adding', add, i.name)
            amts[i.name] += add
        if extra > 0:
            if i.name not in extras:
                extras[i.name] = 0
            extras[i.name] += extra
        #     amts[i.name] -= extra
        print(amts)
        print(extras)
        r = find_reaction_with_output(i.name)
        if r is not None:
            recurse(r, i.quantity * ratio)

def run(text):
    fuel_reaction = None
    for line in text.splitlines():
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

    recurse(fuel_reaction)
    # print(amts)
    # print(extras)

    if not 'ORE' in extras:
        extras['ORE'] = 0
    ore = amts['ORE'] + extras['ORE']
    print('Total ORE:', ore)
    return ore


def test():
    assert run(r"""10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL""") == 31
    exit(0)

    assert run(r"""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""") == 165


test()

with open('input.txt', 'r') as f:
    # with open('test.txt', 'r') as f:
    input = f.readlines()
    # program_code = [int(x) for x in f.read().split(',')]
    # computer = IntcodeComputer(debug=False)
    # inputs = deque()
    # computer.run(program_code, inputs)
