import sys
sys.path.append('../..')
import util


def process(input):
    grid = util.text_to_grid_dict(input.strip())
    loc_s = util.grid_dict_locate_item(grid, 'S')
    loc_e = util.grid_dict_locate_item(grid, 'E')
    grid[loc_s] = 'a'
    grid[loc_e] = 'z'
    # Search from start location to end location
    paths = find_valid_paths(grid, loc_s, loc_e)
    return min(paths)


def find_valid_paths(grid, loc_s, loc_e):
    # BFS to find all valid paths from start to end location
    paths = []
    visited = {}
    queue = [{'loc': loc_s, 'steps': 0}]
    while len(queue) > 0:
        current = queue.pop()
        loc = current['loc']
        steps = current['steps']
        if loc not in visited or visited[loc] > steps:
            visited[loc] = steps

            # print('At loc', loc, 'in', steps, 'steps')
            # render(grid, loc)

            if loc == loc_e:
                # print('  Found end', loc_e, 'at', steps, 'steps')
                paths.append(steps)
            else:
                for dir in get_open_dirs(grid, loc):
                    # print('    Dir', dir)
                    move_loc = util.coord_move(loc, dir)
                    queue.append({'loc': move_loc, 'steps': steps+1})
    # print(paths)
    return paths


def get_open_dirs(grid, loc):
    opens = []
    cur_val = grid[loc]
    for dir in ['N', 'S', 'E', 'W']:
        next_loc = util.coord_move(loc, dir)
        val = grid.get(next_loc)
        if val is not None and ord(val) <= ord(cur_val) + 1:
            opens.append(dir)
    return opens


def render(grid, loc):
    grid = grid.copy()
    grid[loc] = '*'
    print(util.grid_dict_to_text(grid))


def test():
    test_input = '''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
    '''
    assert(process(test_input) == 31)

# test()
# exit(0)

with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
    assert(val == 420)
