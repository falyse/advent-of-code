import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util
from collections import deque
import os
import time

render = False
screen = {}


def process_outputs(outputs):
    tiles = []
    for i in range(0, len(outputs), 3):
        tiles.append(outputs[i:i+3])
    return tiles


def render_screen(tiles):
    for x, y, id in tiles:
        if x >= 0:
            if (x,y) not in screen:
                screen[(x,y)] = ' '
            char = ' '
            if id == 1:
                char = '█'
            if id == 2:
                char = '▭'
            if id == 3:
                char = '▀'
            if id == 4:
                char = '●'
            screen[(x,y)] = char
    # Display the screen
    lines = []
    for y in range(0,22):
        lines.append(''.join([screen[(x,y)] for x in range(0,37)]))
    out = '\n'.join(lines) + '\n'
    out += '█' * 37 + '\n'
    out += ' ' * 12 + 'Score: %5d\n\n' % score
    # os.system('clear')
    sys.stdout.write(out)
    sys.stdout.flush()
    time.sleep(0.02)


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)
    inputs = deque()

    # Part 1
    computer.run(program_code, inputs)
    outputs = computer.outputs
    tiles = process_outputs(outputs)
    num_blocks = sum([1 for x in tiles if x[2] == 2])
    print('Num blocks:', num_blocks)
    assert num_blocks == 344

    # Part 2
    program_code[0] = 2
    computer.initialize(program_code, inputs)

    score = 0
    while True:
        computer.reset_outputs()
        done = computer.execute()
        outputs = computer.outputs
        if not render:
            print('outputs', outputs)

        tiles = process_outputs(outputs)

        for x, y, id in tiles:
            if x == -1 and y == 0:
                score = id
                if score > 0:
                    num_blocks -= 1
                if not render:
                    print('Display score:', score, '- Remaining blocks:', num_blocks)
            if id == 3:
                x_paddle = x
            if id == 4:
                x_ball = x
                y_ball = y

        if not render:
            print('Ball at (%0d, %0d), Paddle at x=%0d' % (x_ball, y_ball, x_paddle))
        if render:
            render_screen(tiles)

        # Move paddle towards ball
        if x_ball > x_paddle:
            inputs.append(1)
        elif x_ball < x_paddle:
            inputs.append(-1)
        else:
            inputs.append(0)

        if num_blocks <= 0:
            break

    if not render:
        print('Final score:', score)
    assert score == 17336

