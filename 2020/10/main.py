import sys
sys.path.append('../..')
import util

cache = {}

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
    adapters = adapters + [max(adapters) + 3]
    adapters = sorted(adapters)
    print(adapters)

    global cache
    cache = {}
    num_paths = get_valid_paths(adapters, 0)
    print('total', num_paths)
    return num_paths


def get_valid_paths(adapters, start):
    if start in cache:
        return cache[start]
    if start == adapters[-1]:
        return 1
    num = 0
    for j in range(1,4):
        if start+j in adapters:
            num += get_valid_paths(adapters, start+j)
    cache[start] = num
    return num


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
    num_paths = num_arrangements(input)
    print('Part 2:', num_paths)
