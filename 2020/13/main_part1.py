import sys
sys.path.append('../..')
import util


def process(input):
    time, busses = input.strip().splitlines()
    time = int(time)
    busses = [int(b) for b in busses.split(',') if b != 'x']
    options = {}
    for bus in busses:
        div = int(time/bus)
        next_bus = bus * div + bus
        options[bus] = next_bus
    print(options)
    fastest_bus = util.key_with_min_value(options)
    return fastest_bus * (options[fastest_bus] - time)


def test():
    test_input = '''
939
7,13,x,x,59,x,31,19
'''
    assert(process(test_input) == 295)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
