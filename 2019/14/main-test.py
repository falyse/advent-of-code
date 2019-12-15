import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util
import math

reacts = []
class Node:
    """Class to define a node in the orbit tree"""
    def __init__(self, name, depth):
        self.name = name
        self.parent = None
        self.depth = depth
        self.children = []

    def __str__(self):
        text = '%sNode %s\n' % (' '*self.depth, self.name)
        for child in self.children:
            text += str(child)
        return text

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def remove_child(self, node):
        node.parent = None
        self.children = self.children.remove(node)
        if self.children is None:
            self.children = []

    def get_total_depth(self):
        return self.depth + sum([x.get_total_depth() for x in self.children])

    def find_node(self, name):
        """Find descendant node with matching name"""
        if self.name == name:
            return self
        for child in self.children:
            node = child.find_node(name)
            if node:
                return node
        return None

    def flatten(self):
        all_nodes = []
        for child in self.children:
            all_nodes.extend(child.flatten())
        all_nodes.append(self)
        return all_nodes


def get_ancestors(node):
    """Return a list of all parent ancestors from the specified node to the tree root"""
    ancestors = []
    while True:
        parent = node.parent
        if parent is None:
            break
        else:
            ancestors.append(parent)
            node = parent
    return ancestors


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


def create_tree(reacts, start='FUEL', depth=0):
    """Construct a tree based on the connections defined in the orbits hash"""
    node = Node(start, depth)
    for r in reacts:
        if r.output.name == start:
            for i in r.inputs:
                child = create_tree(reacts, i.name, depth+1)
                node.add_child(child)
    return node

eles = {}


def recurse_replace(nums, level):
    print(nums)
    print('Replace level', level)
    new = []
    for k,v in nums:
        if eles[k] == level:
            r = find_reaction_with_output(k)
            for i in r.inputs:
                new.append((i.name, i.quantity*math.ceil(v/r.output.quantity)))
        else:
            new.append((k,v))
    final = {}
    if level > 1:
        for ele,cnt in new:
            if ele not in final:
                final[ele] = 0
            final[ele] += cnt
        print(' counts:', final)
        new = list(final.items())
        new,_ = recurse_replace(list(new), level-1)


    return new, final



def run(text):
    global reacts
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
        eles[n] = 0
        reaction = Reaction(ri, ro)
        if n == 'FUEL':
            fuel_reaction = reaction
        reacts.append(reaction)
    print([str(x) for x in reacts])

    tree = create_tree(reacts)
    print(tree)
    all_nodes = tree.flatten()
    # print(all_nodes)

    for node in all_nodes:
        if node.name == 'ORE':
            ancestors = get_ancestors(node)
            for i, parent in enumerate(ancestors):
                if i > eles[parent.name]:
                    eles[parent.name] = i

    print(eles)
    return get_total_ore(1)

def part2():
    fuel = max_fuel_from_ore_value(1000000000000)
    assert fuel == 2267486

def get_total_ore(fuel):
    # nums = [('FUEL', 2267000)]
    nums = [('FUEL', fuel)]
    nums, _ = recurse_replace(list(nums), eles['FUEL'])
    print(nums)

    final = {}
    for ele,cnt in nums:
        if ele not in final:
            final[ele] = 0
        final[ele] += cnt
    print(' counts:', final)
    new = list(final.items())

    total_ore = 0
    for r in reacts:
        if 'ORE' in [x.name for x in r.inputs]:
            # if r.output.name in final:
            cnt = math.ceil(final[r.output.name] / r.output.quantity) * r.inputs[0].quantity
            total_ore += cnt
            print('  Adding', cnt, 'ore from', r.output.name)
    print('Total ORE:', total_ore)
    return total_ore

def max_fuel_from_ore_value(num_ore):
    # nums = [('FUEL', 1)]
    # for i in range(2)
    for i in range(2267000, 2268000):
        total_ore = get_total_ore(i)
        ratio = (total_ore/1000000000000)
        print (ratio)
        if ratio > 1:
            return i - 1


def get_fuel(total_ore):
    guess = 1000000000000 / total_ore
    print(guess)



def test0():
    assert run(r"""10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL""") == 31

def test1():
    print('\n' * 10)
    assert run(r"""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""") == 165

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

def test():
    test0()
    test1()
    test2()
    test3()
    # exit(0)
test()

with open('input.txt', 'r') as f:
    # with open('test.txt', 'r') as f:
    input = f.read().strip()
    # program_code = [int(x) for x in f.read().split(',')]
    # computer = IntcodeComputer(debug=False)
    # inputs = deque()
    # computer.run(program_code, inputs)

    # Part 1
    total_ore = run(input)
    assert total_ore == 1582325

    # Part 2
    part2()


# 1693718 too high