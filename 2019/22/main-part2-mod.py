import sys
sys.path.append('..')
import util


def shuffle(input, size, iterations, index):
    increment_mul = 1
    offset_diff = 0

    for line in input.strip().splitlines():
        if 'new' in line:
            increment_mul *= -1
            offset_diff += increment_mul
        if 'increment' in line:
            n = util.ints(line)[0]
            increment_mul *= pow(int(n), size - 2, size)
        if 'cut' in line:
            n = util.ints(line)[0]
            offset_diff += int(n) * increment_mul
    increment_mul %= size
    offset_diff %= size

    increment = pow(increment_mul, iterations, size)
    offset = offset_diff * (1 - increment) * pow((1 - increment_mul) % size, size - 2, size)
    offset %= size

    card = (offset + index * increment) % size
    return card


with open('input.txt', 'r') as f:
    input = f.read()

    # https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/
    # https://github.com/mcpower/adventofcode/blob/501b66084b0060e0375fc3d78460fb549bc7dfab/2019/22/a-improved.py
    size = 119315717514047
    iterations = 101741582076661
    index = 2020

    card = shuffle(input, size, iterations, index)
    print('Card at index', index, 'is', card)
    assert card == 71345377301237
