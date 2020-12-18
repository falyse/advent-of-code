import sys
sys.path.append('../..')
import util


def process(input):
    rules, yours, nearby = process_text(input)
    valid_tickets = get_valid_tickets(rules, yours, nearby)
    positions = get_field_positions(valid_tickets, rules)

    result = 1
    for field, pos in positions.items():
        if 'departure' in field:
            result = result * yours[pos]
    return result


def get_field_positions(valid_tickets, rules):
    positions = {}
    i = 0
    while len(positions) != len(rules):
        iterate_field_positions(positions, valid_tickets, rules)
        i += 1
        print('Iteration', i)
        print(positions)
    return positions


def iterate_field_positions(positions, valid_tickets, rules):
    for i in range(len(valid_tickets[0])):
        all_values = [x[i] for x in valid_tickets]
        # print(i, all_values)
        matches = []
        for field, options in rules.items():
            if field in positions:
                continue
            # print('check', i, field, options)
            if all_values_match_options(all_values, options):
                # print('  match', field)
                matches.append(field)
        if len(matches) == 1:
            positions[matches[0]] = i
    return positions


def get_valid_tickets(rules, yours, nearby):
    valid_tickets = [yours]
    for ticket in nearby:
        all_values_valid = True
        for value in ticket:
            if not value_is_valid(value, rules):
                all_values_valid = False
        if all_values_valid:
            valid_tickets.append(ticket)
    return valid_tickets


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
    for value_range in options:
        min_valid, max_valid = value_range.split('-')
        if int(min_valid) <= value <= int(max_valid):
            return True
    return False


def all_values_match_options(all_values, options):
    for value in all_values:
        if not value_in_any_option(value, options):
            # print('    fail at', value)
            return False
    return True



def test():
    test_input = '''
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
'''
    process(test_input)
    exit(0)

# test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 2:', val)
