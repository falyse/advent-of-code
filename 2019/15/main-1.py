import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util
import operator


def turn(dir):
    dir += 2
    dir = dir % 4
    return dir


def test():
    pass


test()

with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)
    inputs = deque()
    computer.initialize(program_code, inputs)

    moves = {1: (0,1),
             2: (0,-1),
             3: (-1,0),
             4: (1,0)}

    status_map = {}
    num_moves = 0
    dir = 1
    loc = (0,0)
    while True:
        print('Move', num_moves, 'in dir', dir)
        num_moves += 1
        inputs.append(dir)
        computer.reset_outputs()
        done = computer.execute()
        outputs = computer.outputs
        print('outputs', outputs)

        # Process status code
        status = outputs[0]
        if status != 0:
            deltas = moves[dir]
            loc = tuple(map(operator.add, loc, deltas))

        status_map[loc] = status
        print('  loc', loc, 'is', status)

        # Determine next move command
        if status == 0:
            dir = turn(dir)
        if status == 2:
            print('Finished at step', num_moves)
            exit(0)

