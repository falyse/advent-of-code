import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util

from itertools import permutations

def render(grid):
    for line in grid:
        print(''.join(line))

match = util.make_grid(10, 10, fill='.')
def process_grid(grid):
    cnts = util.make_grid(len(grid[0]), len(grid), fill=0)
    print(cnts)
    max = 0
    for y,line in enumerate(grid):
        for x,char in enumerate(line):
            cnt = 0
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
                    if search_path(grid, x, y, dx, dy):
                        cnt += 1
                # if search_path(grid, x, y, 3, -1):
                #     cnt += 1
                # if search_path(grid, x, y, 2, -1):
                #     cnt += 1
                # if search_path(grid, x, y, 1, -1):
                #     cnt += 1
                cnts[y][x] = cnt
                if cnt > max:
                    max = cnt
                if x == y == 0:
                    print('Count 0,0:', cnt)
    print(cnts)
    render(match)
    return cnts, max

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
    debug = x == 0 and y == 0
    while True:
        x += delta_x
        y += delta_y
        if x < 0 or x >= len(line):
            break
        if y < 0 or y >= len(line):
            break
        if grid[y][x]:
            if debug:
                print('  search path', delta_x, delta_y, 'found',  x, y, 'input', input[y][x])
                # print(x,y)
                # match[y][x] = '#'
            # print('    found', x, y)
            return True
    return False


def test():
    pass


test()

with open('input.txt', 'r') as f:
# with open('test-4.txt', 'r') as f:
    input = [x.strip() for x in f.readlines()]
    print(input)
    grid = util.make_grid(len(input[0]), len(input), fill=False)
    for y,line in enumerate(input):
        for x,char in enumerate(line):
            # print('xy', x, y, 'char', char)
            grid[y][x] = char != '.'
    print(grid)

    counts,max = process_grid(grid)
    print('Max', max)


