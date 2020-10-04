import sys
sys.path.append('../..')
import util

def is_triangle(sides):
    if sides[0] + sides[1] <= sides[2]:
        return False
    if sides[1] + sides[2] <= sides[0]:
        return False
    if sides[0] + sides[2] <= sides[1]:
        return False
    return True


def count_triangles_horizontal(input):
    cnt = 0
    for line in input.splitlines():
        sides = util.positive_ints(line)
        print('sides:', sides)
        if is_triangle(sides):
            cnt += 1
    return cnt


def count_triangles_vertical(input):
    lines = input.strip().splitlines()
    cnt = 0
    for i in range(0, len(lines), 3):
        cols = []
        cols.append(util.positive_ints(lines[i]))
        cols.append(util.positive_ints(lines[i+1]))
        cols.append(util.positive_ints(lines[i+2]))
        for j in range(3):
            sides = [cols[0][j], cols[1][j], cols[2][j]]
            print('sides', j, ':', sides)
            if is_triangle(sides):
                cnt += 1
    return cnt


def test():
    assert is_triangle([5, 10, 25]) is False
    assert count_triangles_vertical(r"""
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603""")

test()


with open('input.txt', 'r') as f:
    input = f.read().strip()
    cnt = count_triangles_horizontal(input)
    print('Part 1 count:', cnt)
    cnt = count_triangles_vertical(input)
    print('Part 2 count:', cnt)

