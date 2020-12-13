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
                cnt = util.grid_count_adjacent(grid, (x, y), '#')
                if val == 'L' and cnt == 0:
                    new_grid[y][x] = '#'
                if val == '#' and cnt >= 4:
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


def test():
    test_cnt = '''
###.
#.#.
###L
'''
    grid = util.text_to_grid(test_cnt.strip())
    assert(util.grid_count_adjacent(grid, (1,1), '#') == 8)
    assert(util.grid_count_adjacent(grid, (0,0), '#') == 2)
    assert(util.grid_count_adjacent(grid, (2,1), '#') == 4)

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
#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
'''.strip())

    assert(process(test_input, 5) == '''
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
'''.strip())

    assert(run(test_input) == 37)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = run(input)
    print('Part 1:', val)
