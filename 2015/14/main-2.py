import math

deer = {}

def preprocess_input(input):
    input = input.replace('can fly ', '')
    input = input.replace('km/s for ', '')
    input = input.replace('seconds, but then must rest for ', '')
    input = input.replace(' seconds.', '')
    return input

# with open('test.txt', 'r') as f:
with open('input.txt', 'r') as f:
    # stop_time = 1000
    stop_time = 2503

    input = f.read()
    input = preprocess_input(input)
    print(input)
    for line in input.splitlines():
        name, speed, time, rest = line.split()
        deer[name] = {'speed': int(speed), 'time': int(time), 'rest': int(rest), 'points': 0}
    # print(deer)

    for d in deer:
        deer[d]['dist'] = {}
        curr = 0
        deer[d]['points'] = 0
        cycle_time = 0
        for i in range(stop_time):
            if cycle_time == deer[d]['time'] + deer[d]['rest']:
                cycle_time = 0
            if cycle_time < deer[d]['time']:
                curr += deer[d]['speed']
            deer[d]['dist'][i] = curr
            cycle_time += 1
        print(deer[d]['dist'])

    for i in range(0, stop_time):
        max_dist = max([deer[x]['dist'][i] for x in deer])
        leaders = [x for x in deer if deer[x]['dist'][i] == max_dist]
        for l in leaders:
            deer[l]['points'] += 1
    print(deer)

    max_points = max([deer[x]['points'] for x in deer])
    print('Max:', max_points)

