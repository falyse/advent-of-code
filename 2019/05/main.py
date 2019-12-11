import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util

with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)

    # Part 1
    computer.run(program_code, 1)  # Part 1
    output = computer.outputs[-1]
    print('Part 1 output =', output)
    assert output == 15508323

    # Part 2
    output = computer.run(program_code, 5)  # Part 2
    print('Part 2 output =', output)
    assert output == 9006327

