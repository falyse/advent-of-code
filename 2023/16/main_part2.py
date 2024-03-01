import sys
sys.path.append('../..')
import util

sys.setrecursionlimit(1000000)

visited = set()

def process(input):
    grid = util.text_to_grid_dict(input.strip())
    min, max = util.grid_dict_coord_range(grid)
    start_locs = []
    for y in range(min[1], max[1]):
        start_locs.append(((-1, y), 'E'))
        start_locs.append(((max[0]+1, y), 'W'))
    for x in range(min[0], max[0]):
        start_locs.append(((x, -1), 'N'))
        start_locs.append(((x, max[1]+1), 'S'))
    
    max_energy = 0
    for loc, dir in start_locs:
        # print('Start loc', loc, dir)
        energy = grid.copy()
        visited.clear()
        run_beam(loc, dir, grid, energy)
        # util.render_grid(energy)
        num = sum([1 for v in energy.values() if v == '#'])
        if num > max_energy:
            max_energy = num
    print('max_energy', max_energy)
    return max_energy


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
    # print('loc', loc, 'dir', dir, 'next', loc, next_char)

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
    assert(process(test_input) == 51)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Result:', val)
