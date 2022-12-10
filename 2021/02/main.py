import sys
sys.path.append('../..')
import util


dir_map = {
    'forward': 'E',
    'backward': 'W',
    'up': 'S',
    'down': 'N',
}

def process(input):
    cmds = input.strip().splitlines()
    loc = (0, 0)
    for cmd in cmds:
        dir, num = cmd.split()
        loc = util.coord_move(loc, dir_map[dir], int(num))
        print(cmd, loc)
    return loc[0] * loc[1]


def test():
    test_input = '''
forward 5
down 5
forward 8
up 3
down 8
forward 2
    '''
    assert(process(test_input) == 150)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
