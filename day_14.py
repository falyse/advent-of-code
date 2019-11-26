deer = {}

def preprocess_input(input):
    input = input.replace('can fly ', '')
    input = input.replace('km/s for ', '')
    input = input.replace('seconds, but then must rest for ', '')
    input = input.replace(' seconds.', '')
    return input

with open('input_14.txt', 'r') as f:
    input = f.read()
    input = preprocess_input(input)
    print(input)
    for line in input.splitlines():
        name, speed, time, rest = line.split()
        deer[name] = {'speed': int(speed), 'time': int(time), 'rest': int(rest)}
    # print(deer)

    stop_time = 2503
    max = 0
    for d in deer.keys():
        cycle_time = deer[d]['time'] + deer[d]['rest']
        num_cycles = stop_time / cycle_time
        full_cycles = int(num_cycles)
        partial_cycles = num_cycles - full_cycles
        # print(num_cycles, full_cycles, partial_cycles)
        partial_time = partial_cycles * cycle_time
        fly_time = deer[d]['time'] * full_cycles
        if partial_time > deer[d]['time']:
            fly_time += deer[d]['time']
        else:
            fly_time += int(partial_time)
        dist = deer[d]['speed'] * fly_time
        print(d, dist)
        if dist > max:
            max = dist
    print('Max:', max)


