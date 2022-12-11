import sys
sys.path.append('../..')
import util


def process(input):
    sacks = input.strip().splitlines()
    sum = 0
    for sack in sacks:
        split_point = int(len(sack)/2)
        c1, c2 = sack[:split_point], sack[split_point:]
        for letter in set(c1) & set(c2):
            sum += get_letter_value(letter)
    return sum


def get_letter_value(letter):
    value = ord(letter)
    if value >= 97:
        value = value - ord('a')
    else:
        value = value - ord('A') + 26
    value += 1
    return value


def test():
    test_input = '''
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
    '''
    assert(get_letter_value('a') == 1)
    assert(get_letter_value('z') == 26)
    assert(get_letter_value('A') == 27)
    assert(get_letter_value('Z') == 52)
    assert(process(test_input) == 157)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
    assert(val == 7568)
