import sys
sys.path.append('../..')
import util


def process_part1(input):
    sum = 0
    for i in range(len(input)):
        if input[i] == input[(i + 1) % len(input)]:
            sum += int(input[i])
    return sum


def process_part2(input):
    sum = 0
    for i in range(len(input)):
        if input[i] == input[(i + len(input) // 2) % len(input)]:
            sum += int(input[i])
    return sum


def test():
    assert(process_part1('1122') == 3)

    assert(process_part2('1212') == 6)
    assert(process_part2('1221') == 0)
    assert(process_part2('123425') == 4)
    assert(process_part2('123123') == 12)
    assert(process_part2('12131415') == 4)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process_part1(input)
    print('Part 1:', val)
    val = process_part2(input)
    print('Part 2:', val)
