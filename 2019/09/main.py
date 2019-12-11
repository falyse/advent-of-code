import sys
sys.path.append('../intcode')
from intcode import IntcodeComputer


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=True)

    # Part 1
    output = computer.run(program_code, 1)
    print('Part 1 output =', output)
    assert output == 3512778005

    # Part 2
    output = computer.run(program_code, 2)
    print('Part 2 output =', output)
    assert output == 35920
