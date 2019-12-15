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


def render(status_map, loc):
    smap = status_map.copy()
    smap[loc] = 'D'
    image = []
    x_vals, y_vals = zip(*smap.keys())
    for y in reversed(range(min(y_vals), max(y_vals)+1)):
        row = []
        for x in range(min(x_vals), max(x_vals)+1):
            value = smap.get((x, y))
            if value is None:
                char = ' '
            else:
                char = value
            row.append(char)
        image.append(''.join(row))
    text = '\n'.join(image)
    print(text)

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
        status = computer.outputs[0]

        # Calc next potential location
        deltas = moves[dir]
        move_loc = tuple(map(operator.add, loc, deltas))

        # Process status code
        if status == 0:
            status_map[move_loc] = '#'
        elif status == 1:
            status_map[loc] = '.'
            loc = move_loc
        elif status == 2:
            status_map[move_loc] = 'X'
            loc = move_loc
        else:
            print('Unknown status', status)
            exit(1)

        # print('  loc', loc, 'is', status)
        render(status_map, loc)

        # Determine next move command
        if status == 0:
            dir = turn(dir)
        if status == 2:
            print('Finished at step', num_moves)
            exit(0)

