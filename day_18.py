lights = []
size = 0

def display():
    text = ''
    for row in lights:
        for light in row:
            text += '#' if light else '.'
        text += '\n'
    print(text)

def update_lights():
    global lights
    x = 0
    y = 0
    new_lights = []
    num_on = 0
    for row in lights:
        new_row = []
        for light in row:
            cnt = 0
            if x > 0:
                cnt += row[x-1]  # left
            if x < size - 1:
                cnt += row[x+1]  # right
            if y > 0:
                cnt += lights[y-1][x]  # top
            if y < size - 1:
                cnt += lights[y+1][x]  # bottom
            if x > 0 and y > 0:
                cnt += lights[y-1][x-1]  # top left
            if x > 0 and y < size - 1:
                cnt += lights[y+1][x-1]  # bottom left
            if x < size - 1 and y > 0:
                cnt += lights[y-1][x+1]  # top right
            if x < size - 1 and y < size - 1:
                cnt += lights[y+1][x+1]  # bottom right
            # print(y, x, '-', cnt)
            if (x == y == 0) or (x == 0 and y == size-1) or (x == size-1 and y == 0) or (x == y == size-1):
                new_row.append(True)
            else:
                if light:
                    new_row.append(cnt in [2, 3])
                else:
                    new_row.append(cnt == 3)
            x += 1
        new_lights.append(new_row)
        num_on += sum(new_row)
        y += 1
        x = 0
    lights = new_lights
    return num_on

with open('input_18.txt', 'r') as f:
# with open('input_18-test.txt', 'r') as f:
    for line in f.readlines():
        row = []
        for char in line.strip():
            row.append(True if char == '#' else False)
        lights.append(row)
    size = len(lights)
    lights[0][0] = True
    lights[0][size-1] = True
    lights[size-1][0] = True
    lights[size-1][size-1] = True
    display()

    steps = 100
    for i in range(steps):
        num_on = update_lights()
        display()
    print('On', num_on)
