import sys
sys.path.append('..')
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

    open_keys = get_open_keys(maze, keyring)
    # print('At loc', loc, 'open keys', open_keys)
    if len(open_keys) == 0:
        dist = 0
    else:
        dists = []
        for k,v in open_keys.items():
            key_dist = v[0]
            key_loc = v[1]
            key_quad = v[2]
            # print('  check key', k)
            kr = keyring.copy()
            kr.add(k)
            path_dist = get_dist(maze, key_loc, kr)
            dists.append(key_dist + path_dist)
        dist = min(dists)
    cache[cache_key] = dist
    # print('dist', dist)
    return dist


def get_open_keys(maze, keyring):
    start_locs = get_current_locs(maze)
    queue = collections.deque(start_locs)
    distance = {}
    for start_loc in start_locs:
        distance[start_loc] = 0
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
                open_keys[tile] = distance[loc], loc, quad
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
#######
#a.#Cd#
##@#@##
#######
##@#@##
#cB#.b#
#######    
        """) == 8
    exit(0)

def test1():
    assert solve_maze(r"""
###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############
    """) == 24
    exit(0)

def test2():
    assert solve_maze(r"""
#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############
    """) == 32
    exit(0)

def test3():
    assert solve_maze(r"""
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
    """) == 72
    exit(0)

# test0()



with open('input-part2.txt', 'r') as f:
    input = f.read()
    dist = solve_maze(input)
