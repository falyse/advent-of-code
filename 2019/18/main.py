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
    for y in reversed(range(min(y_vals), max(y_vals)+1)):
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
    render(maze, loc)

    # BFS to all letters
    keyring = set()
    visited = set()
    queue = [{'loc': loc, 'steps': 0}]
    while maze_has_key(maze):
        current = queue.pop()
        loc = current['loc']
        if current['loc'] not in visited:
            visited.add(loc)
            steps = current['steps']
            print('At loc', loc, 'in', steps, 'steps')

            for dir in get_open_dirs(maze, loc):
                print('    Dir', dir)
                move_loc = get_next_loc(loc, dir)

                moved = True
                if re_key.match(maze[loc]):
                    print('  Found key', maze[loc], 'at', steps, 'steps')
                    keyring.add(maze[loc])
                if re_door.match(maze[loc]):
                    print('  Found door', maze[loc], 'at', steps, 'steps')
                    matching_key = maze[loc].lower()
                    if matching_key in keyring:
                        print('    unlocked!')
                    else:
                        print('    locked')
                        moved = False
                if moved:
                    maze[loc] = '.'
                    queue.append({'loc': move_loc, 'steps': steps+1})

            render(maze, loc)


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
    
    exit(0)
test()


with open('input.txt', 'r') as f:
    solve_maze(f.read())
