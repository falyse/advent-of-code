def process_input(input):
    input = input.split(',')
    input = [int(x) for x in input]
    print(input)
    return input

def get_param_modes(cmd_bits):
    modes = [int(x) for x in cmd_bits]
    modes = list(reversed(modes))
    # Add zeros for unspecified modes
    while len(modes) < 2:
        modes.append(0)
    # print('modes', modes)
    return modes

def decode_cmd(cmd):
    cmd = str(cmd)
    op = int(cmd[-2:])  # Last 2 bits are opcode
    modes = get_param_modes(cmd[:-2])  # Other bits are parameter modes
    return op, modes


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    input = process_input(f.read())

    pc = 0
    input_param = 5
    output_param = None
    while True:
        cmd = input[pc]
        op, modes = decode_cmd(cmd)
        print('pc', pc, 'cmd', cmd, 'op', op)
        # Halt
        if op == 99:
            break
        if op == 1:
            src0 = input[pc+1]
            src1 = input[pc+2]
            dst = input[pc+3]
            # print('src0', src0, 'src1', src1, 'dst', dst)
            s0 = src0 if modes[0] == 1 else input[src0]
            s1 = src1 if modes[1] == 1 else input[src1]
            input[dst] = s0 + s1
            pc += 4
        if op == 2:
            src0 = input[pc+1]
            src1 = input[pc+2]
            dst = input[pc+3]
            # print('src0', src0, 'src1', src1, 'dst', dst)
            s0 = src0 if modes[0] == 1 else input[src0]
            s1 = src1 if modes[1] == 1 else input[src1]
            input[dst] = s0 * s1
            # print('s0', s0, 's1', s1)
            pc += 4
        if op == 3:
            dst = input[pc+1]
            input[dst] = input_param
            pc += 2
        if op == 4:
            src0 = input[pc+1]
            s0 = src0 if modes[0] == 1 else input[src0]
            output_param = s0
            pc += 2
        if op == 5:
            src0 = input[pc+1]
            src1 = input[pc+2]
            s0 = src0 if modes[0] == 1 else input[src0]
            s1 = src1 if modes[1] == 1 else input[src1]
            if s0:
                pc = s1
            else:
                pc += 3
        if op == 6:
            src0 = input[pc+1]
            src1 = input[pc+2]
            s0 = src0 if modes[0] == 1 else input[src0]
            s1 = src1 if modes[1] == 1 else input[src1]
            if not s0:
                pc = s1
            else:
                pc += 3
        if op == 7:
            src0 = input[pc+1]
            src1 = input[pc+2]
            dst = input[pc+3]
            # print('src0', src0, 'src1', src1, 'dst', dst)
            s0 = src0 if modes[0] == 1 else input[src0]
            s1 = src1 if modes[1] == 1 else input[src1]
            input[dst] = 1 if s0 < s1 else 0
            pc += 4
        if op == 8:
            src0 = input[pc+1]
            src1 = input[pc+2]
            dst = input[pc+3]
            # print('src0', src0, 'src1', src1, 'dst', dst)
            s0 = src0 if modes[0] == 1 else input[src0]
            s1 = src1 if modes[1] == 1 else input[src1]
            input[dst] = 1 if s0 == s1 else 0
            pc += 4
        if pc >= len(input):
            break
    # print(input)
    # output = input[0]
    print('Done', output_param)

    if output_param != 9006327:
        print('Refactor error')
        exit(1)


