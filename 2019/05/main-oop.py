external_input = 5
external_output = None


def process_input(input):
    input = input.split(',')
    input = [int(x) for x in input]
    print(input)
    return input


def run_program():
    global pc
    pc = 0
    while True:
        cmd = program[pc]
        instr = decode_instr(cmd)
        if isinstance(instr, Halt):
            break

        instr.run()
        print(instr)
        pc = instr.update_pc(pc)

        if pc >= len(program):
            break
    print('\nDone. Output =', external_output)

    if external_output != 9006327:
        print('Refactor error')
        exit(1)


def decode_instr(cmd):
    op, modes = decode_cmd(cmd)
    instr = decode_op(op)
    instr.decode_params(modes)
    return instr


def decode_cmd(cmd):
    cmd = str(cmd)
    op = int(cmd[-2:])  # Last 2 bits are opcode
    modes = get_param_modes(cmd[:-2])  # Other bits are parameter modes
    return op, modes


def get_param_modes(cmd_bits):
    modes = [int(x) for x in cmd_bits]
    modes = list(reversed(modes))
    return modes


def decode_op(op):
    if op == 99:
        return Halt()
    if op == 1:
        return Add()
    if op == 2:
        return Multiply()
    if op == 3:
        return Input()
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
    print('ERROR: Unknown opcode', op)


class Instruction:
    def __init__(self):
        self.param_format = []
        self.params = []
        self.modes = []

    def __str__(self):
        return type(self).__name__ + ' ' + str(self.params)

    def decode_params(self, modes):
        self.modes = modes
        self.params = self.get_params()

    def get_params(self):
        params = []
        for i in range(len(self.param_format)):
            param = program[pc+i+1]
            if self.param_format[i] == 'src':
                # If the mode for this param was not specified, default to 0
                if len(self.modes) < i+1:
                    self.modes.append(0)
                param = self.resolve_param(param, self.modes[i])
            params.append(param)
        return params

    def resolve_param(self, value, mode):
        return value if mode == 1 else program[value]

    def run(self):
        pass

    def update_pc(self, pc):
        return pc + len(self.param_format) + 1


class Halt(Instruction):
    pass


class Add(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src', 'dst']

    def run(self):
        src0, src1, dst = self.params
        program[dst] = src0 + src1


class Multiply(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src', 'dst']

    def run(self):
        src0, src1, dst = self.params
        program[dst] = src0 * src1


class Input(Instruction):
    def __init__(self):
        self.param_format = ['dst']

    def run(self):
        dst, = self.params
        program[dst] = external_input


class Output(Instruction):
    def __init__(self):
        self.param_format = ['src']

    def run(self):
        global external_output
        src0, = self.params
        external_output = src0


class JumpIfTrue(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src']

    def update_pc(self, pc):
        src0, src1 = self.params
        if src0:
            return src1
        else:
            return super().update_pc(pc)


class JumpIfFalse(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src']

    def update_pc(self, pc):
        src0, src1 = self.params
        if not src0:
            return src1
        else:
            return super().update_pc(pc)


class LessThan(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src', 'dst']

    def run(self):
        src0, src1, dst = self.params
        program[dst] = 1 if src0 < src1 else 0


class Equals(Instruction):
    def __init__(self):
        self.param_format = ['src', 'src', 'dst']

    def run(self):
        src0, src1, dst = self.params
        program[dst] = 1 if src0 == src1 else 0


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    input = process_input(f.read())
    program = input.copy()
    run_program()