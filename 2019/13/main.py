import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util
from collections import deque


def process_outputs(outputs):
    tiles = []
    tile = []
    i = 0
    for o in outputs:
        tile.append(o)
        if not (i+1) % 3:
            tiles.append(tile)
            tile = []
        i += 1
    # print(items)
    return tiles


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
        print('outputs', outputs)

        tiles = process_outputs(outputs)

        for x, y, id in tiles:
            if x == -1 and y == 0:
                score = id
                if score > 0:
                    num_blocks -= 1
                print('Display score:', score, '- Remaining blocks:', num_blocks)
            if id == 3:
                print('* Paddle at', x, y)
                xp = x
            if id == 4:
                print('Ball at', x, y)
                xb = x

        # Move paddle towards ball
        if xb > xp:
            inputs.append(1)
        elif xb < xp:
            inputs.append(-1)
        else:
            inputs.append(0)

        if num_blocks <= 0:
            break

    print('Final score:', score)
    assert score == 17336

