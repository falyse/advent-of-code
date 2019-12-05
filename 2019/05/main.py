def get_modes(p):
    modes = [int(x) for x in p]
    modes = list(reversed(modes))
    print('modes', modes)
    return modes


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    input = f.read()
    input = input.split(',')
    input = [int(x) for x in input]
    input_orig = input.copy()
    print(input)

    pc = 0
    stop = False
    input_param = 1
    output_param = None
    while not stop:
        cmd = input[pc]
        print('pc', pc, 'cmd', cmd)
        op = int(str(cmd)[-2:])
        modes = get_modes(str(cmd)[:-2])
        print('op', op)
        if op == 99:
            break
        if op == 1:
            src0 = input[pc+1]
            src1 = input[pc+2]
            dst = input[pc+3]
            # print('src0', src0, 'src1', src1, 'dst', dst)
            if len(modes) == 0:
                modes = [0, 0]
            if len(modes) == 1:
                modes.append(0)
            s0 = src0 if modes[0] == 1 else input[src0]
            s1 = src1 if modes[1] == 1 else input[src1]
            input[dst] = s0 + s1
            pc += 4
        if op == 2:
            src0 = input[pc+1]
            src1 = input[pc+2]
            dst = input[pc+3]
            # print('src0', src0, 'src1', src1, 'dst', dst)
            if len(modes) == 0:
                modes = [0, 0]
            if len(modes) == 1:
                modes.append(0)
            s0 = src0 if modes[0] == 1 else input[src0]
            s1 = src1 if modes[1] == 1 else input[src1]
            input[dst] = s0 * s1
            # print('s0', s0, 's1', s1)
            pc += 4
        if op == 3:
            dst = input[pc+1]
            # s0 = input_param if modes[0] == 1 else input[input_param]
            input[dst] = input_param
            pc += 2
        if op == 4:
            src0 = input[pc+1]
            if len(modes) == 0:
                modes = [0]
            s0 = src0 if modes[0] == 1 else input[src0]
            output_param = s0
            pc += 2
        if pc >= len(input):
            break
    # print(input)
    # output = input[0]
    print('Done', output_param)


