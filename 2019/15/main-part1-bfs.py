import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util
import operator
import random

random.seed(2)

def change_dir(status_map, loc):
    # If more than one is found, choose randomly
    empty_dirs = search_for_empty(status_map, loc)
    if len(empty_dirs) > 0:
        i = random.randint(0, len(empty_dirs)-1)
        return empty_dirs[i]
    exit_dirs = search_for_exit(status_map, loc)
    if len(exit_dirs) > 0:
        i = random.randint(0, len(exit_dirs)-1)
        return exit_dirs[i]


def search_for_empty(status_map, loc):
    empty = []
    if not status_map.get(get_next_loc(loc, 1)):
        empty.append(1)
    if not status_map.get(get_next_loc(loc, 2)):
        empty.append(2)
    if not status_map.get(get_next_loc(loc, 3)):
        empty.append(3)
    if not status_map.get(get_next_loc(loc, 4)):
        empty.append(4)
    return empty

def search_for_exit(status_map, loc):
    exits = []
    if status_map.get(get_next_loc(loc, 1)) == '.':
        exits.append(1)
    if status_map.get(get_next_loc(loc, 2)) == '.':
        exits.append(2)
    if status_map.get(get_next_loc(loc, 3)) == '.':
        exits.append(3)
    if status_map.get(get_next_loc(loc, 4)) == '.':
        exits.append(4)
    return exits


def render(status_map, loc):
    smap = status_map.copy()
    smap[loc] = 'D'
    smap[(0,0)] = 'S'
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


def get_next_loc(loc, dir):
    moves = {1: (0,1),
             2: (0,-1),
             3: (-1,0),
             4: (1,0)}
    deltas = moves[dir]
    next_loc = tuple(map(operator.add, loc, deltas))
    return next_loc


def test():
    pass


test()

with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)
    inputs = deque()
    computer.initialize(program_code, inputs)

    status_map = {}
    dir = 1
    loc = (0,0)
    status_map[loc] = '.'
    history = {}
    visited = set()
    queue = [{'loc': loc, 'steps': 0, 'computer': computer}]

    found = False
    while not found:
        current = queue.pop()
        loc = current['loc']
        if current['loc'] not in visited:
            visited.add(loc)
            current_computer = current['computer']
            steps = current['steps'] + 1
            print('Move', steps, 'loc', loc)

            for dir in range(1,5):
                # print('    Dir', dir)
                move_loc = get_next_loc(loc, dir)
                new_computer = current_computer.clone()

                new_computer.set_inputs(deque([dir]))
                new_computer.reset_outputs()
                done = new_computer.execute()
                status = new_computer.outputs[0]

                # Process status code
                if status == 0:
                    status_map[move_loc] = '#'
                elif status == 1:
                    status_map[move_loc] = '.'
                elif status == 2:
                    status_map[move_loc] = 'X'
                else:
                    print('Unknown status', status)
                    exit(1)

                if status == 2:
                    print('Finished at step', steps)
                    found = True
                elif status == 0:
                    visited.add(move_loc)
                else:
                    queue.append({'loc': move_loc, 'steps': steps, 'computer': new_computer})

            render(status_map, loc)

    assert steps == 304
