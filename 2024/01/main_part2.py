import sys
sys.path.append('../..')
import util
import pprint
import re


def process(input):
    l1, l2 = get_lists(input)
    # l1 = sorted(l1)
    # l2 = sorted(l2)
    print(l1)
    print(l2)

    d2 = {}
    for b in l2:
        if b not in d2:
            d2[b] = 1
        else:
            d2[b] += 1
    print(d2)

    dist = 0
    for a in l1:
        s = d2.get(a, 0)
        print(a, s)
        dist += a * s
    print(dist)
    return dist

def get_lists(input):
    l1 = []
    l2 = []
    for line in input.strip().splitlines():
        a, b = util.ints(line)
        l1.append(a)
        l2.append(b)
    # print(l1)
    # print(l2)
    return l1, l2


def test():
    test_input = '''
3   4
4   3
2   5
1   3
3   9
3   3
    '''
    assert(process(test_input) == 31)

test()
# exit(0)


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 2:', val)
