import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util
import operator


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


def render(status_map, inters=[]):
    smap = status_map.copy()
    for int in inters:
        smap[int] = 'O'
    image = []
    x_vals, y_vals = zip(*smap.keys())
    for y in range(min(y_vals), max(y_vals)+1):
        row = []
        for x in range(min(x_vals), max(x_vals)+1):
            value = smap.get((x, y))
            if value is None:
                print('None at ', x, y)
                char = ' '
            else:
                char = value
            row.append(char)
        image.append(''.join(row))
    text = '\n'.join(image)
    print(text)


def find_intersections(status_map):
    inters = []
    for loc in status_map:
        if is_intersection(status_map, loc):
            inters.append(loc)
    print('Intersections:', inters)
    return inters


def calc_param(inters):
    value = 0
    for int in inters:
        value += int[0] * int[1]
    return value


def is_intersection(status_map, loc):
    locs = [loc]
    for dir in range(1, 5):
        locs.append(get_next_loc(loc, dir))
    for l in locs:
        if l not in status_map or status_map[l] != '#':
            return False
    return True


def get_next_loc(loc, dir):
    moves = {1: (0,1),
             2: (0,-1),
             3: (-1,0),
             4: (1,0)}
    deltas = moves[dir]
    next_loc = tuple(map(operator.add, loc, deltas))
    return next_loc


def test():
    calc_param([(2,2), (2,4), (6,4), (10,4)]) == 76
    # exit(0)
test()


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)
    inputs = deque()

    computer.run(program_code, inputs)
    status_map = process_outputs(computer.outputs)
    # render(status_map)

    inters = find_intersections(status_map)
    render(status_map, inters)
    alignment_param = calc_param(inters)
    print('Alignment parameter:', alignment_param)
    assert alignment_param == 5724
