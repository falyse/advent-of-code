import sys
sys.path.append('../..')
import util
import random
import itertools


def is_valid(preamble, number):
    num_combos = itertools.combinations(preamble, 2)
    for nums in num_combos:
        if number == sum(nums) and nums[0] != nums[1]:
            return True
    return False


def process(input, preamble_len):
    preamble = []
    for num in util.ints(input):
        if len(preamble) == preamble_len:
            # print(preamble, num)
            if not is_valid(preamble, num):
                return num
            preamble = preamble[1:]
        preamble.append(num)


def find_contig(input, target_sum):
    current_set = []
    input = util.ints(input)
    for i_start in range(0, len(input)):
        for i_end in range(i_start, len(input)):
            # print(i_start, i_end)
            nums = input[i_start:i_end]
            # print(nums, sum(nums))
            if sum(nums) == target_sum:
                return min(nums) + max(nums)


def test():
    preamble = list(range(1,26))
    random.shuffle(preamble)
    assert(is_valid(preamble, 26) is True)
    assert(is_valid(preamble, 49) is True)
    assert(is_valid(preamble, 100) is False)
    assert(is_valid(preamble, 50) is False)

    test_input = '''
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
'''
    assert(process(test_input, 5) == 127)
    assert(find_contig(test_input, 127) == 62)


test()


with open('input.txt', 'r') as f:
    input = f.read()
    num = process(input, 25)
    print('Part 1:', num)
    val = find_contig(input, num)
    print('Part 2:', val)
