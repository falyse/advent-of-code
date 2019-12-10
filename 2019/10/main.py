import sys
sys.path.append('..')
import util

from itertools import permutations
import math

def render(grid):
    for line in grid:
        line = ['#' if x else '.' for x in line]
        print(''.join(line))

match = util.make_grid(10, 10, fill='.')


def vaporize_grid(grid, start_coords):
    x, y = start_coords
    coords = []
    combos = get_combos(len(line))
    for dx,dy in combos:
        coord = search_path(grid, x, y, dx, dy)
        if coord is not None:
            coords.append(coord)
    return coords

def process_grid(grid):
    cnts = util.make_grid(len(grid[0]), len(grid), fill=0)
    print(cnts)
    max = 0
    clist = []
    for y,line in enumerate(grid):
        for x,char in enumerate(line):
            cnt = 0
            coords = []
            if grid[y][x]:
                # print('Asteroid at', x, y)
                combos = get_combos(len(line))
                for dx,dy in combos:
                    coord = search_path(grid, x, y, dx, dy)
                    if coord is not None:
                        cnt += 1
                        coords.append(coord)
                cnts[y][x] = cnt
                if cnt > max:
                    max_coords = (x,y)
                    max = cnt
                    clist = coords.copy()
    print(cnts)
    return cnts, max_coords, max, clist

def get_combos(max):
    combos = get_offset_combos(1, 0)
    for i in range(max):
        combos.extend([(-1*i,-1), (-1*i,1), (i,-1), (i,1)])
        combos.extend([(-1,-1*i), (1,-1*i), (-1,i), (1,i)])
    for i in range(max):
        for j in range(2,max):
            if i > j and i % j:
                combos.extend([(-1*i,-1*j), (-1*i,j), (i,-1*j), (i,j)])
                combos.extend([(-1*j,-1*i), (j,-1*i), (-1*j,i), (j,i)])
    combos = set(combos)

    valid = []
    for x,y in combos:
        ok = True
        for i in range(2,max):
            if not x %i and not y % i:
                ok = False
        if ok:
            valid.append((x,y))
    valid = set(valid)
    return valid

def get_offset_combos(offset, mid):
    list1 = [-1*offset, mid, offset]
    combos = [zip(x,list1) for x in permutations(list1, len(list1))]
    combos = util.flatten(combos)
    combos = set(combos)
    if (0,0) in combos:
        combos.remove((0, 0))
    return list(combos)

def search_path(grid, x, y, delta_x, delta_y):
    debug = x == 11 and y == 13
    while True:
        x += delta_x
        y += delta_y
        if x < 0 or x >= len(line):
            break
        if y < 0 or y >= len(line):
            break
        if grid[y][x]:
            if debug and x == 11:
                print('  search path', delta_x, delta_y, 'found',  x, y, 'angle', get_angle((delta_x, delta_y)))
                # print(x,y)
                # match[y][x] = '#'
            # print('    found', x, y)
            return (x,y, get_angle((delta_x, delta_y)))
    return None

def get_angle(coord):
    x,y = coord
    angle = math.atan2(-1*y, x) * 180/math.pi
    # Convert to clockwise angle
    angle = (90 - angle) % 360
    return angle


def test():
    assert get_angle((0,-1)) == 0
    assert get_angle((1,0)) == 90
    assert get_angle((0,1)) == 180
    assert get_angle((-1,0)) == 270
    assert get_angle((1,-1)) == 45

    assert find_station_location(
r'''.#..#
.....
#####
....#
...##
''') == ((3,4), 8)
    exit(0)


def find_station_location(text):
    grid = util.text_to_grid(text)
    grid = util.grid_map(grid, {'#': True, '.': False})
    print(grid)


# test()

with open('input.txt', 'r') as f:
# with open('test-4.txt', 'r') as f:
#     input = [x.strip() for x in f.readlines()]
#     print(input)
#     x_size = len(input[0])
#     y_size = len(input)
#     size = max(x_size, y_size)
#     grid = util.make_grid(size, size, fill=False)
#     for y,line in enumerate(input):
#         for x,char in enumerate(line):
#             grid[y][x] = char != '.'
    grid = util.text_to_grid(f.read())
    grid = util.grid_map(grid, {'#': True, '.': False})
    line = grid[0]

    counts,max_coords, max_count,coords = process_grid(grid)
    print('Max', max_count, 'at', max_coords, 'coords', coords)
    assert max_count == 326

    # Part 2
    step_max = 200
    step = 0
    while True:
        sorted_coords = []
        coords = sorted(coords, key=lambda x: x[2])
        render(grid)
        for x,y,angle in coords:
            step += 1
            grid[y][x] = False
            print('Step', step, 'vaporized', x, y, 'angle', angle)
            if step == step_max:
                print('Reached step %0d: ' % step_max, x, y)
                value = x*100 + y
                print('  ', value)
                assert value == 1623
                exit(0)
        coords = vaporize_grid(grid, max_coords)


