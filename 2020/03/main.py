import sys
sys.path.append('../..')
import util


def count_trees(input, dir):
    input = input.strip()
    grid = util.text_to_grid(input)
    y_size = len(grid)
    x_size = len(grid[0])

    num_trees = 0
    loc = (0, 0)
    while True:
        loc = util.tuple_add(loc, dir)
        # Stop after reaching the bottom
        if loc[1] >= y_size:
            break
        # Loop around at the horizontal edge
        if loc[0] >= x_size:
            loc = (loc[0] - x_size, loc[1])
        is_tree = grid[loc[1]][loc[0]] == '#'
        print('loc', loc, ':', is_tree)
        if is_tree:
            num_trees += 1

    return num_trees


def test():
    assert(count_trees('''
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
''', (3, 1)) == 7)


test()


with open('input.txt', 'r') as f:
    input = f.read().strip()
    num = count_trees(input, (3, 1))
    print('Part 1', num)
    assert(num == 184)

    dirs = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    mult = 1
    for dir in dirs:
        num = count_trees(input, dir)
        mult *= num
    print('Part 2', mult)
    assert(mult == 2431272960)

