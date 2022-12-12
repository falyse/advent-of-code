import sys
sys.path.append('../..')
import util


def process(input, packet_len):
    input = input.strip()
    for i in range(packet_len, len(input)):
        sub = input[i-packet_len:i]
        if not string_has_duplicates(sub):
            return i


def string_has_duplicates(sub):
    d = {}
    for c in sub:
        if c in d:
            return True
        d[c] = None
    return False


def test():
    assert(process('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4) == 7)
    assert(process('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input, 4)
    print('Part 1:', val)
    val = process(input, 14)
    print('Part 2:', val)
