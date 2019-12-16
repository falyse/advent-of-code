def decode_signal(input, num_phases, repeat=10000, override_offset=None):
    offset = int(input[0:7])
    if override_offset is not None:
        offset = override_offset
    print('offset', offset)
    input = input * repeat
    # Everything before the offset can be ignored, because it will be zero
    input = input[offset:]
    result = run_fft(input, num_phases)
    return result


def run_fft(input, num_phases):
    digits = [int(x) for x in input.strip()]
    for i in range(num_phases):
        print('Starting phase', i)
        digits = run_phase(digits)
    result = ''.join([str(x) for x in digits])
    # Extract result digits at offset
    result = result[0:8]
    return result


def run_phase(digits):
    # o[0] = d[0]
    # o[1] = d[0] + d[1]         =  o[0] + d[1]
    # o[2] = d[0] + d[1] + d[2]  =  o[1] + d[2]
    outputs = []
    val = 0
    for d in reversed(digits):
        val += d
        outputs.append(val)
        # print(outputs)
    outputs = [ones_digit(abs(x)) for x in reversed(outputs)]
    print('outputs', outputs)
    return outputs


def ones_digit(value):
    digits = [x for x in str(value)]
    return int(digits[-1])


def test():
    assert decode_signal('1234', 2, repeat=5, override_offset=11) == '40014001'
    # assert decode_signal('1234', 2, repeat=5, override_offset=12) == '00140014'

    assert decode_signal('03036732577212944063491565474664', 100) == '84462026'
    exit(0)
# test()


with open('input.txt', 'r') as f:
    input = f.read().strip()
    result = decode_signal(input, 100)
    print('Result:', result)
    assert result == '41402171'
