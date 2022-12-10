import sys
sys.path.append('../..')
import util


def process(input, count):
    nums = util.ints(input)
    ages = {}
    last_num = None
    for i, num in enumerate(nums):
        ages[num] = [i+1]
        last_num = num
    print(ages)
    for i in range(len(nums)+1, count+1):
        if last_num in ages and len(ages[last_num]) > 1:
            num = ages[last_num][0] - ages[last_num][1]
        else:
            num = 0
        if num in ages:
            ages[num] = [i, ages[num][0]]
        else:
            ages[num] = [i]
        # if i%1000000 == 0 or i == count+1:
        #     print('Turn', i, ':', num)
        #     print(ages)
        last_num = num
    return last_num


def test():
    test_input = '0,3,6'
    assert(process(test_input, 2020) == 436)
    assert(process(test_input, 30000000) == 175594)
    exit(0)

# test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input, 2020)
    print('Part 1:', val)
    val = process(input, 30000000)
    print('Part 2:', val)
