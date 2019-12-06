def populate_grid(input):
    """Process input directions to route the wire path to a 2-d grid dict
       At each coordinate, store the number of steps taken so far"""
    grid = {}
    x0 = 0
    y0 = 0
    num_steps = 0
    for route in input:
        # print(route)
        dir = route[0]
        val = int(route[1:])

        x1 = x0
        y1 = y0
        if dir == 'R':
            x1 = x0 + val
        if dir == 'L':
            x1 = x0 - val
        if dir == 'U':
            y1 = y0 + val
        if dir == 'D':
            y1 = y0 - val

        # print('x', get_range(x0, x1), ', y', get_range(y0, y1))
        for x in get_range(x0, x1):
            for y in get_range(y0, y1):
                set_point(grid, x, y, num_steps)
                num_steps += 1
        x0 = x1
        y0 = y1
    return grid


def get_range(p0, p1):
    """Return list between two values, accomodating for all equality cases"""
    if p0 == p1:
        return [p0]
    elif p0 > p1:
        return range(p0, p1, -1)
    else:
        return range(p0, p1)


def set_point(grid, x, y, num_steps):
    """Set the grid value of the specified point to the passed number of steps"""
    if x not in grid:
        grid[x] = {}
    if y not in grid[x]:
        grid[x][y] = num_steps
        # print('  ', x, y, 'steps', i)


def calc_dist(point):
    """Manhattan distance from origin to point"""
    x, y = point
    d = abs(x) + abs(y)
    return d


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    w1_input, w2_input = f.readlines()
    w1_input = w1_input.strip().split(',')
    w2_input = w2_input.strip().split(',')

    grid1 = populate_grid(w1_input)
    grid2 = populate_grid(w2_input)

    crosses = []
    for x in grid1.keys():
        if x in grid2.keys():
            for y in grid1[x].keys():
                if y in grid2[x].keys():
                    if grid1[x][y] and grid2[x][y]:
                        if x != 0 and y != 0:
                            crosses.append((x,y))

    # Part 1: Mininum Manhattan distance to cross
    dists = [calc_dist(point) for point in crosses]
    print('Min distance', min(dists))
    assert min(dists) == 896

    # Part 2: Minimum steps to cross
    steps = [grid1[x][y] + grid2[x][y] for x,y in crosses]
    print('Min steps', min(steps))
    assert min(steps) == 16524


