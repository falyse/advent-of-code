import sys
sys.path.append('../..')
import util
import networkx as nx
from dataclasses import dataclass


def process(input):
    G = build_graph(input)
    total = 0
    loc = 'AA'
    for minute in range(1, 2):
        print()
        print('== Minute %0d ==' % minute)
        print('At valve', loc)
        visited = set()
        loc, value = step(G, visited, loc, 28 - minute)
        total += value
    return total


def step(G, visited, loc, remaining):
    if loc in visited:
        return
    visited.add(loc)
    flow = G.nodes[loc]['flow']
    next_loc = loc
    for path in G.adj[loc]:
        print('  Path', path)
    return next_loc, 0


def calc_weight(loc, remaining, visited):
    weight = loc.flow * remaining
    for path in loc.paths:
        if path.name not in visited:
            visited.add(loc.name)
            print('    Adding path', path.name, 'at time', remaining, '=', path.flow * remaining, '-', visited)
            weight += calc_weight(path, remaining-2, visited)
    return weight


def build_graph(input):
    G = nx.Graph()
    lines = input.strip().splitlines()
    for line in lines:
        words = line.split()
        name = words[1]
        flow = util.ints(words[4])[0]
        path_names = [x.strip(',') for x in words[9:]]
        G.add_node(name, flow=flow)
        for n in path_names:
            G.add_edge(name, n)
    # print(G.nodes.data())
    return G


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
