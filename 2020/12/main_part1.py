import sys
sys.path.append('../..')
import util


def process(input):
    instrs = input.strip().splitlines()
    loc = (0, 0)
    dir = 'E'
    for instr in instrs:
        cmd, val = instr[0], int(instr[1:])
        if cmd == 'F':
            loc = util.coord_move(loc, dir, val)
        elif cmd in ['L', 'R']:
            repeat = int(val/90)
            for _ in range(repeat):
                dir = util.coord_turn(dir, cmd)
        else:
            loc = util.coord_move(loc, cmd, val)
        print(cmd, val, '->', loc, dir)
    return util.taxi_distance(loc)


def test():
    test_input = '''
F10
N3
F7
R90
F11
'''
    assert(process(test_input) == 25)
    exit(0)

# test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
