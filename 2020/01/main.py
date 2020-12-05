import sys
sys.path.append('../..')
import util
import itertools
import numpy


def check_combos(input, num_selected):
    for nums in itertools.combinations(input, num_selected):
        if sum(nums) == 2020:
            return numpy.prod(nums)


with open('input.txt', 'r') as f:
    input = f.read().strip().splitlines()
    input = list(map(int, input))

    result = check_combos(input, 2)
    print('Part 1', result)
    assert(result == 902451)

    result = check_combos(input, 3)
    print('Part 2', result)
    assert(result == 85555470)
