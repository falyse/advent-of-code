import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util


def test():
    pass

test()



with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]

    computers = []
    inputs = []
    outputs = []
    for i in range(50):
        computer = IntcodeComputer(debug=False)
        computers.append(computer)
        input = deque([i])
        inputs.append(input)
        computer.initialize(program_code, input)

    while True:
        for i, computer in enumerate(computers):
            if len(inputs[i]) == 0:
                inputs[i].append(-1)
            computer.execute()
            output = computer.outputs
            while len(output) > 2:
                addr, x, y = output[0:3]
                output = output[3:]
                print('Computer', i, 'sent packet', addr, x, y)
                if addr == 255:
                    print('Y at 255', y)
                    exit(0)
                inputs[addr].extend([x, y])
