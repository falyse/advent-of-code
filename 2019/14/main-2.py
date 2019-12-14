import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util

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
def recurse(start, need=1):
    print('recurse', start)
    matches = []
    for r in reacts:
        if r.output.name == start:
            matches.append(r)
            print('  ', r)
    if len(matches) > 1:
        print('Need to handle multi')
    for m in matches:
        for i in m.inputs:
            if i.name not in amts:
                amts[i.name] = []
            print('     adding', i.quantity, i.name)
            amts[i.name].append(i.quantity)
            print(amts)
            recurse(i.name, i.quantity)

def run(text):
    for line in text.splitlines():
        inputs, output = line.strip().split(' => ')
        ri = []
        for i in inputs.split(', '):
            q, n = i.split(' ')
            ri.append(Element(n,q))
        q, n = output.split(' ')
        ro = Element(n,q)
        reacts.append(Reaction(ri, ro))
    print([str(x) for x in reacts])

    recurse('FUEL')
    print(amts)
    print(extras)



def test():
    run(r"""10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL""")
    exit(0)

    run(r"""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""")


test()

with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    input = f.readlines()
    # program_code = [int(x) for x in f.read().split(',')]
    # computer = IntcodeComputer(debug=False)
    # inputs = deque()
    # computer.run(program_code, inputs)
