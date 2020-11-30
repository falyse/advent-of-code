import sys
sys.path.append('../..')
import util


def process(input):
    item = ''
    in_paren = False
    data = []
    for x in input:
        if x == '(':
            in_paren = True
            item = ''
        elif x == ')':
            in_paren = False
            data.append(item)
        elif in_paren:
            item += x
        else:
            data.append(x)
    print(data)

    output = ''
    num_chars = 1
    char_cnt = 0
    group = ''
    repeat = 1
    in_marker = False
    for item in data:
        if in_marker == False and len(item) > 1:
            in_marker = True
            num_chars, repeat = item.split('x')
            num_chars = int(num_chars)
            repeat = int(repeat)

        char_cnt += 1
        group += item

        elif char_cnt == num_chars:
            for x in range(repeat):
                output += group
                in_marker = False
            char_cnt = 0
            repeat = 1
            group = ''

    print(output)

    return output

def test():
    assert(process('ADVENT') == 'ADVENT')
    assert(process('A(1x5)BC') == 'ABBBBBC')
    assert(process('(3x3)XYZ') == 'XYZXYZXYZ')
    assert(process('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG')
    assert(process('(6x1)(1x3)A') == '(1x3)A')
    assert(process('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY')

test()


with open('input.txt', 'r') as f:
    input = f.read().strip().splitlines()
    output = process(input)
    print(output)
