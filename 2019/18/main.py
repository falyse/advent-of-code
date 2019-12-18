import sys
sys.path.append('..')
import util
import operator
import re


def text_to_maze(text):
    loc = (0,0)
    maze = {}
    for line in text.strip().splitlines():
        for char in line.strip():
            maze[loc] = char
            loc = (loc[0] + 1, loc[1])
        loc = (0, loc[1] + 1)
    return maze


def render(maze):
    maze = maze.copy()
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
    return any([re_key.match(x) for x in maze])


def get_current_loc(maze):
    locs = [v for v in maze.values() if v == '@']
    return locs[0]


def get_next_loc(loc, dir):
    moves = {1: (0,1),
             2: (0,-1),
             3: (-1,0),
             4: (1,0)}
    deltas = moves[dir]
    next_loc = tuple(map(operator.add, loc, deltas))
    return next_loc


def get_open_dirs(status_map, loc):
    opens = []
    for d in range(1, 5):
        val = status_map.get(get_next_loc(loc, d))
        if val is not None and val != '#':
            opens.append(d)
    return opens


def test():
    pass
test()


with open('input.txt', 'r') as f:
    maze = text_to_maze(f.read().strip())
    loc = get_current_loc(maze)
    render(maze)

    re_key = re.compile(r'[a-z]')
    re_door = re.compile(r'[A-Z]')

    # BFS to all letters
    keyring = set()
    visited = set()
    queue = [{'loc': loc, 'steps': 0}]
    found = False
    while not maze_has_key():
        current = queue.pop()
        loc = current['loc']
        if current['loc'] not in visited:
            visited.add(loc)
            steps = current['steps'] + 1
            print('Move', steps, 'loc', loc)

            open_dirs =
            for dir in range(1,5):
                print('    Dir', dir)
                move_loc = get_next_loc(loc, dir)

                if re_key.match(maze[loc]):
                    print('  Found key', maze[loc], 'at', steps, 'steps')
                    keyring.add(maze[loc])
                    maze[loc] = '.'
                if re_door.match(maze[loc]):
                    print('  Found door', maze[loc], 'at', steps, 'steps')
                    matching_key = maze[loc].lower()
                    if matching_key in keyring:
                        print('    unlocked!')
                    else:
                        print('    locked')


                all_keys_found = not maze_has_key(maze)
                if status == 2:
                    print('Finished at step', steps)
                    found = True
                elif status == 0:
                    visited.add(move_loc)
                else:
                    queue.append({'loc': move_loc, 'steps': steps, 'computer': new_computer})

            render(maze, loc)

    assert steps == 304
