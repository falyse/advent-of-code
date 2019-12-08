from itertools import permutations

def process_input(file_input):
    file_input = file_input.split(',')
    file_input = [int(x) for x in file_input]
    return file_input


def run_program(code, input_params):
    pc = 0
    input_index = 0
    output_param = None
    while code[pc] != 99:  # Halt
        cmd = code[pc]
        op, modes = decode_cmd(cmd)
        # print('pc', pc, 'cmd', cmd, 'op', op, 'modes', modes)

        src0 = pc + 1 if modes[0] == 1 else code[pc + 1]
        src1 = pc + 2 if modes[1] == 1 else code[pc + 2]
        dst = code[pc + 3]
        # print('  src0', src0, 'src1', src1, 'dst', dst)

        if op == 1:  # Add
            code[dst] = code[src0] + code[src1]
            pc += 4
        if op == 2:  # Multiply
            code[dst] = code[src0] * code[src1]
            pc += 4
        if op == 3:  # Input
            dst = code[pc + 1]
            code[dst] = input_params[input_index]
            input_index += 1
            pc += 2
        if op == 4:  # Output
            output_param = code[src0]
            pc += 2
        if op == 5:  # Jump if true
            if code[src0]:
                pc = code[src1]
            else:
                pc += 3
        if op == 6:  # Jump if false
            if not code[src0]:
                pc = code[src1]
            else:
                pc += 3
        if op == 7:  # Less than
            code[dst] = 1 if code[src0] < code[src1] else 0
            pc += 4
        if op == 8:  # Equals
            code[dst] = 1 if code[src0] == code[src1] else 0
            pc += 4

    return output_param


def decode_cmd(cmd):
    cmd = str(cmd)
    op = int(cmd[-2:])
    modes = get_modes(cmd[:-2])  # Other bits are parameter modes
    # print(op, modes)
    return op, modes


def get_modes(p):
    modes = [int(x) for x in p]
    modes = list(reversed(modes))
    while len(modes) < 3:
        modes.append(0)
    return modes


def run_amps(code, sequence):
    input_signal = 0
    for phase in sequence:
        # print('amp phase', phase, 'input', input_signal)
        input_signal = run_program(code.copy(), [phase, input_signal])
    return input_signal


def test():
    assert run_amps([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0]) == 43210
    assert run_amps([3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4]) == 54321
    assert run_amps([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1,0,4,3,2]) == 65210


with open('input.txt', 'r') as f:
    program_code = process_input(f.read())
    # test()

    perms = permutations(range(5))
    max = 0
    for p in perms:
        print(p)
        value = run_amps(program_code.copy(), list(p))
        if value > max:
            max = value
        print('  output', value, 'max', max)
    print('Max value:', max)
    assert max == 21760

