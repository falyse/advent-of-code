import sys
sys.path.append('..')
import util
import operator
import re
from itertools import permutations


re_key = re.compile(r'[a-z]')
re_door = re.compile(r'[A-Z]')


def text_to_maze(text):
    loc = (0,0)
    maze = {}
    for line in text.strip().splitlines():
        for char in line.strip():
            maze[loc] = char
            loc = (loc[0] + 1, loc[1])
        loc = (0, loc[1] + 1)
    return maze


def render(maze, loc):
    maze = maze.copy()
    maze[loc] = '@'
    image = []
    x_vals, y_vals = zip(*maze.keys())
    for y in range(min(y_vals), max(y_vals)+1):
        row = []
        for x in range(min(x_vals), max(x_vals)+1):
            value = maze.get((x, y))
            if value is None:
                char = ' '
            else:
                char = value
            row.append(char)
        image.append(''.join(row))
    text = '\n'.join(image)
    print(text)


def maze_has_key(maze):
    return any([re_key.match(x) for x in maze.values()])


def get_current_loc(maze):
    locs = [k for k,v in maze.items() if v == '@']
    return locs[0]


def get_next_loc(loc, dir):
    moves = {1: (0,1),
             2: (0,-1),
             3: (-1,0),
             4: (1,0)}
    deltas = moves[dir]
    next_loc = tuple(map(operator.add, loc, deltas))
    return next_loc


def get_open_dirs(maze, loc):
    opens = []
    for d in range(1, 5):
        val = maze.get(get_next_loc(loc, d))
        if val is not None and val != '#':
            opens.append(d)
    return opens


def solve_maze(input):
    maze = text_to_maze(input)
    loc = get_current_loc(maze)
    all_paths, all_keys = find_all_paths(maze)
    perms = permutations(all_keys)
    min_steps = None
    for p in list(perms):
        prev_key = '@'
        total_steps = 0
        needs_met = True
        for i, key in enumerate(p):
            # First check if all prerequisite keys have been collected
            needs = all_paths[(prev_key, key)]['needs']
            for n in needs:
                if n not in p[0:i]:
                    print(key, 'requires', n)
                    needs_met = False
            if not needs_met:
                continue
            # If so, add the path steps to the total
            steps = all_paths[(prev_key, key)]['steps']
            print(prev_key, 'to', key, '=', steps)
            total_steps += steps
            prev_key = key
        print('Permutation', p, '=', total_steps, 'needs met:', needs_met)
        if not needs_met:
            continue
        if min_steps is None or total_steps < min_steps:
            min_steps = total_steps
    print('Min steps:', min_steps)
    return min_steps


def clear_key_from_maze(maze, key):
    for loc,v in maze.items():
        if v == key or v == key.upper():
            maze[loc] = '.'


def find_all_paths(maze):
    all_paths = {}
    # First create a hash of the current loc and all keys and doors
    items = {'@': get_current_loc(maze)}
    all_keys = set()
    for loc, v in maze.items():
        if re_key.match(v):
            items[v] = loc
            all_keys.add(v)
    # Next, find path lengths from each item to other items
    for item, loc in items.items():
        paths = find_key_paths(maze, loc)
        for k, v in paths.items():
            if k != item:
                all_paths[(k,item)] = {}
                all_paths[(k,item)]['steps'] = v['steps']
                all_paths[(k,item)]['needs'] = [x.lower() for x in v['doors']]
                all_paths[(item,k)] = all_paths[(k,item)]
    util.pretty_print(all_paths)
    return all_paths, all_keys


def find_key_paths(maze, loc):
    # BFS to find all the keys
    maze = maze.copy()
    key_paths = {}
    visited = set()
    queue = [{'loc': loc, 'steps': 0, 'doors': []}]
    while len(queue) > 0:
        current = queue.pop()
        loc = current['loc']
        if current['loc'] not in visited:
            visited.add(loc)
            tile = maze[loc]
            steps = current['steps']
            doors = list(current['doors'])

            # print('At loc', loc, 'in', steps, 'steps')
            if re_key.match(tile):
                # print('  Found key', tile, 'at', steps, 'steps')
                key_paths[tile] = {'loc': loc, 'steps': steps, 'doors': doors}
            if re_door.match(tile):
                # print('  Found door', tile, 'at', steps, 'steps')
                doors.append(tile)

            for dir in get_open_dirs(maze, loc):
                # print('    Dir', dir)
                move_loc = get_next_loc(loc, dir)

                moved = True
                if moved:
                    # maze[loc] = '.'
                    queue.append({'loc': move_loc, 'steps': steps+1, 'doors': doors})

            # render(maze, loc)
    return key_paths


def test():
    assert solve_maze(r"""
#########
#b.A.@.a#
#########
    """) == 8

    assert solve_maze(r"""
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################    
    """) == 86
    
    exit(0)
# test()


with open('input.txt', 'r') as f:
    solve_maze(f.read())
