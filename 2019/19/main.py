import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util


def render(status_map, loc=None):
    smap = status_map.copy()
    if loc is not None:
        smap[loc] = 'O'
    image = []
    x_vals, y_vals = zip(*smap.keys())
    for y in range(min(y_vals), max(y_vals)+1):
        row = []
        for x in range(min(x_vals), max(x_vals)+1):
            value = smap.get((x, y))
            if value is None:
                char = ' '
            else:
                char = value
            row.append(char)
        image.append(''.join(row))
    text = '\n'.join(image)
    print(text)


def populate_range(computer, status_map, x_range, y_range):
    cnt = 0
    for y in range(*y_range):
        for x in range(*x_range):
            inputs = deque([x,y])
            computer.run(program_code, inputs)
            if computer.outputs[0]:
                char = '#'
                cnt += 1
            else:
                char = '.'
            status_map[(x, y)] = char
    return cnt


def check_point(computer, x, y):
    inputs = deque([x,y])
    computer.run(program_code, inputs)
    result = computer.outputs[0]
    print('Check', x, y, ':', result)
    return result


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)
    inputs = deque()
    computer.initialize(program_code, inputs)

    # Part 1
    status_map = {}
    cnt = populate_range(computer, status_map, (0,50), (0,50))
    assert cnt == 179
    render(status_map)

    # Part 2
    # Search along bottom edge of the beam
    #   and check if opposite edge of the square is still in the beam
    x = 0
    y = 99
    value = 0
    while True:
        # Move right until in the beam
        if not check_point(computer, x, y):
            x += 1
        else:
            # Check if the whole square fits at the current point
            if check_point(computer, x+99, y-99):
                print('Found at', x, y)
                value = 10000*x + y-99
                print('Value', value)
                break
            # Move down until out of the beam
            while check_point(computer, x, y):
                y += 1
    assert value == 9760485
