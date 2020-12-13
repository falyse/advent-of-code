import sys
sys.path.append('../..')
import util


def process(input):
    instrs = input.strip().splitlines()
    loc = (0, 0)
    way = (10, 1)
    dir = 'E'
    for instr in instrs:
        cmd, val = instr[0], int(instr[1:])
        if cmd == 'F':
            move = tuple([val*x for x in way])
            loc = util.tuple_add(loc, move)
        elif cmd in ['L', 'R']:
            repeat = int(val/90)
            for _ in range(repeat):
                way = way[1], way[0]
                if cmd == 'L':
                    way = (way[0] * -1, way[1])
                else:
                    way = (way[0], way[1] * -1)
        else:
            way = util.coord_move(way, cmd, val)
        print(cmd, val, '->', loc, way)
    return util.taxi_distance(loc)


def test():
    test_input = '''
F10
N3
F7
R90
F11
'''
    assert(process(test_input) == 286)
    exit(0)

# test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 2:', val)
