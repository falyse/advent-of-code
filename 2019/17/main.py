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
        if o == 35:
            status_map[loc] = '#'
        elif o == 46:
            status_map[loc] = '.'
        elif o == 60:
            status_map[loc] = '>'
        elif o == 62:
            status_map[loc] = '<'
        elif o == 94:
            status_map[loc] = '^'
        elif o == 76:
            status_map[loc] = 'v'
        elif o == 58:
            status_map[loc] = 'X'
        elif o == 10:
            loc = (0, loc[1] + 1)
            print(status_map)
        else:
            print('Unrecognized code', o)
            exit(1)
        if o != 10:
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
    exit(0)

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
