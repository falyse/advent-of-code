import sys
sys.path.append('../..')
import util


def process(input):
    lines = input.strip().splitlines()
    num_full = 0
    num_any = 0
    for line in lines:
        a, b = [[int(x) for x in y.split('-')] for y in line.split(',')]
        if fully_contains(a, b) or fully_contains(b, a):
            num_full += 1
        if any_overlap(a, b) or any_overlap(b, a):
            num_any += 1
    return num_full, num_any


def fully_contains(a, b):
    return a[0] <= b[0] and a[1] >= b[1]


def any_overlap(a, b):
    return a[0] <= b[0] and a[1] >= b[0]


def test():
    test_input = '''
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
    '''
    assert(process(test_input) == (2, 4))

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val1, val2 = process(input)
    print('Part 1:', val1)
    assert(val1 == 580)
    print('Part 2:', val2)
    assert(val2 == 895)