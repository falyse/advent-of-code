import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util
from collections import deque


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)

    program_code[0] = 2
    inputs = deque()
    computer.initialize(program_code, inputs)

    j = 0
    dir = 1
    num_blocks = 344
    first = True
    last_paddle = (0,0)
    last_ball = (0,0)
    score = 0
    while True:
        computer.reset_outputs()
        inputs.append(dir)
        print('inputs', inputs)
        done = computer.execute()
        outputs = computer.outputs
        print('outputs', outputs)

        items = []
        item = []
        i = 0
        for o in outputs:
            item.append(o)
            if not (i+1) % 3:
                items.append(item)
                item = []
            i += 1
        # print(items)

        for x, y, id in items:
            if x == -1 and y == 0:
                print('Display score:', id)
                score = id
            if id == 0 and not first and (x,y) != last_ball and (x,y) != last_paddle:
                print('# Destroyed block at', x, y)
                num_blocks -= 1
            if id == 3:
                print('* Paddle at', x, y)
                last_paddle = (x,y)
                xp = x
            if id == 4:
                print('Ball at', x, y)
                last_ball = (x,y)
                xb = x
        first = False
        if xb > xp:
            dir = 1
            # inputs.append(1)
        elif xb < xp:
            dir = -1
            # inputs.append(-1)
        else:
            dir = 0
            # inputs.append(0)

        print('Num blocks:', num_blocks)
        if num_blocks <= 0:
            assert score == 17336
            exit(0)

