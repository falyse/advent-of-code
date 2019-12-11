import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util
from collections import deque
from itertools import permutations


def run_amps(code, sequence):
    num_amps = len(sequence)
    computers = [IntcodeComputer(debug=False) for _ in range(num_amps)]
    inputs = [deque([phase]) for phase in sequence]
    inputs[0].append(0)
    for i, c in enumerate(computers):
        c.initialize(code, inputs[i])

    all_done = False
    while not all_done:
        all_done = True
        for i, c in enumerate(computers):
            # print('  computer', i, 'started at', c.pc)
            done = c.execute()
            # print('  computer', i, 'paused at', c.pc, 'outputs', c.outputs)
            if not done:
                all_done = False
            next_i = i + 1
            if next_i >= num_amps:
                next_i = 0
            if len(c.outputs):
                inputs[next_i].extend(c.outputs)
                c.reset_outputs()
    return inputs[0][0]


def test():
    assert run_amps([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [9,8,7,6,5]) == 139629729
    assert run_amps([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], [9,7,8,5,6]) == 18216


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    # test()

    # Part 1
    perms = permutations(range(5))
    max = 0
    for p in perms:
        print(p)
        value = run_amps(program_code, list(p))
        if value > max:
            max = value
        print('  output', value, 'max', max)
    print('Max value:', max)
    assert max == 21760

    # Part 2
    perms = permutations(range(5,10))
    max = 0
    for p in perms:
        print(p)
        value = run_amps(program_code, list(p))
        if value > max:
            max = value
        print('  output', value, 'max', max)
    print('Max value:', max)
    assert max == 69816958
