import sys
sys.path.append('../..')
import util


def parse_input(input):
    input = input.strip().splitlines()
    instr = {}
    for i, line in enumerate(input):
        cmd, arg = line.split()
        arg = int(arg)
        instr[i] = (cmd, arg)
    return instr


def run(instr):
    pc = 0
    acc = 0
    visited = set()
    while True:
        visited.add(pc)
        cmd, arg = instr[pc]
        # print(pc, cmd, arg)

        if cmd == 'acc':
            acc += arg
        
        if cmd == 'jmp':
            pc += arg
        else:
            pc += 1

        if pc in visited:
            return (False, acc)
        if pc == len(instr.keys()):
            return (True, acc)


def part1(input):
    instr = parse_input(input)
    finished, acc = run(instr)
    return acc

def part2(input):
    instr = parse_input(input)
    for pc in instr.keys():
        cmd, arg = instr[pc]
        test_instr = instr.copy()
        if cmd == 'nop':
            test_instr[pc] = ('jmp', arg)
        elif cmd == 'jmp':
            test_instr[pc] = ('nop', arg)
        else:
            continue
        finished, acc = run(test_instr)
        if finished:
            return acc


def test():
    test_input = '''
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
'''
    assert(part1(test_input) == 5)
    assert(part2(test_input) == 8)


test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = part1(input)
    print('Part 1:', val)
    val = part2(input)
    print('Part 2:', val)
