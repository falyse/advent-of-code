def set(grid, x, y):
    if x not in grid:
        grid[x] = {}
    grid[x][y] = True

def calc_dist(point):
   x, y = point
   d = abs(x) + abs(y)
   return d

def populate(input):
    grid = {}
    x0 = 0
    y0 = 0
    for step in input:
        dir = step[0]
        val = int(step[1:])
        x1 = x0
        y1 = y0
        if dir == 'R':
            x1 = x0 + val
            for x in range(x0, x1):
                set(grid, x, y0)
        if dir == 'L':
            x1 = x0 - val
            for x in range(x1, x0):
                set(grid, x, y0)
        if dir == 'U':
            y1 = y0 + val
            for y in range(y0, y1):
                set(grid, x0, y)
        if dir == 'D':
            y1 = y0 - val
            for y in range(y1, y0):
                set(grid, x0, y)
        x0 = x1
        y0 = y1
    return grid


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    w1_input, w2_input = f.readlines()
    w1_input = w1_input.strip().split(',')
    w2_input = w2_input.strip().split(',')
    print(w1_input)
    print(w2_input)

    w1 = populate(w1_input)
    w2 = populate(w2_input)

    print(w1)
    print(w2)

    crosses = []
    for x in w1.keys():
        if x in w2.keys():
            for y in w1[x].keys():
                if y in w2[x].keys():
                    if w1[x][y] and w2[x][y]:
                        if x != 0 and y != 0:
                            print('Cross', x, y)
                            crosses.append((x,y))


    print(crosses)
    dists = [calc_dist(point) for point in crosses]
    print(dists)
    print('Min', min(dists))


