from itertools import permutations

def process_input(file_input):
    file_input = file_input.split(',')
    file_input = [int(x) for x in file_input]
    return file_input

curr_inputs = {}

def run_program(id, code, phase):
    global curr_inputs
    pc = 0
    input_i = 0
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
            if input_i == 0:
                code[dst] = phase
                # print('  amp input', id, phase)
            else:
                code[dst] = curr_inputs[id]
                # print('  amp input', id, curr_inputs[id])
            input_i += 1
            pc += 2
        if op == 4:  # Output
            output_param = code[src0]
            if id == 4:
                curr_inputs[0] = output_param
                # print('  amp output', id, output_param)
            else:
                curr_inputs[id+1] = output_param
                # print('  amp output', id, output_param)
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
    global curr_inputs
    curr_inputs = {0: 0, 1: None, 2: None, 3: None, 4: None}
    # while True:
    codes = [code.copy() for _ in range(0,5)]
    while True:
        i = 0
        for phase in sequence:
            output = run_program(i, codes[i], phase)
            print('amp', i, 'phase', phase, 'input', curr_inputs[i], 'output', output)
            i += 1
    print('loop', output)
    print(output)
    return output



def test(code):
    assert run_amps([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [9,8,7,6,5]) == 139629729
    # assert run_amps([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], [9,7,8,5,6]) == 18216


with open('input.txt', 'r') as f:
    program_code = process_input(f.read())
    test(program_code)
    exit(1)

    # perms = permutations(range(0,5))
    perms = permutations(range(5,10))
    max = 0
    for p in perms:
        print(p)
        value = run_amps(program_code.copy(), list(p))
        if value > max:
            max = value
    print('max', max)

# Not 43520
