import sys
sys.path.append('../..')
import util
import pprint
import itertools
import copy


def process(input):
    lines = input.strip().splitlines()
    wires = {}
    freq = {}
    pairs = set()
    for line in lines:
        src, dsts = line.split(': ')
        for dst in dsts.split():
            wires.setdefault(src, []).append(dst)
            wires.setdefault(dst, []).append(src)
            pairs.add((src, dst))
            freq[dst] = freq.get(dst, 0) + 1
    pprint.pprint(wires)

    # pprint.pprint(freq)
    # print(pairs)
    # test = [x[0] for x in util.sort_by_value(freq)]

    # test = []
    # for k1, v1 in wires.items():
    #     for k2, v2 in wires.items():
    #         if k1 != k2:
    #             print(k1, k2)
    #             intersection = list(set(v1) & set(v2))
    #             print('  ', intersection)
    #             if len(intersection) == 0:
    #                 if (k2, k1) not in test:
    #                     test.append((k1, k2))
    # pprint.pprint(test)

    combos = itertools.combinations(pairs, 3)
    for combo in list(combos):
        w = disconnect(wires, combo)
        num_groups = find_num_groups(w)
        # print('Num groups', num_groups)
        if num_groups == 2:
            print('Combo:', combo)
            groups = find_connected_groups(w)
            val = len(groups[0]) * len(groups[1])
            print(val)
            return val


def disconnect(wires_orig, combo):
    wires = copy.deepcopy(wires_orig)
    # pprint.pprint(wires)
    for pair in combo:
        # print(pair)
        wires[pair[0]].remove(pair[1])
        wires[pair[1]].remove(pair[0])
    # pprint.pprint(wires)
    return wires


def find_connected_groups(wires):
    groups = []
    for k in wires.keys():
        new_group = True
        for g in groups:
            if k in g:
                new_group = False
        if not new_group:
            continue
        group = set()
        # print('Start', k)
        if k in group:
            continue
        find_conns(wires, k, group)
        # print(group)
        groups.append(group)
        # if len(group) == len(wires.keys()):
            # return groups
    # print(groups)
    return groups


def find_num_groups(wires):
    groups = find_connected_groups(wires)
    return len(groups)


def find_conns(wires, k, conns=set()):
    # print('Traverse', k)
    for v in wires[k]:
        if v not in conns:
            conns.add(v)
            find_conns(wires, v, conns)


def test():
    assert(find_num_groups({'abc': ['def'], 'def': ['abc']}) == 1)
    assert(find_num_groups({'a': ['b'], 'x': ['y'], 'y': ['x'], 'b': ['a']}) == 2)

    test_input = '''
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr

    '''
    assert(process(test_input) == 54)

test()
# exit(0)


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Result:', val)
