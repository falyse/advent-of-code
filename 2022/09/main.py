import sys
sys.path.append('../..')
import util


dir_map = {
    'R': 'E',
    'L': 'W',
    'U': 'N',
    'D': 'S',
}


def process(input, num_knots):
    lines = input.strip().splitlines()
    knots = [(0,0) for k in range(num_knots)]
    visited = set([knots[-1]])
    for line in lines:
        dir, num = line.split(' ')
        dir = dir_map[dir]
        num = int(num)
        # print(dir, num)
        for i in range(num):
            knots[0] = util.coord_move(knots[0], dir)
            for k in range(1, len(knots)):
                knots[k] = move_tail(knots[k-1], knots[k])
            visited.add(knots[-1])
            # print(knots)
    # print(visited)
    return len(visited)


def move_tail(h, t):
    diff = util.tuple_sub(h, t)
    if tail_is_adjacent(h, t):
        return t
    # print(diff)

    if diff[0] <= -2 and diff[1] == 0:
        return (t[0] - 1, t[1])
    if diff[0] >= 2 and diff[1] == 0:
        return (t[0] + 1, t[1])
    if diff[1] <= -2 and diff[0] == 0:
        return (t[0], t[1] - 1)
    if diff[1] >= 2 and diff[0] == 0:
        return (t[0], t[1] + 1)

    if diff[0] <= -1 and diff[1] <= -1:
        t = (t[0] - 1, t[1] - 1)
    if diff[0] <= -1 and diff[1] >= 1:
        t = (t[0] - 1, t[1] + 1)
    if diff[0] >= 1 and diff[1] <= -1:
        t = (t[0] + 1, t[1] - 1)
    if diff[0] >= 1 and diff[1] >= 1:
        t = (t[0] + 1, t[1] + 1)
    
    assert(tail_is_adjacent(h, t))

    return t


def tail_is_adjacent(h, t):
    diff = util.tuple_sub(h, t)
    return abs(diff[0]) <= 1 and abs(diff[1]) <= 1  # diagonal counts as adjacent


def test():
    test_input = '''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
    '''
    assert(move_tail((4,2), (3,0)) == (4,1))
    assert(process(test_input, 2) == 13)
    assert(process(test_input, 10) == 1)

test()
# exit(1)


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input, 2)
    print('Part 1:', val)
    assert(val == 6354)

    val = process(input, 10)
    print('Part 2:', val)
    assert(val == 2651)
