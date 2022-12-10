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
            masked_value = get_masked_value(mask, value)
            mem[pos] = masked_value
    total = sum([v for v in mem.values()])
    return total


def get_masked_value(mask, value):
    b = '{:036b}'.format(int(value))
    print(b)
    print(mask)
    b_list = [x for x in b]
    for i, bit in enumerate(mask):
        if bit != 'X':
            b_list[i] = bit
    masked_bits = ''.join(b_list)
    print(masked_bits)
    masked_value = int(masked_bits, base=2)
    print(masked_value)
    return masked_value


def test():
    test_input = '''
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
'''
    assert(process(test_input) == 165)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
