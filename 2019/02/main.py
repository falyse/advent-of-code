import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)

    # Part 1
    program_code[1] = 12
    program_code[2] = 2
    output = computer.run(program_code)
    print('Part 1 output', output)
    assert output == 3166704

    # Part 2
    goal = 19690720
    for noun in range(0,100):
        for verb in range(0,100):
            program_code[1] = noun
            program_code[2] = verb
            output = computer.run(program_code)
            if output == goal:
                result = 100*noun+verb
                print('Part 2 result', result)
                assert result == 8018
                break
