import sys
sys.path.append('../..')
import util
import re


def process(input):
    lines = input.strip().splitlines()
    nums = [re.findall(r"-?\d", x) for x in lines]
    total = 0
    for n in nums:
        if len(n) == 1:
            val = n[0] + n[0]
        else:
            val = n[0] + n[-1]
        print(val)
        total += int(val)
    return total


def test():
    test_input = '''
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
    '''
    assert(process(test_input) == 142)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)