import sys
sys.path.append('../..')
import util


def process(input, require_all):
    groups = input.split('\n\n')
    return sum([process_group(x, require_all) for x in groups])


def process_group(group, require_all):
    lines = group.strip().splitlines()
    ans = {}
    for line in lines:
        for char in line:
            if char not in ans:
                ans[char] = 0
            ans[char] += 1
    # print(ans, '==', len(lines))
    if require_all:
        num_ans = sum([1 for k,v in ans.items() if v == len(lines)])
    else:
        num_ans = len(ans.keys())
    return num_ans


def test():
    test_input = '''
abc

a
b
c

ab
ac

a
a
a
a

b
'''
    assert(process(test_input, require_all=False) == 11)
    assert(process(test_input, require_all=True) == 6)

test()


with open('input.txt', 'r') as f:
    input = f.read().strip()
    cnt = process(input, require_all=False)
    print('Part 1:', cnt)
    cnt = process(input, require_all=True)
    print('Part 2:', cnt)
