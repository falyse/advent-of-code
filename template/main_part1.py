import sys
sys.path.append('../..')
import util
import pprint
import re


def process(input):
    lines = input.strip().splitlines()
    return


def test():
    test_input = '''
    '''
    assert(process(test_input) == )

test()
# exit(0)


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Result:', val)
