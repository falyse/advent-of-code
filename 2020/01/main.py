import sys
sys.path.append('../..')
import util

def process_part1(input):
    for x in input:
        for y in input:
            if x != y and x+y == 2020:
                return x*y

def process_part2(input):
    for x in input:
        for y in input:
            for z in input:
                if x != y and x != z and y != z and x+y+z == 2020:
                    return x*y*z


with open('input.txt', 'r') as f:
    input = f.read().strip().splitlines()
    input = list(map(int, input))

    result = process_part1(input)
    print('Part 1', result)

    result = process_part2(input)
    print('Part 2', result)
