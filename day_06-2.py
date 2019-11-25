size = 1000
lights = [[0 for y in range(size)] for x in range (size)]

def parse_line(line):
    cmd, range0, _through, range1 = line.split()
    # print(cmd, range0, range1)
    x0, y0 = get_coords(range0)
    x1, y1 = get_coords(range1)
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            if cmd == 'on':
                lights[x][y] += 1
            if cmd == 'off' and lights[x][y] > 0:
                lights[x][y] -= 1
            if cmd == 'toggle':
                lights[x][y] += 2

def get_coords(range):
    x, y = range.split(',')
    return int(x), int(y)


with open('input_06.txt', 'r') as f:
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
    # Sum brightness
    brightness = 0
    for x in range(size):
        for y in range(size):
            brightness += lights[x][y]
    print('Brightness:', brightness)

