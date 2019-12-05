def process_input(file_input):
    file_input = file_input.split(',')
    file_input = [int(x) for x in file_input]
    return file_input


def run_program(code, input_param):
    pc = 0
    output_param = None
    while code[pc] != 99:
        cmd = code[pc]
        op = int(str(cmd)[-2:])
        modes = get_modes(str(cmd)[:-2])
        # print('pc', pc, 'cmd', cmd, 'op', op, 'modes', modes)

        src0 = pc + 1 if modes[0] == 1 else code[pc + 1]
        src1 = pc + 2 if modes[1] == 1 else code[pc + 2]
        dst = code[pc + 3]
        # print('  src0', src0, 'src1', src1, 'dst', dst)

        if op == 99: # Halt
            break
        if op == 1:  # Add
            code[dst] = code[src0] + code[src1]
            pc += 4
        if op == 2:  # Multiply
            code[dst] = code[src0] * code[src1]
            pc += 4
        if op == 3:  # Input
            dst = code[pc + 1]
            code[dst] = input_param
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

        if pc >= len(code):
            break
    print('\nDone. Program input =', input_param, '-> output =', output_param)

    if (input_param == 1 and output_param != 15508323 or
        input_param == 5 and output_param != 9006327):
        print('Refactor error')
        exit(1)
    return output_param


def get_modes(p):
    modes = [int(x) for x in p]
    modes = list(reversed(modes))
    while len(modes) < 3:
        modes.append(0)
    return modes


def test():
    # position mode: input is equal to 8; output 1 (if it is) or 0 (if it is not)
    assert run_program([3,9,8,9,10,9,4,9,99,-1,8], 8) == 1
    assert run_program([3,9,8,9,10,9,4,9,99,-1,8], 0) == 0
    # position mode: input is less than equal to 8; output 1 (if it is) or 0 (if it is not)
    assert run_program([3,9,7,9,10,9,4,9,99,-1,8], 7) == 1
    assert run_program([3,9,7,9,10,9,4,9,99,-1,8], 9) == 0
    # immediate mode: input is equal to 8; output 1 (if it is) or 0 (if it is not)
    assert run_program([3,3,1108,-1,8,3,4,3,99,0,0], 8) == 1
    assert run_program([3,3,1108,-1,8,3,4,3,99,0,0], 0) == 0
    # immediate mode: input is less than equal to 8; output 1 (if it is) or 0 (if it is not)
    assert run_program([3,3,1107,-1,8,3,4,3,99,0,0], 7) == 1
    assert run_program([3,3,1107,-1,8,3,4,3,99,0,0], 9) == 0
    # jump tests
    assert run_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0) == 0
    assert run_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 1) == 1
    assert run_program([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0) == 0
    assert run_program([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 1) == 1
    # Use an input instruction to ask for a single number.
    # Then output 999 if the input value is below 8,
    # output 1000 if the input value is equal to 8,
    # or output 1001 if the input value is greater than 8.
    example = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
               1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
               999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    assert run_program(example, 7) == 999
    assert run_program(example, 8) == 1000
    assert run_program(example, 9) == 1001


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
#     test()
    program_code = process_input(f.read())
    run_program(program_code.copy(), 1)
    run_program(program_code.copy(), 5)

