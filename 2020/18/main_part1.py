import sys
sys.path.append('../..')
import util


def process(input):
    total = 0
    for line in input.strip().splitlines():
        num = evaluate(line)
        total += num
    return total

def evaluate(input):
    input = input.strip()
    input = input.replace('(', '( ')
    input = input.replace(')', ' )')
    expr = replace_parens(input)
    value = calc(expr)
    return value


def replace_parens(input):
    # print(input)
    while '(' in input:
        expr = ''
        for char in input.split():
            if char == '(':
                expr = ''
            elif char == ')':
                value = calc(expr)
                input = input.replace('( %s)' % expr, str(value))
                # print(input)
            else:
                expr += char + ' '
    return input

def calc(input):
    # print(input)
    last_op = '+'
    value = 0
    for char in input.split():
        if char in ['+', '*']:
            last_op = char
        else:
            if last_op == '+':
                value += int(char)
            elif last_op == '*':
                value *= int(char)
        # print(char, ':', value)
    return value


def test():
    assert(evaluate('1 + 2 * 3 + 4 * 5 + 6') == 71)
    assert(evaluate('1 + (2 * 3) + (4 * (5 + 6))') == 51)
    exit(0)

# test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
