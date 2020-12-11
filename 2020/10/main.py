import sys
sys.path.append('../..')
import util
import math


def connect_all(input):
    adapters = util.ints(input)
    adapters.append(max(adapters) + 3)
    adapters = sorted(adapters)
    print(adapters)

    deltas = {}
    source = 0
    for adapter in adapters:
        diff = adapter - source
        source = adapter
        if diff not in deltas:
            deltas[diff] = 0
        deltas[diff] += 1
    # print(deltas)
    return deltas


def num_arrangements(input):
    adapters = util.ints(input)
    adapters.append(max(adapters) + 3)
    adapters = sorted(adapters)

    num_valid = []
    source = 0
    i = 0
    while i < len(adapters):
        adapter = adapters[i]
        num = 0
        last_source = source
        for j in range(1,4):
            test_adapter = last_source + j
            if test_adapter in adapters:
                num += 1
                source = test_adapter
                i = adapters.index(test_adapter) + 1
        num_valid.append(num)
    print(num_valid)

    # total = sum([math.factorial(x) for x in num_valid])
    total = 0
    for n in num_valid:
        if n > 1:
            total += math.factorial(n)
    print(total)
    return total

    # total = 0
    # group = 1
    # for num in num_valid:
    #     if num > 1:
    #         group = group * num
    #     if num == 1:
    #         if group > 1:
    #             total += group
    #         group = 1
    # print('total', total)

    return num_valid
    exit(0)

    num_variants = 1
    source = 0
    visited = set()
    for adapter in adapters:
        print(adapter)
        if adapter in visited:
            print('  vis', adapter)
            continue
        num_valid = 0
        for i in range(1,4):
            # print(source, '->', i, source+i)
            if source + i in adapters:
                num_valid += 1
                visited.add(source + i)
        print(source, '->', num_valid, ':', visited)
        source = adapter
        visited.add(adapter)
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
