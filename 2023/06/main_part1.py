import sys
sys.path.append('../..')
import util


def process(input):
    lines = input.strip().splitlines()
    times = util.ints(lines[0])
    distances = util.ints(lines[1])
    total = 1
    for i in range(len(times)):
        num = num_wins(times[i], distances[i])
        print(i, num)
        total *= num
    return total


def num_wins(time, distance):
    num = 0
    for t in range(time):
        d = t * (time - t)
        if d > distance:
            num += 1
    return num


def test():
    assert(num_wins(7, 9) == 4)

    test_input = '''
Time:      7  15   30
Distance:  9  40  200

    '''
    assert(process(test_input) == 288)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
