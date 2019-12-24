import sys
sys.path.append('..')
import collections
import operator
import copy
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

def text_to_layers(text):
    tile_text = text.split(',')
    layers = {i-1: text_to_grid(x) for i, x in enumerate(tile_text)}
    print(layers)
    return layers


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


def sim_bugs_steps(input, steps=0):
    layers = {0: text_to_grid(input)}
    if steps:
        for i in range(steps):
            print('Iteration', i)
            layers[-i-1] = blank_tile()
            layers[i+1] = blank_tile()
            new = copy.deepcopy(layers)
            for layer, tiles in layers.items():
                for loc, tile in tiles.items():
                    if tile == '#' and num_surrounding(layers, layer, loc) != 1:
                        new[layer][loc] = '.'
                    if tile == '.' and num_surrounding(layers, layer, loc) in [1, 2]:
                        new[layer][loc] = '#'
                new[layer][2, 2] = '.'
            layers = new

            for layer, tiles in sorted(layers.items()):
                print('  Layer', layer)
                render(tiles)
    return layers

def num_surrounding(layers, layer, loc):
    num = 0
    for d in range(1, 5):
        next_loc = get_next_loc(loc, d)
        if next_loc == (2, 2):
            if layer+1 not in layers:
                continue
            if loc == (2, 1):
                num += num_row(layers, layer+1, 0)
            if loc == (2, 3):
                num += num_row(layers, layer+1, 4)
            if loc == (1, 2):
                num += num_col(layers, layer+1, 0)
            if loc == (3, 2):
                num += num_col(layers, layer+1, 4)
        else:
            char = layers[layer].get(next_loc)
            if char is not None and char == '#':
                num += 1
    # At inner most layer
    if layer+1 not in layers:
        if loc[1] == 0:
            num += layers[layer-1][2, 1] == '#'
        if loc[1] == 4:
            num += layers[layer-1][2, 3] == '#'
        if loc[0] == 0:
            num += layers[layer-1][1, 2] == '#'
        if loc[0] == 4:
            num += layers[layer-1][3, 2] == '#'
    return num

def num_row(layers, layer, y):
    num = sum([1 for loc, tile in layers[layer].items() if tile == '#' and loc[1] == y])
    return num

def num_col(layers, layer, x):
    num = sum([1 for loc, tile in layers[layer].items() if tile == '#' and loc[0] == x])
    return num

def blank_tile():
    return text_to_grid(r"""
.....
.....
.....
.....
.....
    """)

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

    assert sim_bugs_steps(start, 1) == text_to_layers(r"""
.....
..#..
...#.
..#..
.....,

#..#.
####.
##..#
##.##
.##..,

....#
....#
....#
....#
#####
    """)
    exit(0)

    assert sim_bugs_steps(start, 10) == text_to_grid(r"""
.#...
.#.##
.#...
.....
.....    
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
