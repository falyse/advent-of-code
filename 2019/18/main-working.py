import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import collections
import util
import operator

cache = {}

def solve_maze(input):
    maze = text_to_maze(input)
    loc = get_current_loc(maze)
    dist = get_dist(maze, loc)
    print('Dist:', dist)
    return dist


def get_dist(maze, loc, keyring=set()):
    # Cache key is current location plus collected keys
    cache_key = loc, ''.join(sorted(keyring))
    if cache_key in cache:
        return cache[cache_key]
    if not len(cache) % 100:
        print('Cache len', len(cache), 'keyring', keyring)

    # open_keys = get_open_keys(maze, loc, keyring)
    open_keys = get_open_keys(maze, loc, keyring)
    # print('At loc', loc, 'open keys', open_keys)
    if len(open_keys) == 0:
        dist = 0
    else:
        dists = []
        for k,v in open_keys.items():
            key_dist = v[0]
            key_loc = v[1]
            # print('  check key', k)
            kr = keyring.copy()
            kr.add(k)
            path_dist = get_dist(maze, key_loc, kr)
            dists.append(key_dist + path_dist)
        dist = min(dists)
    cache[cache_key] = dist
    # print('dist', dist)
    return dist


def get_open_keys_old(maze, loc, keyring):
    # BFS to find shortest path from loc to all open keys
    queue = [{'loc': loc, 'steps': 0}]
    visited = set()
    open_keys = {}
    while len(queue) > 0:
        current = queue.pop()
        loc = current['loc']
        if loc not in visited:
            visited.add(loc)
            steps = current['steps']
            for dir in get_open_dirs(maze, loc):
                move_loc = get_next_loc(loc, dir)
                tile = maze[move_loc]
                if tile.isupper() and tile.lower() not in keyring:
                    continue
                if tile.islower() and tile not in keyring:
                    open_keys[tile] = steps+1, move_loc
                else:
                    queue.append({'loc': move_loc, 'steps': steps+1})
    return open_keys



def get_open_keys(maze, start_loc, keyring):
    queue = collections.deque([start_loc])
    distance = {start_loc: 0}
    open_keys = {}
    while queue:
        h = queue.popleft()
        for dir in get_open_dirs(maze, h):
            loc = get_next_loc(h, dir)
            tile = maze[loc]
            if loc in distance:
                continue
            distance[loc] = distance[h] + 1
            if tile.isupper() and tile.lower() not in keyring:
                continue
            if tile.islower() and tile not in keyring:
                open_keys[tile] = distance[loc], loc
            else:
                queue.append(loc)
    return open_keys


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

def get_all_keys(maze):
    return {v for k,v in maze.items() if v.islower()}

def get_current_loc(maze, char='@'):
    locs = [k for k,v in maze.items() if v == char]
    return locs[0]


def text_to_maze(text):
    loc = (0,0)
    maze = {}
    for line in text.strip().splitlines():
        for char in line.strip():
            maze[loc] = char
            loc = (loc[0] + 1, loc[1])
        loc = (0, loc[1] + 1)
    return maze


def test0():
    assert solve_maze(r"""
    #########
    #b.A.@.a#
    #########
        """) == 8
    exit(0)

def test1():
    assert solve_maze(r"""
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
    """) == 86
    exit(0)

def test2():
    assert solve_maze(r"""
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
    """) == 132
    exit(0)

def test3():
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
    exit(0)

def test4():
    assert solve_maze(r"""
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
    """) == 81
    exit(0)

# test3()



with open('input.txt', 'r') as f:
    input = f.read()
    dist = solve_maze(input)
    assert dist == 4954
    # 4978 too high
