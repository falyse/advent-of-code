import sys
sys.path.append('..')
import util
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
            min_match, _ = util.attribute_min_max(matching, 'dist')
            #print('  can see', min_match, '(angle %0.2f, dist %0.2f)' % (angle, min_match.dist))
            self.visible.append(min_match)

    def get_path(self, coord0, coord1):
        dx = coord1[0] - coord0[0]
        dy = coord1[1] - coord0[1]
        dist = dx**2 + dy**2
        angle = math.atan2(-1*dy, dx) * 180/math.pi
        angle = (90 - angle) % 360  # Convert to clockwise angle
        return dist, angle

    def get_num_visible(self):
        return len(self.visible)


def text_to_asteroids(text):
    asteroids = []
    for y, line in enumerate(text.strip().splitlines()):
        for x, char in enumerate(line.strip()):
            if char == '#':
                asteroids.append(Asteroid((x,y)))
    return asteroids


def find_station_location(asteroids):
    for a in asteroids:
        print(a)
        a.update_visible(asteroids)
    best_a = None
    for a in asteroids:
        if best_a is None or a.get_num_visible() > best_a.get_num_visible():
            best_a = a
    # return best_a.coords, best_a.get_num_visible()
    return best_a


def vaporize(all_asteroids, asteroid, step_max):
    step = 0
    while True:
        visible = asteroid.visible
        visible = sorted(visible, key=lambda x: x.angle)
        for v in visible:
            step += 1
            print('Step', step, 'vaporized', v)
            all_asteroids = [x for x in all_asteroids if x.coords != v.coords]
            if step == step_max:
                value = v.coords[0]*100 + v.coords[1]
                print('Reached step %0d: value' % step_max, value)
                return value
        asteroid.update_visible(all_asteroids)


def test1():
    all = text_to_asteroids(r"""
        .#..#
        .....
        #####
        ....#
        ...##
        """)
    a = find_station_location(all)
    assert a.coords == (3, 4)
    assert a.get_num_visible() == 8

    all = text_to_asteroids(r"""
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
    a = find_station_location(all)
    assert a.coords == (5, 8)
    assert a.get_num_visible() == 33

    all = text_to_asteroids(r"""
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
    a = find_station_location(all)
    assert a.coords == (1, 2)
    assert a.get_num_visible() == 35

    all = text_to_asteroids(r"""
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
    a = find_station_location(all)
    assert a.coords == (6, 3)
    assert a.get_num_visible() == 41

    all = text_to_asteroids(r"""
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
    a = find_station_location(all)
    assert a.coords == (11, 13)
    assert a.get_num_visible() == 210


def test2():
    all = text_to_asteroids(r"""
        .#....#####...#..
        ##...##.#####..##
        ##...#...#.#####.
        ..#.....#...###..
        ..#.#.....#....##
        """)
    a = find_station_location(all)
    assert a.coords == (8, 3)
    assert vaporize(all, a, 9) == 1501


# test1()
# test2()

with open('input.txt', 'r') as f:
    all_asteroids = text_to_asteroids(f.read())

    # Part 1
    asteroid = find_station_location(all_asteroids)
    max_visible = asteroid.get_num_visible()
    print('Max', max_visible, 'at', asteroid.coords)
    assert max_visible == 326

    # Part 2
    value = vaporize(all_asteroids, asteroid, 200)
    assert value == 1623

