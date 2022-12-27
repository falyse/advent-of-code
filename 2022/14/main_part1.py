import sys
sys.path.append('../..')
import util


def process(input):
    grid = build_grid(input)
    i = 0
    finish = False
    while not finish:
        grid, finish = drop_sand(grid)
        if not finish:
            i += 1
    print(util.grid_dict_to_text(grid, empty_fill_char='.'))
    return i


def build_grid(input):
    lines = input.strip().splitlines()
    rock_coords = []
    for line in lines:
        coords = []
        for point in line.split(' -> '):
            x, y = util.ints(point)
            coords.append((x,y))
            rock_coords.append((x,y))
        for i in range(1, len(coords)):
            dx, dy = util.tuple_sub(coords[i], coords[i-1])
            for a in range(abs(dx)):
                coord = (coords[i][0] - sign(dx)*a, coords[i][1])
                rock_coords.append(coord)
            for b in range(abs(dy)):
                coord = (coords[i][0], coords[i][1] - sign(dy)*b)
                rock_coords.append(coord)
    grid = {}
    for coord in rock_coords:
        grid[coord] = '#'
    # print(util.grid_dict_to_text(grid, empty_fill_char='.'))
    return grid


def drop_sand(grid):
    test_loc = (500, 0)
    at_rest = False
    while not at_rest:
        loc = test_loc
        test_loc = util.coord_move(loc, 'N')
        if loc_is_blocked(grid, test_loc):
            test_loc = util.coord_move(test_loc, 'W')
            if loc_is_blocked(grid, test_loc):
                test_loc = util.coord_move(test_loc, 'E', 2)
                if loc_is_blocked(grid, test_loc):
                    at_rest = True
        if loc[1] > 1000:
            return grid, True
    grid[loc] = 'o'
    return grid, False


def loc_is_blocked(grid, loc):
    return grid.get(loc) in ['#', 'o']


def sign(x):
    if x < 0:
        return -1
    if x == 0:
        return 0
    if x > 0:
        return 1

def test():
    test_input = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
    '''
    assert(process(test_input) == 24)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
    assert(val == 757)
