import sys
sys.path.append('../..')
import util


def count_increases(nums):
    last = None
    incs = 0
    for num in nums:
        if last is not None and num > last:
            incs += 1
        last = num
    return incs


def count_3sum_increases(nums):
    sums = []
    for i in range(len(nums)):
        if i > 1:
            sums.append(sum(nums[i-2:i+1]))
    incs = count_increases(sums)
    return incs


test = '''
199
200
208
210
200
207
240
269
260
263
'''

with open('input.txt', 'r') as f:
    input = util.ints(f.read())
    # input = util.ints(test)

    result = count_increases(input)
    print('Part 1', result)
    assert(result == 1754)

    result = count_3sum_increases(input)
    print('Part 2', result)
    assert(result == 1789)
