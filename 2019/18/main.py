import sys
sys.path.append('..')
import util
import operator
import re


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
    maze[loc] = '.'

    total_steps = 0
    keyring = set()
    key_paths = find_key_paths(maze, loc)
    while True:
        render(maze, loc)
        util.pretty_print(key_paths)
        open_keys = [k for k,v in key_paths.items() if len(v['doors']) == 0]
        print('Open keys:', open_keys)
        if len(open_keys) == 0:
            print('Total steps:', total_steps)
            return total_steps
        elif len(open_keys) == 1:
            key = open_keys[0]
            loc = key_paths[key]['loc']
            total_steps += key_paths[key]['steps']
            keyring.add(key)
            print('Got key', key, ': total steps', total_steps)
            clear_key_from_maze(maze, key)
            key_paths = find_key_paths(maze, loc)
        else:
            print('Len > 1')
            exit(1)


def clear_key_from_maze(maze, key):
    for loc,v in maze.items():
        if v == key or v == key.upper():
            maze[loc] = '.'


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
test()


with open('input.txt', 'r') as f:
    solve_maze(f.read())
