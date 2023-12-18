import sys
sys.path.append('../..')
import util
import heapq


def process(input):
    grid = util.text_to_grid_dict(input.strip())
    loc_s, loc_e = util.grid_dict_coord_range(grid)
    debug = True
    debug = False
    # paths = find_valid_paths(grid, loc_s, loc_e, debug)
    costs = find_grid_path_costs(grid, loc_s, debug)
    # print(costs)
    costs = [v for k,v in costs.items() if k[0] == loc_e]
    # print(costs)
    print('Best path:', min(costs))
    return min(costs)


def find_grid_path_costs(grid, loc_s, debug=False):
    '''
    Dijkstra's algorithm to find the best costs between start location and all other nodes in the grid
    Returns a dict with {loc: lowest_cost_from_loc_s}
    '''
    loc_id = (loc_s, None)  # loc, last_dir
    costs = {
        loc_id: 0
    }
    priority_queue = [(0, (loc_id))]
    visited = set()
    while len(priority_queue) > 0:
        _cost, loc_id = heapq.heappop(priority_queue)
        loc, last_dir = loc_id
        if debug:
            print('loc_id', loc_id, 'cost', costs[loc_id])
        if loc_id in visited:
            continue
        visited.add(loc_id)
        # Check all adjacent nodes
        for dir in get_open_dirs(grid, loc, last_dir, 0):
            dist_cost = 0
            for dist in range(1, 4):
                # If the current node's cost + cost to the node we're visiting
                # is less than the previously recorded cost of the node we're visiting,
                # replace that cost and push the node we're visiting into the priority queue
                move_loc = util.coord_move(loc, dir, dist)
                if move_loc in grid:
                    move_cost = int(grid[move_loc]) + dist_cost
                    dist_cost = move_cost
                    move_loc_id = (move_loc, dir)
                    
                    if debug:
                        print(' dir', dir, '*', dist, 'to', move_loc, 'move_cost', move_cost, 'cur_cost', costs.get(move_loc_id))
                    if (move_loc_id not in costs) or (costs[loc_id] + move_cost < costs[move_loc_id]):
                        costs[move_loc_id] = costs[loc_id] + move_cost
                        heapq.heappush(priority_queue, (costs[move_loc_id], (move_loc, dir)))
    return costs


def get_open_dirs(grid, loc, last_dir, dir_steps):
    opens = []
    cur_val = grid[loc]
    if last_dir is None:
        valid_dirs = ['N', 'S', 'E', 'W']
    else:
        valid_dirs = [util.coord_turn(last_dir, 'left'), util.coord_turn(last_dir, 'right')]
        # if dir_steps < 3:
        #     valid_dirs.append(last_dir)
    # print('valid_dirs', valid_dirs)
    for dir in valid_dirs:
        next_loc = util.coord_move(loc, dir)
        val = grid.get(next_loc)
        if val is not None:
            opens.append(dir)
    return opens


def test():
    test_input = '''
24
32
    '''
    assert(process(test_input) == 5)

    test_input = '''
241
321
325
    '''
    # 11, 12, 13, 11, 12, 13
    assert(process(test_input) == 11)

    test_input = '''
24111
32356
    '''
    # 17, 19, 20, 19, 17
    assert(process(test_input) == 17)

    test_input = '''
112999
911111
    '''
    assert(process(test_input) == 7)

    test_input = '''
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533

    '''
    assert(process(test_input) == 102)

test()
# exit(0)


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
