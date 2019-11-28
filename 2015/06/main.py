size = 1000
lights = [[False for y in range(size)] for x in range (size)]

def parse_line(line):
    cmd, range0, _through, range1 = line.split()
    print(cmd, range0, range1)
    x0, y0 = get_coords(range0)
    x1, y1 = get_coords(range1)
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            if cmd == 'on':
                lights[x][y] = True
            if cmd == 'off':
                lights[x][y] = False
            if cmd == 'toggle':
                lights[x][y] = not lights[x][y]

def get_coords(range):
    x, y = range.split(',')
    return int(x), int(y)


with open('input.txt', 'r') as f:
    input = f.readlines()
    #input = [
    #   'turn on 0,0 through 9,9',
    #   'turn on 0,0 through 999,999',
    #   'toggle 0,0 through 999,0',
    #   'turn off 499,499 through 500,500'
    #]
    # Remove 'turn ' and from all lines
    input = [x.replace('turn ', '') for x in input]
    # Process each line
    [parse_line(line) for line in input]
    # Count
    num_on = 0
    for x in range(size):
        for y in range(size):
            if lights[x][y]:
                num_on += 1
    print('Num on:', num_on)

