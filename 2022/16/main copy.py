import sys
sys.path.append('../..')
import util
from dataclasses import dataclass


open_valves = {}

@dataclass
class Valve:
    name: str
    flow: int
    path_names: list

    # def get_path_values(self, remaining):
    #     visited = {}
    #     queue = [self]
    #     queue = [{'loc': self, 'steps': 0, 'weight': self.flow*remaining}]
    #     while len(queue) > 0:
    #         current = queue.pop()
    #         loc = current['loc']
    #         steps = current['steps']
    #         # weight = current['weight']
    #         if loc.name not in visited or visited[loc.name] > steps:
    #             visited[loc.name] = steps

    #             weight = loc.flow * (remaining - steps)
    #             print('Path', loc.name, '(%0d steps)' % steps, weight)
    #             print('    ', remaining-steps)

    #             for path in loc.paths:
    #                 if path.name not in visited:
    #                     print('  Path', path.name, visited)
    #                     queue.append({'loc': path, 'steps': steps+1, 'weight': weight})


def process(input):
    map = build_map(input)
    total = 0
    loc = map['AA']
    for minute in range(1, 3):
        print()
        print('== Minute %0d ==' % minute)
        total += sum(open_valves.values())
        loc = step(loc, 28 - minute)
        print('Total', total)
    return total


def step(loc, remaining):
    global open_valves
    local_weight = loc.flow * remaining
    print('At valve', loc.name, '- local weight', local_weight)
    max_weight = local_weight
    next_loc = loc
    for path in loc.paths:
        print('  Path', path.name)
        visited = set([loc.name, path.name])
        weight = calc_weight(path, remaining, visited)
        print('    Weight', weight)
        if weight > max_weight:
            max_weight = weight
            next_loc = path
    if next_loc == loc:
        print('Open valve', loc.name)
        open_valves[loc.name] = loc.flow
        loc.flow = 0
    else:
        print('Move to valve', next_loc.name)
    return next_loc


def calc_weight(loc, remaining, visited):
    weight = loc.flow * remaining
    for path in loc.paths:
        if path.name not in visited:
            visited.add(loc.name)
            print('    Adding path', path.name, 'at time', remaining, '=', path.flow * remaining, '-', visited)
            weight += calc_weight(path, remaining-2, visited)
    return weight


def build_map(input):
    lines = input.strip().splitlines()
    valves = {}
    for line in lines:
        words = line.split()
        name = words[1]
        flow = util.ints(words[4])[0]
        path_names = [x.strip(',') for x in words[9:]]
        valves[name] = Valve(name, flow, path_names)
    for valve in valves.values():
        valve.paths = []
        for n in valve.path_names:
            valve.paths.append(valves[n])
    return valves

def test():
    test_input = '''
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
    '''
    assert(process(test_input) == 1651)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
    # assert(val == )
