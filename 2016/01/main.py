import sys
sys.path.append('..')
import util

def get_dist(input):
    loc = (0,0)
    dir = 'N'
    for i in input.split(', '):
        turn = i[0]
        steps = int(i[1:])
        dir = util.coord_turn(dir, turn)
        loc = util.coord_move(loc, dir, steps)
    return util.taxi_distance(loc)


def get_first_revisit_dist(input):
    loc = (0,0)
    dir = 'N'
    prev_locs = {loc: 1}
    for i in input.split(', '):
        turn = i[0]
        steps = int(i[1:])
        dir = util.coord_turn(dir, turn)
        for s in range(steps):
            loc = util.coord_move(loc, dir, 1)
            print('loc', loc)
            if loc in prev_locs:
                return util.taxi_distance(loc)
            else:
                prev_locs[loc] = 1
    return 0


def test1():
    assert get_dist('R2, L3') == 5
    assert get_dist('R2, R2, R2') == 2
    assert get_dist('R5, L5, R5, R3') == 12

def test2():
    assert get_first_revisit_dist('R8, R4, R4, R8') == 4


test1()
test2()
#exit(0)


with open('input.txt', 'r') as f:
    input = f.read()
    dist = get_dist(input)
    print('Part 1 dist', dist)
    dist = get_first_revisit_dist(input)
    print('Part 2 dist', dist)

