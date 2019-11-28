houses = {}

def add_gift(x, y):
    global houses
    if x not in houses:
        houses[x] = {}
    if y not in houses[x]:
        houses[x][y] = 0
    houses[x][y] += 1

def process_input_steps(input):
    x = 0
    y = 0
    add_gift(x, y)
    for step in input:
        if step == '>':
            x += 1
        if step == '<':
            x -= 1
        if step == '^':
            y += 1
        if step == 'v':
            y -= 1
        add_gift(x, y)
    print(houses)

with open('input_03.txt', 'r') as f:
    input = f.read()
    # input = '^v^v^v^v^v'
    santa_input = []
    robot_input = []
    i = 0
    for x in input:
        if i % 2:
            robot_input.append(x)
        else:
            santa_input.append(x)
        i += 1
    process_input_steps(santa_input)
    process_input_steps(robot_input)

    count_at_least_one = 0
    for x in houses:
        for y in houses[x]:
            if houses[x][y] > 0:
                count_at_least_one += 1
    print('At least one:', count_at_least_one)


