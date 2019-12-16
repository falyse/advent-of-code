import sys
sys.path.append('..')
import util
import numpy as np
import math

base_pattern = np.array([0, 1, 0, -1])
pattern_cache = {}

def decode_signal(input, num_phases, repeat=10000, override_offset=None):
    offset = int(input[0:7])
    if override_offset is not None:
        offset = override_offset
    print('offset', offset)
    input = input * repeat
    input = input[offset:]
    result = run_fft(input, num_phases, offset)
    return result


def run_fft(input, num_phases, offset=0):
    global pattern_cache
    pattern_cache = {}
    digits = np.array([int(x) for x in input.strip()])
    for i in range(num_phases):
        print('Starting phase', i)
        # digits = calc_fft_accel(digits, offset)
        digits = run_phase(digits)
        # if not i % 10:
        #     print('Finished phase', i)
    result = ''.join([str(x) for x in digits])
    # Extract result digits at offset
    result = result[0:8]
    print('result', result)
    return result


def run_phase(digits):
    outputs = []
    val = 0
    for i,d in enumerate(reversed(digits)):
        val += d
        outputs.append(ones_digit(abs(val)))
        # print(outputs)
    outputs = list(reversed(outputs))
    print('outputs', outputs)
    return outputs


# def calc_fft_accel(digits, offset):
#     # print('digits ', digits)
#     outputs = [ones_digit(abs(sum(digits[j:]))) for j in range(len(digits))]
#     print('outputs', outputs)
#     return outputs


def calc_fft_accel(digits, offset):
    # print('digits ', digits)
    outputs = []
    for j in range(len(digits)):
        vals = digits[j:]
        total = abs(sum(vals))
        print('  j', j, ':', vals, ' :  sum', total)
        outputs.append(ones_digit(total))
    print('results', outputs)
    return outputs


def get_full_pattern(i, length):
    if i not in pattern_cache:
        pattern = get_pattern(i)
        pattern = np.tile(pattern, math.ceil(length/len(pattern)))
        pattern = pattern[:length]
        pattern_cache[i] = pattern
    return pattern_cache[i]


def get_pattern(i):
    pattern = np.repeat(base_pattern, i)
    pattern = np.append(pattern[1:], pattern[0])
    return pattern


def ones_digit(value):
    digits = [x for x in str(value)]
    return int(digits[-1])


def test():
    # assert get_pattern(2) == np.array([0, 1, 1, 0, 0, -1, -1, 0])
    # assert get_pattern(3) == [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0]
    assert run_fft('12345678', 4) == '01029498'
    assert run_fft('80871224585914546619083218645595', 100) == '24176176'
    exit(0)
# test()

def test2():
    assert run_fft('1234'*1, 1, offset=0) == '2574'
    assert run_fft('1234'*2, 1, offset=0) == '40800974'
    # assert run_fft('1234'*3, 1, offset=0) == '65261574'

    assert decode_signal('1234', 1, repeat=1, override_offset=0, accel=False) == '2574'
    assert decode_signal('1234', 1, repeat=2, override_offset=0, accel=False) == '40800974'
    exit(0)
# test2()

def test3():
    # assert decode_signal('1234', 1, repeat=5, override_offset=12) == '09740974'
    # assert decode_signal('1234', 2, repeat=5, override_offset=12) == '00140014'
    # assert decode_signal('1234', 2, repeat=5, override_offset=11) == '40014001'

    assert decode_signal('03036732577212944063491565474664', 100) == '84462026'
    exit(0)
# test3()


with open('input.txt', 'r') as f:
    input = f.read().strip()
    # run_fft(input, 100)
    decode_signal(input, 100)


# Fork from main-d
