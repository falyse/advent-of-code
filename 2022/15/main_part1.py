import sys
sys.path.append('../..')
import util


def process(input, y):
    pairs = extract_pairs(input)
    grid = build_grid(pairs)
    dists = calc_dists(pairs)
    # grid = map_coverage(grid, dists)
    # val = count_rows(grid, y)
    val = check_coverage(grid, dists, y)
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
    return dists


# def map_coverage(grid, dists):
#     for s, d in dists:
#         print(s, d)
#         for dx in range(-d, d+1):
#             for dy in range(-d, d+1):
#                 if util.taxi_distance((dx, dy)) <= d:
#                     coord = (s[0] + dx, s[1] + dy)
#                     if coord not in grid:
#                         grid[coord] = '#'
#     print(util.grid_dict_to_text(grid, empty_fill_char='.'))
#     return grid


# def count_rows(grid, y):
#     sum = 0
#     for loc in grid.keys():
#         if loc[1] == y and grid.get(loc) == '#':
#             sum += 1
#     print(sum)
#     return sum


def check_coverage(grid, dists, y):
    coord_min, coord_max = util.grid_dict_coord_range(grid)
    max_dist = 0
    for s, d in dists:
        if d > max_dist:
            max_dist = d
    sum = 0
    x_min, x_max = coord_min[0] - max_dist, coord_max[0] + max_dist + 1
    print('X range:', x_min, x_max)
    for x in range(x_min, x_max):
        any_inside = False
        for s, d in dists:
            if grid.get((x,y)) is None and util.taxi_distance((x,y), s) <= d:
                any_inside = True
        if any_inside:
            sum += 1
    print(sum)
    return sum


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
    assert(process(test_input, 10) == 26)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input, 2000000)
    print('Part 1:', val)
    assert(val == 5108096)
