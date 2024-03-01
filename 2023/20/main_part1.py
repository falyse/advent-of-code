import sys
sys.path.append('../..')
import util


def process(input):
    lines = input.strip().splitlines()
    return


def test():
    test_input = r'''
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
    '''
    assert(process(test_input) == 32000000)
    exit(0)

    test_input = r'''
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
    '''
    assert(process(test_input) == 11687500)

test()
exit(0)


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Result:', val)
