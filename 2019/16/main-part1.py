def run_fft(input, num_phases):
    digits = [int(x) for x in input.strip()]
    for i in range(num_phases):
        print('Starting phase', i)
        digits = calc_fft(digits)
    result = ''.join([str(x) for x in digits])
    result = result[0:8]
    print('result', result)
    return result


def calc_fft(digits):
    # print(digits)
    outputs = []
    for i, digit in enumerate(digits):
        pattern = get_pattern(i+1)
        # print(pattern)
        mult = []
        for j, digit in enumerate(digits):
            k = j % len(pattern)
            # print('digit', digit, 'pattern', pattern[k])
            mult.append(digit * pattern[k])
        # print(mult)
        output = abs(sum(mult))
        output = ones_digit(output)
        outputs.append(output)
        # print(output)
    # print(outputs)
    return outputs


def get_pattern(i):
    base_pattern = [0, 1, 0, -1]
    pattern = []
    for p in base_pattern:
        for j in range(i):
            pattern.append(p)
    p0 = pattern[0]
    pattern = pattern[1:]
    pattern.append(p0)
    return pattern


def ones_digit(value):
    digits = [x for x in str(value)]
    return int(digits[-1])


def test():
    assert get_pattern(2) == [0, 1, 1, 0, 0, -1, -1, 0]
    assert get_pattern(3) == [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0]
    assert run_fft('12345678', 4) == '01029498'
    assert run_fft('80871224585914546619083218645595', 100) == '24176176'
    # exit(0)
# test()


with open('input.txt', 'r') as f:
    input = f.read()
    result = run_fft(input, 100)
    print('Result:', result)
    assert result == '22122816'
