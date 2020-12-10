import sys
sys.path.append('../..')
import util


def connect_all(input):
    adapters = util.ints(input)
    adapters.append(max(adapters) + 3)
    adapters = sorted(adapters)
    print(adapters)

    deltas = {}
    jolt = 0
    for adapter in adapters:
        diff = adapter - jolt
        jolt = adapter
        if diff not in deltas:
            deltas[diff] = 0
        deltas[diff] += 1
    print(deltas)
    return deltas


def num_arrangements(input):
    adapters = util.ints(input)
    adapters.append(max(adapters) + 3)
    adapters = sorted(adapters)

    num_variants = 1
    jolt = 0
    visited = set()
    for adapter in adapters:
        if adapter in visited:
            continue
        num_valid = 0
        for i in range(1,4):
            # print(jolt, '->', i, jolt+i)
            if jolt + i in adapters:
                num_valid += 1
                visited.add(jolt + i)
        print(jolt, '->', num_valid, ':', visited)
        jolt = adapter
        if num_valid > 1:
            num_variants += num_valid
    print(num_variants)
    # return num_variants


def test():
    test_input = '''
16
10
15
5
1
11
7
19
6
12
4
'''
    assert(connect_all(test_input) == {1: 7, 3: 5})
    assert(num_arrangements(test_input) == 8)

    test_input = '''
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
'''
    assert(connect_all(test_input) == {1: 22, 3: 10})
    assert(num_arrangements(test_input) == 19208)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    deltas = connect_all(input)
    print('Part 1:', deltas[1] * deltas[3])
