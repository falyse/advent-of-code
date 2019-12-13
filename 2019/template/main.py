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
# with open('test.txt', 'r') as f:
    input = f.readlines()
    # program_code = [int(x) for x in f.read().split(',')]
    # computer = IntcodeComputer(debug=False)
