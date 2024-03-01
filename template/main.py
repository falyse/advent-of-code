import sys
sys.path.append('../..')
import util


def process_part1(input):
    return 0


def process_part2(input):
    return 0


def test():
    test_input = '''
    '''
    assert(process_part1(test_input) == )
    # assert(process_part2(test_input) == )

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process_part1(input)
    print('Part 1:', val)
    val = process_part2(input)
    print('Part 2:', val)
