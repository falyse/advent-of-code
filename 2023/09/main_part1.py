import sys
sys.path.append('../..')
import util


def process(input):
    lines = input.strip().splitlines()
    histories = [util.ints(x) for x in lines]
    print()
    print(histories)
    total = 0
    for h in histories:
        val = extrapolate(h)
        print('Next val', val)
        total += val
    print('Total', total)
    return total

def diff_list(nums):
    diff_list = []
    for x, y in zip(nums[0::], nums[1::]):
        diff_list.append(y-x)
    return diff_list

def extrapolate(nums):
    lists = [nums]
    while not all([x == 0 for x in nums]):
        nums = diff_list(nums)
        lists.append(nums)
    print(lists)
    
    lists = list(reversed(lists))
    c = lists.copy()

    for i, nums in enumerate(lists):
        print(i, nums)
        if i == 0:
            val = 0
        else:
            val = nums[-1] + c[i-1][-1]
        if i == len(lists)-1:
            return val
        c[i].append(val)


def test():
    assert(diff_list([0,3,6,9,12,15]) == [3,3,3,3,3])
    assert(extrapolate([0,3,6,9,12,15]) == 18)

    assert(diff_list([0,-3,-6,-9,-12,-15]) == [-3,-3,-3,-3,-3])
    assert(extrapolate([0,-3,-6,-9,-12,-15]) == -18)

    test_input = '''
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45

    '''
    assert(process(test_input) == 114)

test()
# exit(0)


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Result:', val)
