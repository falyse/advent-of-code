import sys
sys.path.append('../..')
import util


def process(input):
    grid = util.text_to_grid(input.strip())
    visible = 0
    for y, row in enumerate(grid):
        for x, _val in enumerate(row):
            if is_visible(grid, x, y):
                visible += 1
    return visible


def is_visible(grid, x, y):
    if x == 0 or y == 0 or x == len(grid[0])-1 or y == len(grid)-1:
        return True
    
    up = range(0,y)
    down = range(y+1,len(grid))
    left = range(0,x)
    right = range(x+1,len(grid[0]))

    if all([grid[y0][x] < grid[y][x] for y0 in up]):
        return True
    if all([grid[y0][x] < grid[y][x] for y0 in down]):
        return True
    if all([grid[y][x0] < grid[y][x] for x0 in left]):
        return True
    if all([grid[y][x0] < grid[y][x] for x0 in right]):
        return True

    return False


def test():
    test_input = '''
30373
25512
65332
33549
35390
    '''
    assert(process(test_input) == 21)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
    assert(val == 1538)
