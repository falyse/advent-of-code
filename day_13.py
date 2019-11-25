from itertools import permutations

happy = {}

def preprocess_input(input):
    input = input.replace('would ', '')
    input = input.replace('happiness units by sitting next to ', '')
    input = input.replace('.', '')
    input = input.replace('gain ', '')
    input = input.replace('lose ', '-')
    return input

def add_yourself():
    happy['you'] = {}
    for guest in happy.keys():
        happy['you'][guest] = 0
        happy[guest]['you'] = 0

with open('input_13.txt', 'r') as f:
# with open('input_13-test.txt', 'r') as f:
    input = f.read()
    input = preprocess_input(input)
    for line in input.splitlines():
        who, gain, neighbor = line.split()
        if who not in happy:
            happy[who] = {}
        happy[who][neighbor] = int(gain)
    print(happy)

    add_yourself()

    perms = permutations(happy.keys())
    max = 0
    for order in list(perms):
        sum = 0
        for i in range(len(order)):
            guest = order[i]
            neighbor = order[i-1]
            local = happy[guest][neighbor] + happy[neighbor][guest]
            sum += local
            # print(guest, neighbor, happy[guest][neighbor], happy[neighbor][guest], local)
        print(order, sum)
        if sum > max:
            max = sum
    print('Max:', max)
