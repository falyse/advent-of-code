import sys
sys.path.append('..')
import util

from itertools import permutations
import math
import copy


class Asteroid:
    def __init__(self, coords):
        self.coords = coords
        self.visible = []

    def __str__(self):
        return 'Asteroid at ' + str(self.coords)

    def set_path(self, dist, angle):
        self.dist = dist
        self.angle = angle

    def update_visible(self, others):
        self.visible = []
        all = []
        all_angles = set()
        # First, calculate the paths to all other asteroids
        for o in others:
            if o != self:
                dist, angle = self.get_path(self.coords, o.coords)
                oc = copy.copy(o)
                oc.set_path(dist, angle)
                all.append(oc)
                all_angles.add(angle)
        # Then, discard any asteroid that is not the closest in its path
        for angle in all_angles:
            matching = [a for a in all if a.angle == angle]
            min_match, _ = util.attribute_min_max(matching, 'angle')
            print('  can see', min_match, '(angle %0.2f)' % angle)
            self.visible.append(min_match)

    def get_path(self, coord0, coord1):
        dx = coord1[0] - coord0[0]
        dy = coord1[1] - coord0[1]
        dist = dx^2 + dy^2
        angle = math.atan2(-1*dy, dx) * 180/math.pi
        angle = (90 - angle) % 360  # Convert to clockwise angle
        return dist, angle

    def get_num_visible(self):
        return len(self.visible)


def render(grid):
    for line in grid:
        line = ['#' if x else '.' for x in line]
        print(''.join(line))

match = util.make_grid(10, 10, fill='.')


def vaporize_grid(grid, start_coords):
    x, y = start_coords
    coords = []
    combos = get_combos(len(grid[0]))
    for dx,dy in combos:
        coord = search_path(grid, x, y, dx, dy)
        if coord is not None:
            coords.append(coord)
    return coords

def process_grid(grid):
    cnts = util.make_grid(len(grid[0]), len(grid), fill=0)
    print(cnts)
    max = 0
    clist = []
    for y,line in enumerate(grid):
        for x,char in enumerate(line):
            cnt = 0
            coords = []
            if grid[y][x]:
                # print('Asteroid at', x, y)
                combos = get_combos(len(line))
                for dx,dy in combos:
                    coord = search_path(grid, x, y, dx, dy)
                    if coord is not None:
                        cnt += 1
                        coords.append(coord)
                cnts[y][x] = cnt
                if cnt > max:
                    max_coords = (x,y)
                    max = cnt
                    clist = coords.copy()
    print(cnts)
    return cnts, max_coords, max, clist

def get_combos(max):
    combos = get_offset_combos(1, 0)
    for i in range(max):
        combos.extend([(-1*i,-1), (-1*i,1), (i,-1), (i,1)])
        combos.extend([(-1,-1*i), (1,-1*i), (-1,i), (1,i)])
    for i in range(max):
        for j in range(2,max):
            if i > j and i % j:
                combos.extend([(-1*i,-1*j), (-1*i,j), (i,-1*j), (i,j)])
                combos.extend([(-1*j,-1*i), (j,-1*i), (-1*j,i), (j,i)])
    combos = set(combos)

    valid = []
    for x,y in combos:
        ok = True
        for i in range(2,max):
            if not x %i and not y % i:
                ok = False
        if ok:
            valid.append((x,y))
    valid = set(valid)
    return valid

def get_offset_combos(offset, mid):
    list1 = [-1*offset, mid, offset]
    combos = [zip(x,list1) for x in permutations(list1, len(list1))]
    combos = util.flatten(combos)
    combos = set(combos)
    if (0,0) in combos:
        combos.remove((0, 0))
    return list(combos)

def search_path(grid, x, y, delta_x, delta_y):
    debug = x == 11 and y == 13
    while True:
        x += delta_x
        y += delta_y
        if x < 0 or x >= len(grid[0]):
            break
        if y < 0 or y >= len(grid[0]):
            break
        if grid[y][x]:
            if debug and x == 11:
                print('  search path', delta_x, delta_y, 'found',  x, y, 'angle', get_angle((delta_x, delta_y)))
                # print(x,y)
                # match[y][x] = '#'
            # print('    found', x, y)
            return (x,y, get_angle((delta_x, delta_y)))
    return None

def get_angle(coord):
    x,y = coord
    angle = math.atan2(-1*y, x) * 180/math.pi
    # Convert to clockwise angle
    angle = (90 - angle) % 360
    return angle


def find_station_location(text):
    asteroids = []
    for y, line in enumerate(text.strip().splitlines()):
        for x, char in enumerate(line.strip()):
            if char == '#':
                asteroids.append(Asteroid((x,y)))
    for a in asteroids:
        print(a)
        a.update_visible(asteroids)
    best_a = None
    for a in asteroids:
        if best_a is None or a.get_num_visible() > best_a.get_num_visible():
            best_a = a
    # return best_a.coords, best_a.get_num_visible()
    return best_a


def test():
    assert get_angle((0,-1)) == 0
    assert get_angle((1,0)) == 90
    assert get_angle((0,1)) == 180
    assert get_angle((-1,0)) == 270
    assert get_angle((1,-1)) == 45

    a = find_station_location(r"""
        .#..#
        .....
        #####
        ....#
        ...##
        """)
    assert a.coords == (3, 4)
    assert a.get_num_visible() == 8

    a = find_station_location(r"""
        ......#.#.
        #..#.#....
        ..#######.
        .#.#.###..
        .#..#.....
        ..#....#.#
        #..#....#.
        .##.#..###
        ##...#..#.
        .#....####
        """)
    assert a.coords == (5, 8)
    assert a.get_num_visible() == 33

    a = find_station_location(r"""
        #.#...#.#.
        .###....#.
        .#....#...
        ##.#.#.#.#
        ....#.#.#.
        .##..###.#
        ..#...##..
        ..##....##
        ......#...
        .####.###.
        """)
    assert a.coords == (1, 2)
    assert a.get_num_visible() == 35

    a = find_station_location(r"""
        .#..#..###
        ####.###.#
        ....###.#.
        ..###.##.#
        ##.##.#.#.
        ....###..#
        ..#.#..#.#
        #..#.#.###
        .##...##.#
        .....#.#..
        """)
    assert a.coords == (6, 3)
    assert a.get_num_visible() == 41

    a = find_station_location(r"""
        .#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##
        """)
    assert a.coords == (11, 13)
    assert a.get_num_visible() == 210


test()

with open('input.txt', 'r') as f:
    # Part 1
    asteroid = find_station_location(f.read())
    max_visible = asteroid.get_num_visible()
    print('Max', max_visible, 'at', asteroid.coords)
    assert max_visible == 326

    # Part 2
    step_max = 200
    step = 0
    while True:
        sorted_coords = []
        coords = sorted(coords, key=lambda x: x[2])
        render(grid)
        for x,y,angle in coords:
            step += 1
            grid[y][x] = False
            print('Step', step, 'vaporized', x, y, 'angle', angle)
            if step == step_max:
                print('Reached step %0d: ' % step_max, x, y)
                value = x*100 + y
                print('  ', value)
                assert value == 1623
                exit(0)
        coords = vaporize_grid(grid, max_coords)


