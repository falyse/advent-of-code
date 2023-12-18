import sys
sys.path.append('../..')
import util

sys.setrecursionlimit(1000000)

visited = set()

def process(input):
    grid = util.text_to_grid_dict(input.strip())
    energy = grid.copy()
    loc = (-1,0)
    dir = 'E'
    visited.clear()
    run_beam(loc, dir, grid, energy)
    print(energy)
    util.render_grid(energy)
    num = sum([1 for v in energy.values() if v == '#'])
    print('num', num)
    return num


def run_beam(prev_loc, dir, grid, energy):
    loc = util.coord_move(prev_loc, dir)
    if loc not in grid:
        return
    energy[loc] = '#'
    if (loc, dir) in visited:
        return
    visited.add((loc, dir))
    if loc not in grid:
        return
    next_char = grid[loc]
    print('loc', loc, 'dir', dir, 'next', loc, next_char)

    if next_char == '.':
        run_beam(loc, dir, grid, energy)

    elif next_char == '|':
        if dir in ['E', 'W' ]:
            run_beam(loc, 'N', grid, energy)
            run_beam(loc, 'S', grid, energy)
        else:
            run_beam(loc, dir, grid, energy)

    elif next_char == '-':
        if dir in ['N', 'S' ]:
            run_beam(loc, 'E', grid, energy)
            run_beam(loc, 'W', grid, energy)
        else:
            run_beam(loc, dir, grid, energy)

    elif next_char == '\\':
        if dir == 'E':
            run_beam(loc, 'N', grid, energy)
        if dir == 'N':
            run_beam(loc, 'E', grid, energy)
        if dir == 'W':
            run_beam(loc, 'S', grid, energy)
        if dir == 'S':
            run_beam(loc, 'W', grid, energy)

    elif next_char == '/':
        if dir == 'E':
            run_beam(loc, 'S', grid, energy)
        if dir == 'S':
            run_beam(loc, 'E', grid, energy)
        if dir == 'W':
            run_beam(loc, 'N', grid, energy)
        if dir == 'N':
            run_beam(loc, 'W', grid, energy)

def test():
    test_input = r'''
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....

    '''
    assert(process(test_input) == 46)

test()
# exit(0)


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Result:', val)
