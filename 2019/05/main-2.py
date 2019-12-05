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


def decode_op(op, input_param):
    if op == 1:
        return Add()
    if op == 2:
        return Multiply()
    if op == 3:
        return Input(input_param)
    if op == 4:
        return Output()
    if op == 5:
        return JumpIfTrue()
    if op == 6:
        return JumpIfFalse()
    if op == 7:
        return LessThan()
    if op == 8:
        return Equals()


class Instruction:
    def get_params(self):
        return [input[pc+i] for i in range(1, self.num_params + 1)]

    def resolve_param(self, value, mode):
        return value if mode == 1 else input[value]

    def run(self, modes):
        pass

    def update_pc(self, pc):
        return pc + self.num_params + 1


class Add(Instruction):
    def __init__(self):
        self.num_params = 3

    def run(self, modes):
        src0, src1, dst = self.get_params()
        # print('src0', src0, 'src1', src1, 'dst', dst)
        s0 = self.resolve_param(src0, modes[0])
        s1 = self.resolve_param(src1, modes[1])
        input[dst] = s0 + s1


class Multiply(Instruction):
    def __init__(self):
        self.num_params = 3

    def run(self, modes):
        src0, src1, dst = self.get_params()
        # print('src0', src0, 'src1', src1, 'dst', dst)
        s0 = self.resolve_param(src0, modes[0])
        s1 = self.resolve_param(src1, modes[1])
        input[dst] = s0 * s1


class Input(Instruction):
    def __init__(self, input_param):
        self.num_params = 1
        self.input_param = input_param

    def run(self, modes):
        dst, = self.get_params()
        input[dst] = self.input_param


class Output(Instruction):
    def __init__(self):
        self.num_params = 1

    def run(self, modes):
        src0, = self.get_params()
        s0 = self.resolve_param(src0, modes[0])
        self.output_param = s0


class JumpIfTrue(Instruction):
    def __init__(self):
        self.num_params = 2

    def update_pc(self, pc):
        src0, src1 = self.get_params()
        s0 = self.resolve_param(src0, modes[0])
        s1 = self.resolve_param(src1, modes[1])
        if s0:
            return s1
        else:
            return super().update_pc(pc)


class JumpIfFalse(Instruction):
    def __init__(self):
        self.num_params = 2

    def update_pc(self, pc):
        src0, src1 = self.get_params()
        s0 = self.resolve_param(src0, modes[0])
        s1 = self.resolve_param(src1, modes[1])
        if not s0:
            return s1
        else:
            return super().update_pc(pc)


class LessThan(Instruction):
    def __init__(self):
        self.num_params = 3

    def run(self, modes):
        src0, src1, dst = self.get_params()
        # print('src0', src0, 'src1', src1, 'dst', dst)
        s0 = self.resolve_param(src0, modes[0])
        s1 = self.resolve_param(src1, modes[1])
        input[dst] = 1 if s0 < s1 else 0


class Equals(Instruction):
    def __init__(self):
        self.num_params = 3

    def run(self, modes):
        src0, src1, dst = self.get_params()
        # print('src0', src0, 'src1', src1, 'dst', dst)
        s0 = self.resolve_param(src0, modes[0])
        s1 = self.resolve_param(src1, modes[1])
        input[dst] = 1 if s0 == s1 else 0


with open('input.txt', 'r') as f:
    # with open('test.txt', 'r') as f:
    global input
    input = process_input(f.read())

    pc = 0
    input_param = 5
    output_param = None
    while True:
        cmd = input[pc]
        op, modes = decode_cmd(cmd)
        print('pc', pc, 'cmd', cmd, 'op', op)
        if op == 99:  # Halt instruction
            break
        instr = decode_op(op, input_param)
        instr.run(modes)
        pc = instr.update_pc(pc)
        if hasattr(instr, 'output_param'):
            output_param = instr.output_param
        if pc >= len(input):
            break
    print('Done. Output =', output_param)

    if output_param != 9006327:
        print('Refactor error')
        exit(1)


