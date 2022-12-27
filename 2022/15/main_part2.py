import sys
sys.path.append('../..')
import util


def process(input, max_coord):
    pairs = extract_pairs(input)
    grid = build_grid(pairs)
    dists = calc_dists(pairs)

    # x, y = search(grid, dists, max_coord)
    x, y = search_edges(grid, dists, max_coord)
    val = x * 4000000 + y
    print((x, y), '->', val)
    return val


def extract_pairs(input):
    lines = input.strip().splitlines()
    pairs = []
    for line in lines:
        s, b = line.split(':')
        (sx, sy) = util.ints(s)
        (bx, by) = util.ints(b)
        pairs.append(((sx, sy), (bx, by)))
    return pairs


def build_grid(pairs):
    grid = {}
    for s, b in pairs:
        grid[s] = 'S'
        grid[b] = 'B'
    # print(util.grid_dict_to_text(grid, empty_fill_char='.'))
    return grid


def calc_dists(pairs):
    dists = []
    for s, b in pairs:
        dist = util.taxi_distance(s, b)
        dists.append((s, dist))
    dists = sorted(dists, key=lambda x: x[1], reverse=True)
    return dists


def search(grid, dists, max_coord):
    for y in range(0, max_coord+1):
        for x in range(0, max_coord+1):
            any_inside = False
            if grid.get((x,y)) is None:
                for s, d in dists:
                    if util.taxi_distance((x,y), s) <= d:
                        any_inside = True
                        break
                if not any_inside:
                    return (x, y)


def search_edges(grid, dists, max_coord):
    for s, d in dists:
        edge = d + 1
        for dx in range(edge+1):
            dy = edge - dx
            loc = (s[0] + dx, s[1] + dy)
            if 0 < loc[0] < max_coord and 0 < loc[1] < max_coord:
                if check_loc(grid, dists, loc):
                    return loc
            loc = (s[0] - dx, s[1] - dy)
            if 0 < loc[0] < max_coord and 0 < loc[1] < max_coord:
                if check_loc(grid, dists, loc):
                    return loc
    print('ERROR')


def check_loc(grid, dists, loc):
    # print('Checking', loc)
    any_inside = False
    if grid.get(loc) is None:
        for s, d in dists:
            if util.taxi_distance(loc, s) <= d:
                any_inside = True
                break
        if not any_inside:
            return True
    return False


def test():
    test_input = '''
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
    '''
    assert(process(test_input, 20) == 56000011)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input, 4000000)
    print('Part 2:', val)
    assert(val == 10553942650264)
