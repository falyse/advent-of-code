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
    # print(expr)
    expr = replace_add(expr)
    print(expr)
    value = calc(expr)
    print(value)
    return value


def replace_parens(input):
    # print(input)
    while '(' in input:
        expr = ''
        for char in input.split():
            if char == '(':
                expr = ''
            elif char == ')':
                print('  ', expr)
                calc_expr = replace_add(expr)
                print('  ', calc_expr)
                value = calc(calc_expr)
                input = input.replace('( %s)' % expr, str(value))
                # print(input)
            else:
                expr += char + ' '
    return input

def replace_add(input):
    print(input)
    while '+' in input:
        expr = ''
        for char in input.split():
            if char == '*':
                expr = ''
            else:
                expr += char + ' '
                if '+' in expr and char != '+':
                    expr = expr.rstrip()
                    value = calc(expr)
                    input = input.replace(expr, str(value))
                    print(input, ':', expr)
                    break
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
    # assert(evaluate('1 + 2 * 3 + 4 * 5 + 6') == 231)
    # assert(evaluate('1 + (2 * 3) + (4 * (5 + 6))') == 51)
    # assert(evaluate('2 * 3 + (4 * 5)') == 46)
    # assert(evaluate('4 + 9 + 3') == 16)
    assert(evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445)
    exit(0)

# test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 2:', val)  # 54461147888880 too low
