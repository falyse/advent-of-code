import sys
sys.path.append('../..')
import util


def process(input):
    in_paren = False
    in_marker = False
    marker = ''
    num_chars = -1
    data = []
    for i, x in enumerate(input):
        if num_chars > 0:
            data.append(x)
            num_chars -= 1
            continue

        if x == '(':
            in_paren = True
            if not in_marker:
                in_marker = True

        if in_marker:
            marker += x
        else:
            data.append(x)

        if x == ')':
            in_paren = False
            if in_marker:
                data.append(marker)
                num_chars, repeat = util.ints(marker)
                in_marker = False
                marker = ''

    print(data)

    output = ''
    num_chars = -1
    char_cnt = 0
    char_group = ''
    for x in data:
        if len(x) > 1:
            num_chars, repeat = util.ints(x)
            char_cnt = 0
            char_group = ''
        elif num_chars > char_cnt:
            char_group += x
            char_cnt += 1
            if num_chars == char_cnt:
                for i in range(repeat):
                    output += char_group
                num_chars = -1
        else:
            output += x

    print(output)
    print()
    return output


def test():
    assert(process('ADVENT') == 'ADVENT')
    assert(process('A(1x5)BC') == 'ABBBBBC')
    assert(process('(3x3)XYZ') == 'XYZXYZXYZ')
    assert(process('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG')
    assert(process('(6x1)(1x3)A') == '(1x3)A')
    assert(process('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY')
    exit(0)

# test()


with open('input.txt', 'r') as f:
    input = f.read().strip()
    output = process(input)
    print(len(output))
