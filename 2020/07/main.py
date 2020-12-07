import sys
sys.path.append('../..')
import util
import re


def process(input, own_bag, part1):
    lines = input.strip().splitlines()
    parent_bags = {}
    child_bags = {}
    for line in lines:
        parent, children = line.split(' bags contain ')
        child_bags[parent] = []
        for child in children.split(','):
            m = re.search(r'(\d+) (.+) bag', child)
            if m:
                child_cnt, child_bag = int(m.group(1)), m.group(2)
                child_bags[parent].append((child_cnt, child_bag))
                if child_bag not in parent_bags:
                    parent_bags[child_bag] = []
                parent_bags[child_bag].append((child_cnt, parent))
    # util.pretty_print(bags)

    current = own_bag
    valid_bags = set()

    if part1:
        search_paths(parent_bags, current, valid_bags)
        return len(valid_bags)
    else:
        total_bags = search_paths(child_bags, current, valid_bags)
        return total_bags - 1


def search_paths(bags, current, valid_bags):
    if current not in bags:
        return 1
    next_bags = bags[current]
    total_bags = 1
    # print(current, next_bags)
    for num_bag, next_bag in next_bags:
        valid_bags.add(next_bag)
        tb = search_paths(bags, next_bag, valid_bags)
        total_bags += num_bag * tb
        # print(next_bag, num_bag, '*', tb, '=', num_bag*tb, '=>', total_bags)
    return total_bags


def test():
    rules = '''
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
'''
    assert(process(rules, 'shiny gold', True) == 4)
    assert(process(rules, 'shiny gold', False) == 32)


test()


with open('input.txt', 'r') as f:
    input = f.read()
    num = process(input, 'shiny gold', True)
    print('Part 1:', num)
    num = process(input, 'shiny gold', False)
    print('Part 2:', num)
