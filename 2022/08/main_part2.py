import sys
sys.path.append('../..')
import util


def process(input):
    grid = util.text_to_grid(input.strip())
    max_score = 0
    for y, row in enumerate(grid):
        for x, _val in enumerate(row):
             score = get_score(grid, x, y)
             if score > max_score:
                max_score = score
    return max_score


def get_score(grid, x, y):
    if x == 0 or y == 0 or x == len(grid[0])-1 or y == len(grid)-1:
        return True
    
    up = reversed(range(0,y))
    down = range(y+1,len(grid))
    left = reversed(range(0,x))
    right = range(x+1,len(grid[0]))

    total_score = (
        get_num_visible_y(grid, x, y, up) *
        get_num_visible_y(grid, x, y, down) * 
        get_num_visible_x(grid, x, y, left) * 
        get_num_visible_x(grid, x, y, right)
    )
    return total_score


def get_num_visible_y(grid, x, y, test_range):
    num = 0
    for y0 in test_range:
        num += 1
        if grid[y0][x] >= grid[y][x]:
            break
    return num

def get_num_visible_x(grid, x, y, test_range):
    num = 0
    for x0 in test_range:
        num += 1
        if grid[y][x0] >= grid[y][x]:
            break
    return num

def test():
    test_input = '''
30373
25512
65332
33549
35390
    '''
    grid = util.text_to_grid(test_input.strip())
    assert(get_score(grid, 2, 1) == 4)
    assert(process(test_input) == 8)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 2:', val)
    assert(val == 496125)
