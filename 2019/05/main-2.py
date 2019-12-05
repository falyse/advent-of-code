def process_input(input):
    input = input.split(',')
    input = [int(x) for x in input]
    print(input)
    return input


def run_program():
    global pc
    pc = 0
    input_param = 5
    output_param = None
    while True:
        cmd = program[pc]
        op, modes = decode_cmd(cmd)
        print('pc', pc, 'cmd', cmd, 'op', op)
        if op == 99:  # Halt instruction
            break
        instr = decode_op(op, input_param)
        instr.run(modes)
        pc = instr.update_pc(pc)
        if hasattr(instr, 'output_param'):
            output_param = instr.output_param
        if pc >= len(program):
            break
    print('Done. Output =', output_param)

    if output_param != 9006327:
        print('Refactor error')
        exit(1)


def get_param_modes(cmd_bits):
    global modes
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
    def get_params(self, modes):
        params = []
        for i in range(len(self.param_format)):
            param = program[pc+i+1]
            if self.param_format[i] == 'src':
                param = self.resolve_param(param, modes[i])
            params.append(param)
        return params

    def resolve_param(self, value, mode):
        return value if mode == 1 else program[value]

    def run(self, modes):
        pass

    def update_pc(self, pc):
        return pc + len(self.param_format) + 1


class Add(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src', 'dst']

    def run(self, modes):
        src0, src1, dst = self.get_params(modes)
        program[dst] = src0 + src1


class Multiply(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src', 'dst']

    def run(self, modes):
        src0, src1, dst = self.get_params(modes)
        program[dst] = src0 * src1


class Input(Instruction):
    def __init__(self, input_param):
        self.input_param = input_param
        self.param_format = ['dst']

    def run(self, modes):
        dst, = self.get_params(modes)
        program[dst] = self.input_param


class Output(Instruction):
    def __init__(self):
        self.param_format = ['src']

    def run(self, modes):
        src0, = self.get_params(modes)
        self.output_param = src0


class JumpIfTrue(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src']

    def update_pc(self, pc):
        src0, src1 = self.get_params(modes)
        if src0:
            return src1
        else:
            return super().update_pc(pc)


class JumpIfFalse(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src']

    def update_pc(self, pc):
        src0, src1 = self.get_params(modes)
        if not src0:
            return src1
        else:
            return super().update_pc(pc)


class LessThan(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src', 'dst']

    def run(self, modes):
        src0, src1, dst = self.get_params(modes)
        program[dst] = 1 if src0 < src1 else 0


class Equals(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src', 'dst']

    def run(self, modes):
        src0, src1, dst = self.get_params(modes)
        program[dst] = 1 if src0 == src1 else 0


with open('input.txt', 'r') as f:
    # with open('test.txt', 'r') as f:
    input = process_input(f.read())
    program = input.copy()
    run_program()
