import sys
sys.path.append('../..')
import util


def process(input, repeat):
    space = text_to_space(input)
    space_to_text(space)
    for i in range(repeat):
        space = simulate(space)
        print('Iteration', i)
        space_to_text(space)
    num_active = len([x for x in space.values() if x == '#'])
    return num_active


def text_to_space(input):
    space = {}
    w = 0
    z = 0
    y = 0
    for line in input.strip().splitlines():
        x = 0
        for char in line:
            space[(x,y,z,w)] = char
            x += 1
        y += 1
    return space


def space_to_text(space):
    x_values, y_values, z_values, w_values = get_coord_sets(space)
    for w in w_values:
        for z in z_values:
            print('z=%0d, w=%0d' % (z, w))
            for y in y_values:
                line = ''
                for x in x_values:
                    loc = (x,y,z,w)
                    if loc in space:
                        line += space[loc]
                    else:
                        line += '.'
                print(line)
            print()


def get_coord_sets(space, extend=False):
    x_values = get_coord_set(space, 0, extend)
    y_values = get_coord_set(space, 1, extend)
    z_values = get_coord_set(space, 2, extend)
    w_values = get_coord_set(space, 3, extend)
    return x_values, y_values, z_values, w_values


def get_coord_set(space, dim, extend):
    values = set([k[dim] for k in space.keys()])
    if extend:
        values.add(min(values)-1)
        values.add(max(values)+1)
    return sorted(values)


def simulate(space):
    new_space = space.copy()
    x_values, y_values, z_values, w_values = get_coord_sets(space, extend=True)
    for w in w_values:
        for z in z_values:
            for y in y_values:
                for x in x_values:
                    loc = (x,y,z,w)
                    if loc in space:
                        char = space[loc]
                    else:
                        char = '.'
                    # new_space[loc] = char

                    num_adjacent = grid_count_adjacent(space, loc, '#')
                    if char == '#' and num_adjacent not in [2, 3]:
                        new_space[loc] = '.'
                    if char == '.' and num_adjacent == 3:
                        new_space[loc] = '#'
    return new_space


def grid_count_adjacent(grid, loc, value):
    x, y, z, w = loc
    cnt = 0
    for dw in range(-1,2):
        for dz in range(-1,2):
            for dy in range(-1,2):
                for dx in range(-1,2):
                    if dx == 0 and dy == 0 and dz == 0 and dw == 0:
                        continue
                    w_test = w + dw
                    z_test = z + dz
                    y_test = y + dy
                    x_test = x + dx
                    loc_test = x_test, y_test, z_test, w_test
                    if loc_test in grid and grid[loc_test] == value:
                        cnt += 1
    return cnt


def test():
    test_input = '''
.#.
..#
###
'''
    assert(process(test_input, 6) == 848)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input, 6)
    print('Part 2:', val)
