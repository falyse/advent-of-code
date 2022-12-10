import sys
sys.path.append('../..')
import util


def process(input):
    instrs = input.strip().splitlines()
    mask = None
    mem = {}
    for instr in instrs:
        cmd, value = instr.split(' = ')
        if cmd == 'mask':
            mask = value
        else:
            pos = util.ints(cmd)[0]
            masked_value = get_masked_value(mask, pos)
            expanded_values = expand_value(masked_value)
            for v in expanded_values:
                mem[v] = int(value)
    total = sum([v for v in mem.values()])
    return total


def get_masked_value(mask, value):
    b = '{:036b}'.format(int(value))
    # print(b)
    # print(mask)
    b_list = [x for x in b]
    for i, bit in enumerate(mask):
        if bit != '0':
            b_list[i] = bit
    masked_bits = ''.join(b_list)
    # print(masked_bits)
    return masked_bits


def expand_value(masked_value):
    values = []
    num_x = masked_value.count('X')
    for i in range(0, 2**num_x):
        i_bin = '{:b}'.format(int(i)).zfill(num_x)
        j = 0
        expanded_value = ''
        for b in masked_value:
            if b == 'X':
                expanded_value += i_bin[j]
                j += 1
            else:
                expanded_value += b
        values.append(expanded_value)
    return values


def test():
    test_input = '''
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''
    assert(process(test_input) == 208)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 2:', val)
