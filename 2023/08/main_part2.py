import sys
sys.path.append('../..')
import util


def process(input):
    instr, locs = input.strip().split('\n\n')
    instr = instr.strip().replace('R', '1').replace('L', '0')
    instr = [int(x) for x in instr]
    print(instr)
    lines = locs.strip().splitlines()
    nodes = {}
    for line in lines:
        key, locs = line.split(' = (')
        locs = locs.replace(')', '').split(', ')
        nodes[key] = locs
    print(nodes)

    start_nodes = [x for x in nodes.keys() if x[2] == 'A']
    # steps = run_parallel_search(instr, nodes, start_nodes)
    steps = run_lcm_search(instr, nodes, start_nodes)
    return steps


def run_parallel_search(instr, nodes, start_nodes):
    current = {x: x for x in start_nodes}
    steps = 0
    while True:
        dir = instr[steps % len(instr)]
        for k in start_nodes:
            node = current[k]
            # print('Step %0d : node %s, dir %0d' % (steps, node, dir))
            node = nodes[node][dir]
            current[k] = node
        # print(current)
        steps += 1
        end_nodes = [x for x in current.values() if x[2] == 'Z']
        if len(end_nodes) == len(start_nodes):
            break
    return steps


def run_lcm_search(instr, nodes, start_nodes):
    final_steps = []
    for node in start_nodes:
        steps = 0
        while True:
            dir = instr[steps % len(instr)]
            print('Step %0d : node %s, dir %0d' % (steps, node, dir))
            node = nodes[node][dir]
            steps += 1
            if node[2] == 'Z':
                final_steps.append(steps)
                break
    print(final_steps)
    lcm = util.lcmm(*final_steps)
    print('LCM:', lcm)
    return lcm


def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited


def test():
    test_input = '''
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''
    assert(process(test_input) == 6)
test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 2:', val)
