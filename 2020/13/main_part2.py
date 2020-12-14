import sys
sys.path.append('../..')
import util


def process(input):
    constraints = [None if b == 'x' else int(b) for b in input.split(',')]
    print(constraints)
    max_bus = max(util.ints(input))
    max_i = constraints.index(max_bus)
    print('max', max_bus, max_i)
    t = max_bus - max_i
    while True:
        ok = True
        # print(t)
        for i, bus in enumerate(constraints):
            if bus is None:
                continue
            if (t+i) % bus:
                ok = False
                break
        if ok:
            print('Success at t', t)
            return t
        t += max_bus


def test():
    util.extended_gcd(17, 13)
    exit(0)
    assert(process('17,x,13,19') == 3417)
    # assert(process('7,13,x,x,59,x,31,19') == 1068781)
    exit(0)

test()


with open('input.txt', 'r') as f:
    input = f.read().splitlines()[1]
    val = process(input)
    print('Part 1:', val)
