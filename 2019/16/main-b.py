import sys
sys.path.append('..')
import util
import numpy as np
import math

base_pattern = np.array([0, 1, 0, -1])
pattern_cache = {}

def decode_signal(input, num_phases):
    offset = input[0:7]
    print('offset', offset)
    input = input * 10000
    result = run_fft(input, num_phases)
    return result


def run_fft(input, num_phases, offset=0):
    digits = np.array([int(x) for x in input.strip()])
    for i in range(num_phases):
        digits = calc_fft(digits)
        if not i % 10:
            print('Finished iteration', i)
    result = ''.join([str(x) for x in digits])
    result = result[offset:offset+8]
    print('result', result)
    return result


def calc_fft(digits):
    # print('digits ', digits)
    outputs = []
    for i, digit in enumerate(digits):
        pattern = np.array(get_pattern(i+1))
        # print('pattern', pattern)
        pattern = np.tile(pattern, math.ceil(len(digits)/len(pattern)))
        pattern = pattern[:len(digits)]
        # print('pattern', pattern)
        mult = digits * pattern
        # print('mult', mult)
        output = abs(sum(mult))
        output = ones_digit(output)
        outputs.append(output)
        # print(output)
        if not i % 100 and i > 0:
            print('Finished digit', i)
    # print(outputs)
    return np.array(outputs)


def get_pattern(i):
    if i not in pattern_cache:
        pattern = np.repeat(base_pattern, i)
        pattern = np.append(pattern[1:], pattern[0])
        pattern_cache[i] = pattern
    return pattern_cache[i]


def ones_digit(value):
    digits = [x for x in str(value)]
    return int(digits[-1])


def test():
    # assert get_pattern(2) == np.array([0, 1, 1, 0, 0, -1, -1, 0])
    # assert get_pattern(3) == [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0]
    assert run_fft('12345678', 4) == '01029498'
    assert run_fft('80871224585914546619083218645595', 100) == '24176176'
    exit(0)
test()

def test2():
    assert decode_signal('03036732577212944063491565474664', 100) == '84462026'
    exit(0)
test2()


with open('input.txt', 'r') as f:
    input = f.read()
    run_fft(input, 100)
