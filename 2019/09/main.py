def process_input(file_input):
    file_input = file_input.split(',')
    file_input = [int(x) for x in file_input]
    return file_input


def init_memory(code):
    for _ in range(2000):
        code.append(0)
    return code


def run_program(code, input_param):
    pc = 0
    relative_base = 0
    output_param = None
    code = init_memory(code)
    debug = []
    while code[pc] != 99:  # Halt
        print('pc', pc, ':', code[pc:pc+4])
        cmd = code[pc]
        op, modes = decode_cmd(cmd)
        # print('pc', pc, 'cmd', cmd, ': op', op, 'modes', modes)

        src0 = pc + 1 if modes[0] == 1 else code[pc + 1]
        src1 = pc + 2 if modes[1] == 1 else code[pc + 2]
        dst = code[pc + 3] if pc + 3 < len(code) else None
        # print('  src0', src0, 'src1', src1, 'dst', dst)

        if modes[0] == 2:
            src0 += relative_base
        if modes[1] == 2:
            src1 += relative_base
        if modes[2] == 2:
            dst += relative_base
        # print('  src0', src0, 'src1', src1, 'dst', dst)

        if op == 1:  # Add
            code[dst] = code[src0] + code[src1]
            debug.append('code[%d] = code[%d] + code[%d]' % (dst, src0, src1))
            debug.append('%d = %d + %d' % (code[dst], code[src0], code[src1]))
            pc += 4
        if op == 2:  # Multiply
            code[dst] = code[src0] * code[src1]
            debug.append('code[%d] = code[%d] * code[%d]' % (dst, src0, src1))
            debug.append('%d = %d * %d' % (code[dst], code[src0], code[src1]))
            pc += 4
        if op == 3:  # Input
            dst = code[pc + 1]
            if modes[0]:
                dst += relative_base
            code[dst] = input_param
            debug.append('code[%d] = input' % dst)
            debug.append('%d = %d' % (code[dst], input_param))
            pc += 2
        if op == 4:  # Output
            output_param = code[src0]
            debug.append('output = code[%d]' % src0)
            debug.append('output = %d' % output_param)
            pc += 2
        if op == 5:  # Jump if true
            if code[src0]:
                pc = code[src1]
            else:
                pc += 3
            debug.append('jump to pc code[%d] if code[%d]' % (src1, src0))
            debug.append('jump to pc %d if %d' % (code[src1], code[src0]))
        if op == 6:  # Jump if false
            if not code[src0]:
                pc = code[src1]
            else:
                pc += 3
            debug.append('jump to pc code[%d] if not code[%d]' % (src1, src0))
            debug.append('jump to pc %d if not %d' % (code[src1], code[src0]))
        if op == 7:  # Less than
            code[dst] = 1 if code[src0] < code[src1] else 0
            debug.append('code[%d] = code[%d] < code[%d]' % (dst, src0, src1))
            debug.append('%d = %d < %d' % (code[dst], code[src0], code[src1]))
            pc += 4
        if op == 8:  # Equals
            code[dst] = 1 if code[src0] == code[src1] else 0
            debug.append('code[%d] = code[%d] == code[%d]' % (dst, src0, src1))
            debug.append('%d = %d == %d' % (code[dst], code[src0], code[src1]))
            pc += 4
        if op == 9:  # Relative base offset
            relative_base += code[src0]
            debug.append('relative_base += code[%d]' % (src0))
            debug.append('relative_base += %d -> %d' % (code[src0], relative_base))
            pc += 2

        print('  ', '\n   '.join(debug[-2:]))

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


def test():
    assert run_program([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], 1)
    assert len(str(run_program([1102,34915192,34915192,7,4,7,99,0], 1))) == 16
    assert run_program([104,1125899906842624,99], 1) == 1125899906842624
    assert run_program([103,1985,109,2000,109,19,204,-34,99], 555) == 555


# test()

with open('input.txt', 'r') as f:
    program_code = process_input(f.read())

    # Part 1
    output = run_program(program_code.copy(), 1)
    print('Part 1 output =', output)
    assert output == 3512778005

    # Part 2
    output = run_program(program_code.copy(), 2)
    print('Part 2 output =', output)
    assert output == 35920
