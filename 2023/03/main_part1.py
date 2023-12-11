import sys
sys.path.append('../..')
import util
import re


def process(input):
    input = input.strip()
    grid = util.text_to_grid_dict(input)
    lines = input.splitlines()
    total = 0
    for index, line in enumerate(lines):
        for m in re.finditer(r'\d+', line):
            num = m.group(0)
            span = m.span()
            # Search around the span for a symbol
            found_symbol = False
            for dy in range(-1,2):
                y = index + dy
                for x in range(span[0] - 1, span[1] + 1):
                    if (x, y) in grid:
                        if not re.match(r'[0-9]|\.', grid[(x,y)]):
                            found_symbol = True
            if found_symbol:
                total += int(num)
    return total


def test():
    test_input = '''
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

    '''
    assert(process(test_input) == 4361)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
    # assert(val == )
