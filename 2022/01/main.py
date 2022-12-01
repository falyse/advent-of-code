import sys
sys.path.append('../..')
import util


def process(input, num=1):
    elves = input.strip().split('\n\n')
    calories = [sum(util.ints(e)) for e in elves]
    ordered = list(reversed(sorted(calories)))
    top = ordered[:num]
    total = sum(top)
    return total


def test():
    test_input = '''
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
    '''
    assert(process(test_input) == 24000)
    assert(process(test_input, 3) == 45000)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)

    val = process(input, 3)
    print('Part 2:', val)