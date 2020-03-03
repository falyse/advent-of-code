import sys
sys.path.append('..')
import util

def decode(input, algo='most'):
    input = input.strip().splitlines()
    code = ''
    for i in range(len(input[0])):
        cnts = {}
        for j in range(len(input)):
            char = input[j][i]
            if char in cnts:
                cnts[char] += 1
            else:
                cnts[char] = 1
        if algo == 'most':
            code += util.key_with_max_value(cnts)
        else:
            code += util.key_with_min_value(cnts)
    print(code)
    return code


def test():
    test_input = r"""
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar    
    """
    assert decode(test_input, algo='most') == 'easter'
    assert decode(test_input, algo='least') == 'advent'

test()


with open('input.txt', 'r') as f:
    input = f.read().strip()
    code = decode(input, algo='most')
    print('Part 1 code:', code)
    code = decode(input, algo='least')
    print('Part 2 code:', code)
