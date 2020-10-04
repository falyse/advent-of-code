import sys
sys.path.append('..')
import util

def run(screen, input):
    for cmd in input.strip().splitlines():
        print(cmd)
        if 'rect' in cmd:
            dims = cmd.split()[1]
            a, b = map(int, dims.split('x'))
            screen = rect_cmd(screen, a, b)
        else:
            dims = cmd.split('=')[1]
            a, b = map(int, dims.split(' by '))
            if 'row' in cmd:
                screen = rotate_row_cmd(screen, a, b)
            else:
                screen = rotate_col_cmd(screen, a, b)
    print(util.grid_to_text(screen))
    return screen

def rect_cmd(screen, a, b):
    for x in range(a):
        for y in range(b):
            screen[y][x] = '#'
    return screen

def rotate_row_cmd(screen, a, b):
    row = screen[a]
    screen[a] = util.rotate_list(row, b, 'right')
    return screen

def rotate_col_cmd(screen, a, b):
    col = []
    for row in screen:
        col.append(row[a])
    col = util.rotate_list(col, b, 'right')
    for i, row in enumerate(screen):
        row[a] = col[i]
    return screen


def test():
    screen = util.make_grid(3, 7, fill='.')

    screen = run(screen, 'rect 3x2')
    assert util.grid_to_text(screen) == r"""
###....
###....
.......""".strip()

    screen = run(screen, 'rotate column x=1 by 1')
    assert util.grid_to_text(screen) == r"""
#.#....
###....
.#.....""".strip()

    screen = run(screen, 'rotate row y=0 by 4')
    assert util.grid_to_text(screen) == r"""
....#.#
###....
.#.....""".strip()

    screen = run(screen, 'rotate column x=1 by 1')
    assert util.grid_to_text(screen) == r"""
.#..#.#
#.#....
.#.....""".strip()

test()


with open('input.txt', 'r') as f:
    input = f.read()
    screen = util.make_grid(6, 50, fill='.')
    screen = run(screen, input)
    cnt = util.grid_count(screen, '#')
    print('Part 1 count:', cnt)

    render = util.grid_to_text(screen, {'.': util.PIXEL_WHITE})
    #FIXME - PIXEL_BLACK render size looks bad
    print(render)

