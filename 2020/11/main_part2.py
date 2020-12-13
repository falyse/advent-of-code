import sys
sys.path.append('../..')
import util
import copy


def process(input, rounds):
    grid = util.text_to_grid(input.strip())
    for _ in range(rounds):
        new_grid = copy.deepcopy(grid)
        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                cnt = grid_count_visible(grid, (x, y))
                if val == 'L' and cnt == 0:
                    new_grid[y][x] = '#'
                if val == '#' and cnt >= 5:
                    new_grid[y][x] = 'L'
        grid = copy.deepcopy(new_grid)
    text = util.grid_to_text(grid)
    # print(text)
    # print()
    return text


def run(state):
    state = state.strip()
    round = 0
    while True:
        round += 1
        print('Round:', round)
        next_state = process(state, 1)
        if state == next_state:
            return state.count('#')
        state = next_state


def grid_count_visible(grid, loc):
    x, y = loc
    cnt = 0
    for dy in range(-1,2):
        for dx in range(-1,2):
            if dx == dy == 0:
                continue
            y_test = y + dy
            x_test = x + dx
            while (y_test >= 0 and y_test < len(grid) and
                   x_test >= 0 and x_test < len(grid[y])):
                if grid[y_test][x_test] != '.':
                    if grid[y_test][x_test] == '#':
                        cnt += 1
                    break
                y_test += dy
                x_test += dx
    return cnt


def test_visible():
    test_visible = '''
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
'''
    grid = util.text_to_grid(test_visible.strip())
    assert(grid_count_visible(grid, (3,4)) == 8)

    test_visible = '''
.............
.L.L.#.#.#.#.
.............
'''
    grid = util.text_to_grid(test_visible.strip())
    assert(grid_count_visible(grid, (1,1)) == 0)

    test_visible = '''
.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
'''
    grid = util.text_to_grid(test_visible.strip())
    assert(grid_count_visible(grid, (3,3)) == 0)
    exit(0)


def test():
    test_input = '''
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
'''

    assert(process(test_input, 1) == '''
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
'''.strip())

    assert(process(test_input, 2) == '''
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
'''.strip())

    assert(process(test_input, 3) == '''
#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
'''.strip())

    assert(run(test_input) == 26)
    exit(0)

# test_visible()
# test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = run(input)
    print('Part 2:', val)
