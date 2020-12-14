import sys
sys.path.append('../..')
import util


def process(input):
    constraints = [None if b == 'x' else int(b) for b in input.split(',')]
    print(constraints)
    first_bus = constraints[0]
    t = first_bus
    incr = first_bus
    matched_i = 0
    while True:
        ok = True
        print(t)
        for i, bus in enumerate(constraints):
            if bus is None:
                continue
            if (t+i) % bus:
                ok = False
                break
            elif i > matched_i:
                incr *= bus
                matched_i = i
        # print('  matched_i', matched_i, 'incr', incr)
        if ok:
            print('Success at t', t)
            return t
        t += incr


def test():
    assert(process('17,x,13,19') == 3417)
    assert(process('7,13,x,x,59,x,31,19') == 1068781)
    exit(0)

# test()


with open('input.txt', 'r') as f:
    input = f.read().splitlines()[1]
    val = process(input)
    print('Part 1:', val)
