import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util
from collections import deque, OrderedDict
import operator


def run_robot(outputs):
    global rnum
    global grid
    global rx
    global ry
    global dir
    color = outputs[0]
    next_dir = outputs[1]
    grid[rx][ry] = color
    if next_dir == 0:
        dir -= 90
    else:
        dir += 90
    if dir <= -180:
        dir += 360
    if dir > 180:
        dir -= 360
    # print('  dir', dir)
    if dir == 0:
        ry += 1
    elif dir == 90:
        rx += 1
    elif dir == 180:
        ry -= 1
    elif dir == -90:
        rx -= 1
    else:
        print('Unknown dir', dir)
        exit(1)
    if not rx in grid:
        grid[rx] = {}
    if not ry in grid[rx]:
        grid[rx][ry] = 0
        rnum += 1
    return grid[rx][ry]


def reset(first_color):
    pass
    # global grid
    # global rx
    # global ry
    # global dir
    # global rnum
    #
    # grid = {}
    # grid[0] = {}
    # grid[0][0] = first_color
    #
    # rx = 0
    # ry = 0
    # dir = 0
    # rnum = 1



def test():
    pass


test()

with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)

    dirs = [x for x in range(4)]
    moves = {0: (0,1),
             1: (1,0),
             2: (0,-1),
             3: (-1,0)}

    # Part 1
    inputs = deque()
    computer.initialize(program_code, inputs)
    panels = {(0, 0): 0}
    done = False
    x = y = 0
    dir = 0
    while not done:
        inputs.append(panels[(x,y)])
        done = computer.execute()
        color, turn = computer.outputs[-2:]
        panels[(x,y)] = color
        print('asdf0 dir', dir, 'turn', turn)
        if turn:
            dir += 1
        else:
            dir -= 1
        if dir > 3:
            dir = 0
        if dir < 0:
            dir = 3
        deltas = moves[dir]
        print('asdf1 dir', dir, 'detlas', deltas, 'x', x, 'y', y)
        x,y = tuple(map(operator.add, (x,y), deltas))
        print('asdf2 x', x, 'y', y)
    print('Final rnum', rnum)
    assert rnum == 2088

    exit(0)
    # Part 2
    reset(1)
    run_program(program_code, 1)

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    min_x, max_x = util.min_max(grid.keys())
    for row in grid.keys():
        a, b = util.min_max(grid[row].keys())
        if a < min_y:
            min_y = a
        if b > max_y:
            max_y = b

    print('maxes', min_x, max_x, min_y, max_y)
    temp = util.make_grid(abs(min_y)+1, max_x, fill = ' ')
    for ix in range(min_x, max_x+1):
        # for iy in range(max_y+2, min_y-1, -1):
        for iy in range(0, -6, -1):
            try:
                if grid[ix][iy] == 1:
                    temp[abs(iy)][ix] = '#'
            except:
                pass
    render = util.grid_to_text(temp, map={})
    print(render)
    assert render == '\n'.join([
        ' #  # ###   ##   ##  #### #     ##  ###   ',
        ' #  # #  # #  # #  # #    #    #  # #  #  ',
        ' #  # #  # #    #  # ###  #    #    #  #  ',
        ' #  # ###  #    #### #    #    #    ###   ',
        ' #  # # #  #  # #  # #    #    #  # #     ',
        '  ##  #  #  ##  #  # #    ####  ##  #     '])


