def set(grid, x, y, i):
    if x not in grid:
        grid[x] = {}
    if y not in grid[x]:
        grid[x][y] = i
        # print('  ', x, y, 'steps', i)

def calc_dist(point):
   x, y = point
   d = abs(x) + abs(y)
   return d

def populate(input):
    grid = {}
    x0 = 0
    y0 = 0
    i = 0
    for step in input:
        # print(step)
        dir = step[0]
        val = int(step[1:])
        x1 = x0
        y1 = y0
        if dir == 'R':
            x1 = x0 + val
            for x in range(x0, x1):
                set(grid, x, y0, i)
                i += 1
        if dir == 'L':
            x1 = x0 - val
            for x in range(x0, x1, -1):
                set(grid, x, y0, i)
                i += 1
        if dir == 'U':
            y1 = y0 + val
            for y in range(y0, y1):
                set(grid, x0, y, i)
                i += 1
        if dir == 'D':
            y1 = y0 - val
            for y in range(y0, y1, -1):
                set(grid, x0, y, i)
                i += 1
        x0 = x1
        y0 = y1
    return grid, i-1


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    w1_input, w2_input = f.readlines()
    w1_input = w1_input.strip().split(',')
    w2_input = w2_input.strip().split(',')
    print(w1_input)
    print(w2_input)

    w1, s1 = populate(w1_input)
    w2, s2 = populate(w2_input)

    print(w1)
    print(w2)
    print(s1)
    print(s2)

    crosses = []
    for x in w1.keys():
        if x in w2.keys():
            for y in w1[x].keys():
                if y in w2[x].keys():
                    if w1[x][y] and w2[x][y]:
                        if x != 0 and y != 0:
                            print('Cross', x, y, 'steps', w1[x][y], w2[x][y])
                            crosses.append(w1[x][y] + w2[x][y])


    print(crosses)
    print('Min', min(crosses))


