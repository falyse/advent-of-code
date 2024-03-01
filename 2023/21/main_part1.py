import sys
sys.path.append('../..')
import util
import time
start_time = time.time()


def process(input, steps):
    grid = util.text_to_grid_dict(input.strip())
    loc = util.grid_dict_locate_item(grid, 'S')
    grid[loc] = '.'
    endpoints = util.find_all_endpoints(grid, loc, steps, blockers=['#'])
    print(endpoints)
    return len(endpoints)
    

# def find_all_endpoints_recurse(grid, loc, steps, max_steps, endpoints=[], memo=None, debug=False):
#     '''Recurse to find all unique endpoints from start location moving a specified number of steps'''
#     print('At loc', loc, 'in', steps, 'steps')
#     if memo is not None and loc in memo:
#         print('  memo', loc, memo[loc])
#     if debug:
#         util.render_grid(grid, loc)

#     endpoints = []
#     if steps == max_steps:
#         if debug:
#             print('  Found end', loc, 'at', steps, 'steps')
#         endpoints.append(loc)
#     else:
#         for dir in util.get_open_dirs(grid, loc, ['#']):
#             move_loc = util.coord_move(loc, dir)
#             adjacent = find_all_endpoints_recurse(grid, move_loc, steps+1, max_steps, endpoints, memo)
#             print('  adjacent', loc, adjacent)
#             endpoints.extend(adjacent)
#     print('  endpoints', loc, endpoints, steps)
#     if memo is not None:
#         memo[loc] = endpoints
#     return endpoints


# def find_all_endpoints_bfs(grid, loc_s, max_steps, allow_revisit=False, debug=False):
#     '''BFS to find all unique endpoints from start location moving a specified number of steps'''
#     endpoints = []
#     visited = {}
#     queue = [{'loc': loc_s, 'steps': 0}]
#     while len(queue) > 0:
#         current = queue.pop()
#         loc = current['loc']
#         steps = current['steps']
#         if allow_revisit or (loc not in visited or visited[loc] > steps):
#             visited[loc] = steps

#             if debug:
#                 print('At loc', loc, 'in', steps, 'steps')
#                 util.render_grid(grid, loc)

#             if steps == max_steps:
#                 if debug:
#                     print('  Found end', loc, 'at', steps, 'steps')
#                 endpoints.append(loc)
#             else:
#                 for dir in util.get_open_dirs(grid, loc, ['#']):
#                     if debug:
#                         print('    Dir', dir)
#                     move_loc = util.coord_move(loc, dir)
#                     queue.append({'loc': move_loc, 'steps': steps+1})
#     endpoints = list(set(endpoints))  # remove duplicates
#     return endpoints


def test():
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
    # assert(process(test_input, 2) == 4)
    assert(process(test_input, 6) == 16)

test()
# exit(0)


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input, 64)
    print('Result:', val)
    print('Time: %s' % (time.time() - start_time))
    assert(val == 3658)
