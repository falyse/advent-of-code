import sys
sys.path.append('../..')
import util


def process_part1(input):
    lines = input.strip().splitlines()
    sum = 0
    for line in lines:
        nums = list(map(int, line.split()))
        sum += max(nums) - min(nums)
    return sum

def process_part2(input):
    lines = input.strip().splitlines()
    sum = 0
    for line in lines:
        nums = list(map(int, line.split()))
        for i, num in enumerate(nums):
            for j, other_num in enumerate(nums):
                if i != j and num % other_num == 0:
                    sum += num // other_num
                    break
    return sum


def test():
    test_input = '''
5 1 9 5
7 5 3
2 4 6 8
    '''
    assert(process_part1(test_input) == 18)
    test_input = '''
5 9 2 8
9 4 7 3
3 8 6 5
    '''
    assert(process_part2(test_input) == 9)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process_part1(input)
    print('Part 1:', val)
    val = process_part2(input)
    print('Part 2:', val)
