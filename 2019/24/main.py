import sys
sys.path.append('..')
import collections
import operator
import util

def text_to_grid(text):
    loc = (0,0)
    grid = collections.defaultdict(str)
    for line in text.strip().splitlines():
        for char in line:
            grid[loc] = char
            loc = (loc[0] + 1, loc[1])
        loc = (0, loc[1] + 1)
    return grid

def render(grid, loc=None):
    grid = grid.copy()
    if loc is not None:
        grid[loc] = '@'
    image = []
    x_vals, y_vals = zip(*grid.keys())
    for y in range(min(y_vals), max(y_vals)+1):
        row = []
        for x in range(min(x_vals), max(x_vals)+1):
            value = grid.get((x, y))
            if value is None:
                char = ' '
            else:
                char = value
            row.append(char)
        image.append(''.join(row))
    text = '\n'.join(image)
    print(text)
    return text


def sim_bugs(input):
    tiles = text_to_grid(input)
    layouts = {}
    while True:
        new = tiles.copy()
        for loc, tile in tiles.items():
            if tile == '#' and num_surrounding(tiles, loc) != 1:
                new[loc] = '.'
            if tile == '.' and num_surrounding(tiles, loc) in [1, 2]:
                new[loc] = '#'
        tiles = new
        text = render(tiles)
        print()
        if text in layouts:
            print('Found repeated layout')
            break
        else:
            layouts[text] = True
    bio = calc_bio(tiles)
    print('Bio calc:', bio)
    return bio


def sim_bugs_steps(input, steps=0):
    tiles = text_to_grid(input)
    if steps:
        for i in range(steps):
            print('Iteration', i)
            new = tiles.copy()
            for loc, tile in tiles.items():
                if tile == '#' and num_surrounding(tiles, loc) != 1:
                    new[loc] = '.'
                if tile == '.' and num_surrounding(tiles, loc) in [1, 2]:
                    new[loc] = '#'
            render(new)
            tiles = new
    return new

def num_surrounding(tiles, loc):
    cnt = 0
    for d in range(1, 5):
        char = tiles.get(get_next_loc(loc, d))
        if char is not None and char == '#':
            cnt += 1
    return cnt

def get_next_loc(loc, dir):
    moves = {1: (0,1),
             2: (0,-1),
             3: (-1,0),
             4: (1,0)}
    deltas = moves[dir]
    next_loc = tuple(map(operator.add, loc, deltas))
    return next_loc


def calc_bio(tiles):
    bio = 0
    tile_list = []
    for y in range(5):
        for x in range(5):
            tile = tiles[(x,y)]
            tile_list.append(tile)
    for i, tile in enumerate(tile_list):
        if tile == '#':
            bio += 2**i
    return bio



def test():
    start = r"""
....#
#..#.
#..##
..#..
#....    
    """

    assert sim_bugs_steps(start, 1) == text_to_grid(r"""
#..#.
####.
###.#
##.##
.##..
    """)

    assert sim_bugs_steps(start, 4) == text_to_grid(r"""
####.
....#
##..#
.....
##...
    """)

    assert calc_bio(text_to_grid(r"""
.....
.....
.....
#....
.#...    
    """)) == 2129920

    assert sim_bugs(start) == 2129920


test()


with open('input.txt', 'r') as f:
    input = f.read()
    bio = sim_bugs(input)
    assert bio == 18859569
