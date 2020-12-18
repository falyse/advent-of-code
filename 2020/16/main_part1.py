import sys
sys.path.append('../..')
import util


def process(input):
    rules, yours, nearby = process_text(input)
    invalid_sum = 0
    for ticket in nearby:
        print(ticket)
        for value in ticket:
            if not value_is_valid(value, rules):
                print('  invalid:', value)
                invalid_sum += value
    return invalid_sum


def process_text(input):
    rules_text, yours_text, nearby_text = input.strip().split('\n\n')
    yours = util.ints(yours_text)
    nearby = [util.ints(x) for x in nearby_text.splitlines()[1:]]
    rules = {}
    for line in rules_text.splitlines():
        field, values = line.split(': ')
        options = values.split(' or ')
        rules[field] = options
    return rules, yours, nearby


def value_is_valid(value, rules):
    for field, options in rules.items():
        if value_in_any_option(value, options):
            return True
    return False


def value_in_any_option(value, options):
    # print('    ', value, options)
    for value_range in options:
        min_valid, max_valid = value_range.split('-')
        # print('      test', min_valid, value, max_valid)
        if int(min_valid) <= value <= int(max_valid):
            # print('      ok')
            return True
    return False




def test():
    test_input = '''
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
'''
    assert(process(test_input) == 71)
    exit(0)

# test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
