import sys
sys.path.append('../..')
import util
import time
start_time = time.time()


def process(input, steps):
    print('Steps', steps)
    grid = util.text_to_grid_dict(input.strip())
    loc = util.grid_dict_locate_item(grid, 'S')
    grid[loc] = '.'
    # util.render_grid(grid, loc)
    endpoints = find_all_endpoints(grid, loc, steps, blockers=['#'])
    # print(endpoints)
    val = len(endpoints)
    print('Result:', val)
    return val


def find_all_endpoints(grid, loc, steps, blockers=[]):
    '''Find all endpoints that are reachable from a start location in specified number of steps'''
    memo = {}
    info = {}
    hit_count = 0
    locs = [loc]
    _, coord_max = util.grid_dict_coord_range(grid)
    for i in range(steps):
        # print('Step', i)
        next_locs = []
        for loc in locs:
            check_loc = map_loc_to_coord_range(loc, coord_max)
            coord_diff = util.tuple_sub(loc, check_loc)
            if loc not in info:
                info[loc] = {'start': i}
            if check_loc in memo:
                print(loc, check_loc, memo[check_loc])
                if 'delta' not in info[loc]:
                    info[loc]['delta'] = i - info[loc]['start']
                adjacent = memo[check_loc]
                if loc != check_loc:
                    adjacent = [(x+coord_diff[0], y+coord_diff[1]) for (x,y) in adjacent]
                hit_count += 1
            else:
                adjacent = get_open_dirs(grid, loc, blockers, retval='loc', infinite_coord_range=coord_max)
                # print('    Adj', adjacent)
                memo[loc] = adjacent
            next_locs.extend(adjacent)
            next_locs = list(set(next_locs))
        locs = next_locs
    # print(info)
    print(locs)
    print('Memo size', len(memo.keys()))
    print('Hit count', hit_count)
    return locs


def get_open_dirs(grid, loc, blockers=[], retval='dir', infinite_coord_range=None):
    opens = []
    for dir in ['N', 'S', 'E', 'W']:
        next_loc = util.coord_move(loc, dir)
        check_loc = next_loc
        if infinite_coord_range:
            check_loc = map_loc_to_coord_range(next_loc, infinite_coord_range)
        val = grid.get(check_loc)
        if val is not None and val not in blockers:
            if retval == 'dir':
                opens.append(dir)
            elif retval == 'loc':
                opens.append(next_loc)
            elif retval == 'val':
                opens.append(val)
    return opens


def map_loc_to_coord_range(loc, coord_max):
    '''Use mod operator to map to location in coordinate range (for use with an infinitely repeating grid)'''
    return (loc[0] % (coord_max[0]+1), loc[1] % (coord_max[1]+1))



def test():
    test_input = '''
###
#S.
###
    '''
    # assert(process(test_input, 1) == 1)

    test_input = '''
####
.#S.
####
    '''
    # assert(process(test_input, 2) == 2)

    test_input = '''
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........

    '''
    assert(process(test_input, 6) == 16)
    # assert(process(test_input, 10) == 50)
    # assert(process(test_input, 50) == 1594)
    # assert(process(test_input, 100) == 6536)
    # assert(process(test_input, 500) == 167004)
    # assert(process(test_input, 1000) == 668697)
    # assert(process(test_input, 5000) == 16733044)
    print('Time: %s' % (time.time() - start_time))

test()
exit(0)


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input, 26501365)
    print('Result:', val)
    print('Time: %s' % (time.time() - start_time))
