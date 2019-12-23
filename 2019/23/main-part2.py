import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util


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

    nat_packet = None
    nat_prev = None
    nat_sent = {}
    while True:
        idle = True
        for i, computer in enumerate(computers):
            if len(inputs[i]) == 0:
                inputs[i].append(-1)
                # pass
            else:
                idle = False
            computer.execute()
            output = computer.outputs
            while len(output) > 2:
                addr, x, y = output[0:3]
                output = output[3:]
                # print('Computer', i, 'sent packet', addr, x, y)
                idle = False
                if addr == 255:
                    # print('NAT packet', x, y)
                    nat_packet = x, y
                else:
                    inputs[addr].extend([x, y])
            computer.reset_outputs()
        if idle and nat_packet is not None:
            print('Idle state', nat_packet)
            x, y = nat_packet
            inputs[0].extend([x, y])
            if nat_prev is not None and nat_prev == nat_packet:
                print('Duplicate y', y)
                exit(0)
            nat_prev = nat_packet
