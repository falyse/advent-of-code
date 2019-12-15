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


def render(status_map, loc):
    smap = status_map.copy()
    smap[loc] = 'D'
    image = []
    x_vals, y_vals = zip(*smap.keys())
    for y in (range(min(y_vals), max(y_vals)+1)):
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


def get_unfilled(status_map):
    num = 0
    for k, v in status_map.items():
        if v == '.':
            num += 1
    return num


max_depth = 0
def set_adjacent(status_map, loc, depth=0):
    global max_depth
    if depth > max_depth:
        max_depth = depth
    print('Depth', depth, 'max', max_depth)
    render(status_map, loc)
    # if depth == 25:
    #     exit(1)
    adj_dir = search_for_exit(status_map, loc)
    for d in adj_dir:
        adj_loc = get_next_loc(loc, d)
        status_map[adj_loc] = 'O'
        status_map = set_adjacent(status_map, adj_loc, depth+1)
    return status_map



with open('map.txt', 'r') as f:
    x = 0
    y = 0
    status_map = {}
    loc = (0,0)
    for line in f.readlines():
        y += 1
        x = 0
        for char in line.strip('\n'):
            x += 1
            status_map[(x,y)] = char
            if char == 'X':
                loc = (x,y)
    print('Loc', loc)
    render(status_map, loc)

    # Set adjacent squares
    status_map = set_adjacent(status_map, loc)
    print('Max depth', max_depth)


# 311 too high
