import sys
sys.path.append('../..')
import util


def process(input):
    seeds, name_map, maps = build_maps(input)
    loc = None
    for seed in seeds:
        l = find_loc('seed', seed, name_map, maps)
        if loc is None or l < loc:
            loc = l
        print()
    print('Min location', loc)
    return loc


def find_loc(name, id, name_map, maps):
    print(name, id)
    if name != 'location':
        found = False
        for dst, src, l in maps[name]:
            if id >= src and id <= (src + l):
                found = True
                id += (dst - src)
            if found:
                break
        name = name_map[name]
        id = find_loc(name, id, name_map, maps)
    return id


def build_maps(input):
    input = input.strip()
    groups = input.split('\n\n')
    seeds = util.ints(groups[0])
    maps = {}
    name_map = {}
    for g in groups[1:]:
        lines = g.splitlines()
        name = lines[0].split()[0]
        name_src, name_dst = name.split('-to-')
        name_map[name_src] = name_dst
        maps[name_src] = []
        for line in lines[1:]:
            dst, src, l = util.ints(line)
            maps[name_src].append((dst, src, l))
    return seeds, name_map, maps


def test():
    test_input = '''
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

    '''
    assert(process(test_input) == 35)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
    # assert(val == )
