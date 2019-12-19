import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util
import operator
import random

random.seed(2)

def change_dir(status_map, loc, dir):
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


def reverse_dir(dir):
    if dir == 1:
        return 2
    if dir == 2:
        return 1
    if dir == 3:
        return 4
    if dir == 4:
        return 3


def render(status_map, loc=None):
    smap = status_map.copy()
    if loc is not None:
        smap[loc] = 'O'
    image = []
    x_vals, y_vals = zip(*smap.keys())
    for y in range(min(y_vals), max(y_vals)+1):
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

def process_outputs(outputs):
    status_map = {}
    loc = (0,0)
    for o in outputs:
        if o == 10:
            loc = (0, loc[1] + 1)
        else:
            status_map[loc] = chr(o)
            loc = (loc[0] + 1, loc[1])
    return status_map

def show(status_map, loc, size):
    smap = status_map.copy()
    cnt = 0
    for x in range(size):
        for y in range(size):
            l = (loc[0]+x, loc[1]+y)
            if l not in smap or smap[l] == '.':
                smap[l] = 'X'
            else:
                smap[l] = 'O'
                cnt += 1
    render(smap, (0,0))
    return cnt == 2*size - 1

def check_square(status_map, loc, size, show=False):
    smap = status_map.copy()
    cnt = 0
    x0, y0 = loc
    for x in range(size):
        l = (x0+x, y0)
        if l not in smap or smap[l] == '.':
            smap[l] = 'X'
        else:
            smap[l] = 'O'
            cnt += 1
    for y in range(size):
        l = (x0, y0+y)
        if l not in smap or smap[l] == '.':
            smap[l] = 'X'
        else:
            smap[l] = 'O'
            cnt += 1
    if show:
        render(smap, (0,0))
    print('cnt', cnt)
    return cnt == 2*size

def populate_range(computer, status_map, x_range, y_range):
    for y in range(*y_range):
        for x in range(*x_range):
            inputs = deque([x,y])
            computer.run(program_code, inputs)
            if computer.outputs[0]:
                char = '#'
            else:
                char = '.'
            status_map[(x, y)] = char


def test():
    pass


test()

def check_point(computer, x, y):
    inputs = deque([x,y])
    computer.run(program_code, inputs)
    result = computer.outputs[0]
    print('Check', x, y, ':', result)
    return result

with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)
    inputs = deque()
    computer.initialize(program_code, inputs)

    x = 0
    y = 99
    value = 0
    while True:
        # Move right until in the beam
        if not check_point(computer, x, y):
            x += 1
        else:
            # Check if the whole square fits at the current point
            if check_point(computer, x+99, y-99):
                print('Found at', x, y)
                value =  10000*x + y-99
                print('Value', value)
                break
            # Move down until out of the beam
            while check_point(computer, x, y):
                y += 1
    assert value == 9760485
