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
    all_paths, all_keys = find_all_paths(maze)
    # print(len(all_paths))
    # exit(0)
    src = '@'
    keyring = []
    recurse_path(all_paths, all_keys, src, keyring)
    print('Min steps:', min_steps)
    return min_steps


min_steps = None
def recurse_path(all_paths, all_keys, src, keyring):
    global min_steps
    keyring = keyring.copy()
    keyring.append(src)
    if len(keyring) == len(all_keys) + 1:
        # print(keyring)
        steps = calc_steps(all_paths, keyring)
        if min_steps is None or steps < min_steps:
            min_steps = steps
            print('New min:', min_steps)
            print(keyring)
    for dst in all_keys:
        if dst in keyring:
            continue
        path = all_paths[(src, dst)]
        needs_met = True
        for n in path['needs']:
            if n != src and n != dst and n not in keyring:
                needs_met = False
        if needs_met:
            recurse_path(all_paths, all_keys, dst, keyring)


def calc_steps(all_paths, keyring):
    steps = 0
    prev_key = keyring[0]
    for key in keyring[1:]:
        s = all_paths[(prev_key, key)]['steps']
        steps += s
        # print(prev_key, 'to', key, '=', s, '->', steps)
        prev_key = key
    return steps


def solve_maze_old(input):
    maze = text_to_maze(input)
    all_paths, all_keys = find_all_paths(maze)
    test = {}
    for key_pair, v in all_paths.items():
        n = ''.join(v['needs'])
        print(key_pair, n)
        if len(n) == 14:
            test[key_pair] = (n, len(n))
        # if n not in test:
        #     test[n] = 0
        # test[n] += 1
    # util.pretty_print(util.sort_by_value(test))
    util.pretty_print([(k, x) for k, x in test.items()])
    # exit(0)

    loc = get_current_loc(maze)
    maze[loc] = '.'

    total_steps = 0
    keyring = set()
    curr_key = '@'
    while True:
        keyring.add(curr_key)
        # Find open paths
        open_keys = []
        for key_pair,v in all_paths.items():
            if key_pair[0] == curr_key and key_pair[1] not in keyring:
                needs_met = True
                for n in v['needs']:
                    if n not in keyring:
                        needs_met = False
                if needs_met:
                    open_keys.append(key_pair[1])
        all_paths = remove_key_paths(all_paths, curr_key)
        # Handle open paths
        print('Open keys:', open_keys)
        if len(open_keys) == 0:
            print('Total steps:', total_steps)
            return total_steps
        elif len(open_keys) == 1:
            key = open_keys[0]
            keyring.add(key)
            print('Got key', key)
            curr_key = key
        else:
            print('Len > 1')
            exit(1)
    exit(0)


    maze = text_to_maze(input)
    loc = get_current_loc(maze)
    key_paths = find_key_paths(maze, loc)
    util.pretty_print(key_paths)
    exit(0)
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

def remove_key_paths(all_paths, key):
    # Remove paths to the current key
    temp = all_paths.copy()
    for key_pair, v in temp.items():
        if key_pair[0] == key or key_pair[1] == key:
            del all_paths[key_pair]
    util.pretty_print(all_paths)
    return all_paths

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
                needs = v['needs']
                v['needs'].discard(item)
                v['needs'].discard(k)
                all_paths[(k,item)]['needs'] = v['needs']
                all_paths[(item,k)] = all_paths[(k,item)]
    util.pretty_print(all_paths)
    return all_paths, all_keys


def find_key_paths(maze, loc):
    # BFS to find all the keys
    maze = maze.copy()
    key_paths = {}
    visited = set()
    queue = [{'loc': loc, 'steps': 0, 'needs': set()}]
    while len(queue) > 0:
        current = queue.pop()
        loc = current['loc']
        if current['loc'] not in visited:
            visited.add(loc)
            tile = maze[loc]
            steps = current['steps']
            needs = list(current['needs'])

            # print('At loc', loc, 'in', steps, 'steps')
            if re_key.match(tile):
                # print('  Found key', tile, 'at', steps, 'steps')
                # key_paths[tile] = {'loc': loc, 'steps': steps, 'needs': set(needs)}
                key_paths[tile] = {'steps': steps, 'needs': set(needs)}
                needs.append(tile)
            if re_door.match(tile):
                # print('  Found door', tile, 'at', steps, 'steps')
                needs.append(tile.lower())

            for dir in get_open_dirs(maze, loc):
                # print('    Dir', dir)
                move_loc = get_next_loc(loc, dir)

                moved = True
                if moved:
                    # maze[loc] = '.'
                    queue.append({'loc': move_loc, 'steps': steps+1, 'needs': needs})

            # render(maze, loc)
    return key_paths


def test():
#     assert solve_maze(r"""
# #########
# #b.A.@.a#
# #########
#     """) == 8

    assert solve_maze(r"""
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
    """) == 86

    assert solve_maze(r"""
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
    """) == 132
    exit(0)

    assert solve_maze(r"""
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
    """) == 136

    assert solve_maze(r"""
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
    """) == 81

    exit(0)
# test()


with open('input.txt', 'r') as f:
    solve_maze(f.read())

    # 5134 too high
