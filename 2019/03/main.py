def populate_grid(input):
    """Process input directions to route the wire path to a dict of points
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
    if (x,y) not in grid:
        grid[(x,y)] = num_steps


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

    # Crosses are points that exist in both grids
    crosses = []
    for point in grid1.keys():
        if point in grid2.keys():
            if point != (0,0):
                crosses.append(point)

    # Part 1: Minimum Manhattan distance
    dists = [calc_dist(point) for point in crosses]
    print('Min distance', min(dists))
    assert min(dists) == 896

    # Part 2: Minimum steps
    steps = [grid1[point] + grid2[point] for point in crosses]
    print('Min steps', min(steps))
    assert min(steps) == 16524


