import sys
sys.path.append('../..')
import util
import json
import functools


def process(input):
    pairs = input.strip().split('\n\n')
    sum = 0
    for i, pair in enumerate(pairs):
        index = i + 1
        # print()
        # print('== Pair %0d ==' % index)
        l, r = [json.loads(x) for x in pair.splitlines()]
        if compare(l, r) == -1:
            sum += index
    return sum


def process_sort(input):
    lines = sort(input)
    mult = 1
    for i, line in enumerate(lines):
        if line == [[2]] or line == [[6]]:
            mult *= (i+1)
    return mult


def sort(input):
    input += '[[2]]\n[[6]]'
    lines = input.strip().splitlines()
    lines = [json.loads(x) for x in lines if x != '']
    # print('\n'.join([str(x) for x in lines]))
    lines = sorted(lines, key=functools.cmp_to_key(compare))
    # print('\n'.join([str(x) for x in lines]))
    return lines


def compare(l, r, prefix=''):
    # print(prefix, '- Compare', l, 'vs', r)
    prefix += '  '
    if type(l) != list and type(r) != list:
        if int(l) < int(r):
            # print(prefix, '- Left side is smaller, so inputs are in the right order')
            return -1
        if int(l) > int(r):
            # print(prefix, '- Right side is smaller, so inputs are NOT in the right order')
            return 1
        return 0
    elif type(l) == list and type(r) == list:
        max_len = max([len(l), len(r)])
        for i in range(max_len):
            if i >= len(l):
                # print(prefix, '- Left ran out of items, so inputs are in the right order')
                return -1
            if i >= len(r):
                # print(prefix, '- Right ran out of items, so inputs are NOT in the right order')
                return 1
            ret = compare(l[i], r[i], prefix)
            if ret != 0:
                return ret
    else:
        if type(l) == list:
            ret = compare(l, [r], prefix)
        else:
            ret = compare([l], r, prefix)
        if ret != 0:
            return ret
    return 0

def test():
    test_input = '''
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
    '''

    assert(process(test_input) == 13)
    assert(process_sort(test_input) == 140)

test()


with open('input.txt', 'r') as f:
    input = f.read()

    val = process(input)
    print('Part 1:', val)
    assert(val == 6428)

    val = process_sort(input)
    print('Part 2:', val)
    assert(val == 22464)

