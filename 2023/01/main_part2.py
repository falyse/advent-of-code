import sys
sys.path.append('../..')
import util
import re


def process(input):
    input = preprocess(input)
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

def preprocess(input):
    d = {
        'twone': '21',
        'eightwo': '82',
        'eighthree': '83',
        'oneight': '18',
        'threeight': '38',
        'fiveight': '58',
        'nineight': '98',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }
    for k,v in d.items():
        input = input.replace(k, v)
    return input


def test():
    test_input = '''
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
    '''
    assert(process(test_input) == 281)
    assert(process('tzjfdrzvzfivejsv49eightwozmf') == 52)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 2:', val)