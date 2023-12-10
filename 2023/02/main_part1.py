import sys
sys.path.append('../..')
import util
import re


def process(input, limits):
    lines = input.strip().splitlines()
    total = 0
    for line in lines:
        print(line)
        id, set_info = line.split(': ')
        sets = set_info.split('; ')
        id = util.ints(id)[0]
        valid = True
        for s in sets:
            cubes = s.split(', ')
            for c in cubes:
                num, color = c.split(' ')
                num = int(num)
                if num > limits[color]:
                    valid = False
        if valid:
            print(id)
            total += id
    return total

limits = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

def test():
    test_input = '''
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    '''
    assert(process(test_input, limits) == 8)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input, limits)
    print('Part 1:', val)
    # assert(val == )
