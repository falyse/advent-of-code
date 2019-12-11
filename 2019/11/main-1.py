import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util
from collections import deque
import operator


def run_robot(start_color):
    moves = {0: (0,1),
             1: (1,0),
             2: (0,-1),
             3: (-1,0)}

    inputs = deque()
    computer.initialize(program_code, inputs)
    loc = (0,0)
    dir = 0
    panels = {loc: start_color}
    done = False
    while not done:
        if loc not in panels:
            panels[loc] = 0
        inputs.append(panels[loc])
        done = computer.execute()
        color, turn = computer.outputs[-2:]
        panels[loc] = color
        dir = get_next_dir(dir, turn)
        deltas = moves[dir]
        loc = tuple(map(operator.add, loc, deltas))
    return panels


def get_next_dir(dir, turn):
    if turn:
        dir += 1
    else:
        dir -= 1
    if dir > 3:
        dir = 0
    if dir < 0:
        dir = 3
    return dir


def render_panels(panels):
    image = []
    x_vals, y_vals = zip(*panels.keys())
    for y in reversed(range(min(y_vals), max(y_vals)+1)):
        row = []
        for x in range(min(x_vals), max(x_vals)+1):
            row.append('#' if panels.get((x,y)) else ' ')
        image.append(''.join(row))
    return '\n'.join(image)


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)

    # Part 1
    panels = run_robot(0)
    num_panels = len(panels)
    print('Num panels:', num_panels)
    assert num_panels == 2088

    # Part 2
    panels = run_robot(1)
    render = render_panels(panels)
    print()
    print(render)
    assert render == '\n'.join([
        ' #  # ###   ##   ##  #### #     ##  ###    ',
        ' #  # #  # #  # #  # #    #    #  # #  #   ',
        ' #  # #  # #    #  # ###  #    #    #  #   ',
        ' #  # ###  #    #### #    #    #    ###    ',
        ' #  # # #  #  # #  # #    #    #  # #      ',
        '  ##  #  #  ##  #  # #    ####  ##  #      '])

