import sys
sys.path.append('../..')
import util


def process(input):
    instr, locs = input.strip().split('\n\n')
    instr = instr.strip().replace('R', '1').replace('L', '0')
    instr = [int(x) for x in instr]
    print(instr)
    lines = locs.strip().splitlines()
    nodes = {}
    for line in lines:
        key, locs = line.split(' = (')
        locs = locs.replace(')', '').split(', ')
        nodes[key] = locs
    print(nodes)

    node = 'AAA'
    steps = 0
    while True:
        dir = instr[steps % len(instr)]
        print('Step %0d : node %s, dir %0d' % (steps, node, dir))
        steps += 1
        node = nodes[node][dir]
        if node == 'ZZZ':
            return steps


def test():
    test_input = '''
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

    '''
    assert(process(test_input) == 2)

    test_input = '''
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

    '''
    assert(process(test_input) == 6)
test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
