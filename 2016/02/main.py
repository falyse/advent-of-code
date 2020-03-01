import sys
sys.path.append('..')
import util

KEY_MAP1 = {(0, 0): '1',
            (1, 0): '2',
            (2, 0): '3',
            (0,-1): '4',
            (1,-1): '5',
            (2,-1): '6',
            (0,-2): '7',
            (1,-2): '8',
            (2,-2): '9'}

KEY_MAP2 = {(2, 0): '1',
            (1,-1): '2',
            (2,-1): '3',
            (3,-1): '4',
            (0,-2): '5',
            (1,-2): '6',
            (2,-2): '7',
            (3,-2): '8',
            (4,-2): '9',
            (1,-3): 'A',
            (2,-3): 'B',
            (3,-3): 'C',
            (2,-4): 'D'}

DIR_MAP = {'U': 'N',
           'D': 'S',
           'R': 'E',
           'L': 'W'}

def get_code(input, key_map):
    code = ''
    num = '5'
    for line in input.strip().splitlines():
        num = get_number(num, line, key_map)
        code += str(num)
    return code


def get_number(start_num, line, key_map):
    loc = [k for k,v in key_map.items() if v == start_num][0]
    #print('start', start_num, loc)
    for dir in line:
        try_loc = util.coord_move(loc, DIR_MAP[dir])
        if try_loc in key_map:
            loc = try_loc
        #print('  loc', loc)
    return key_map[loc]


def test():
    assert get_code(r"""
ULL
RRDDD
LURDL
UUUUD""", KEY_MAP1) == '1985'

    assert get_code(r"""
ULL
RRDDD
LURDL
UUUUD""", KEY_MAP2) == '5DB3'

test()


with open('input.txt', 'r') as f:
    input = f.read()
    code = get_code(input, KEY_MAP1)
    print('Part 1 code:', code)
    code = get_code(input, KEY_MAP2)
    print('Part 2 code:', code)

