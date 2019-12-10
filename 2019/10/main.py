import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
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
                # deltas = range(-4,5)
                combos = get_combos(len(line))
                for dx,dy in combos:
                # for dx in deltas:
                #     for dy in deltas:
                #     if ((dx != dy or dx == 1) and
                #             (dx != 0 or dy == 1) and
                #             (dy != 0 or dx == 1)):
                    coord = search_path(grid, x, y, dx, dy)
                    if coord is not None:
                        cnt += 1
                        if x == 11 and y == 13:
                            print('asdf1', coord)
                        coords.append(coord)
                # if search_path(grid, x, y, 3, -1):
                #     cnt += 1
                # if search_path(grid, x, y, 2, -1):
                #     cnt += 1
                # if search_path(grid, x, y, 1, -1):
                #     cnt += 1
                cnts[y][x] = cnt
                if cnt > max:
                    max_coords = (x,y)
                    max = cnt
                    clist = coords.copy()
                if x == y == 0:
                    print('Count 0,0:', cnt)
    print(cnts)
    # render(match)
    # for c in coords:
    #     print(c)
    # exit(1)
    return cnts, max_coords, max, clist

def get_combos(max):
    combos = get_offset_combos(1, 0)
    # combos.extend(get_offset_combos(2, 1))
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
    # print(valid)
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
    # if (delta_x == delta_y == 0 or (delta_x == 0 and delta_y == 2) or (delta_x == 2 and delta_y == 0) or
    #     (delta_x == 0 and delta_y == -2) or (delta_x == -2 and delta_y == 0) or
    #     delta_x == delta_y == 2 or delta_x == delta_y == -2):
    #     return False
    # print('  search path', delta_x, delta_y)
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
                print('  search path', delta_x, delta_y, 'found',  x, y, 'input', input[y][x], 'angle', get_angle((delta_x, delta_y)))
                # print(x,y)
                # match[y][x] = '#'
            # print('    found', x, y)
            return (x,y, get_angle((delta_x, delta_y)))
    return None

def get_angle(coord):
    x,y = coord
    angle = math.atan2(-1*y, x) * 180/math.pi
    # angle = math.atan2(y, x) * 180/math.pi
    # print(x, y, angle)
    # angle = 360 - angle
    # angle -= 90
    # if angle < 0:
    #     angle += 360
    angle = (90 - angle) % 360
    # print(' ', x, y, angle)
    return angle

def test():
    assert get_angle((0,-1)) == 0
    assert get_angle((1,0)) == 90
    assert get_angle((0,1)) == 180
    assert get_angle((-1,0)) == 270
    assert get_angle((1,-1)) == 45
    # exit(0)


test()

with open('input.txt', 'r') as f:
# with open('test-4.txt', 'r') as f:
    input = [x.strip() for x in f.readlines()]
    print(input)
    x_size = len(input[0])
    y_size = len(input)
    size = max(x_size, y_size)
    grid = util.make_grid(size, size, fill=False)
    for y,line in enumerate(input):
        for x,char in enumerate(line):
            # print('xy', x, y, 'char', char)
            grid[y][x] = char != '.'
    # render(grid)

    counts,max_coords, max_count,coords = process_grid(grid)
    print('Max', max_count, 'at', max_coords, 'coords', coords)

    for c in coords:
        print(c)
    # for x,y,angle in coords:
    #     if x == 11:
    #         print('asdf', x, y, angle)
    print()
    # exit(1)

    step_max = 200
    # step_max = 18+9+9
    step = 0
    while True:
        sorted_coords = []
        coords = sorted(coords, key=lambda x: x[2])
        print('coords len', len(coords))
        render(grid)
        for x,y,angle in coords:
            step += 1
            if step == step_max:
                print('Reached %0d: ' % step_max, x, y)
                print('  ', x*100 + y)
                exit(0)
            grid[y][x] = False
            print('Step', step, 'vaporized', x, y, 'angle', angle)
        coords = vaporize_grid(grid, max_coords)


# 2012 wrong
# 3119 wrong
# 3018 wrong
# 1625 wrong
# 1708 wrong


