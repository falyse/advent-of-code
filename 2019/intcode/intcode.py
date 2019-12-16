from collections import deque
from copy import deepcopy


class IntcodeComputer:
    def __init__(self, debug=False):
        self.debug = debug

    def initialize(self, program, inputs):
        self.pc = 0
        self.relative_base = 0
        self.mem = program.copy()
        self.mem += [0] * 10000
        if type(inputs) == int:
            self.inputs = deque([inputs])
        else:
            self.inputs = inputs
        self.outputs = []

    def run(self, program, inputs=deque()):
        self.initialize(program, inputs)
        self.execute()
        if len(self.outputs):
            return self.outputs[0]
        else:
            return self.mem[0]

    def execute(self):
        trace = []
        while self.mem[self.pc] != 99:  # Halt
            if self.debug:
                print('pc', self.pc, ':', self.mem[self.pc:self.pc+4])
            cmd = self.mem[self.pc]
            op, modes = self.decode_cmd(cmd)
            # print('pc', self.pc, 'cmd', cmd, ': op', op, 'modes', modes)

            src0 = self.pc + 1 if modes[0] == 1 else self.mem[self.pc + 1]
            src1 = self.pc + 2 if modes[1] == 1 else self.mem[self.pc + 2]
            dst = self.mem[self.pc + 3] if self.pc + 3 < len(self.mem) else None
            # print('  src0', src0, 'src1', src1, 'dst', dst)

            if modes[0] == 2:
                src0 += self.relative_base
            if modes[1] == 2:
                src1 += self.relative_base
            if modes[2] == 2:
                dst += self.relative_base
            # print('  src0', src0, 'src1', src1, 'dst', dst)

            if op == 1:  # Add
                self.mem[dst] = self.mem[src0] + self.mem[src1]
                trace.append('mem[%d] = mem[%d] + mem[%d]' % (dst, src0, src1))
                trace.append('%d = %d + %d' % (self.mem[dst], self.mem[src0], self.mem[src1]))
                self.pc += 4
            if op == 2:  # Multiply
                self.mem[dst] = self.mem[src0] * self.mem[src1]
                trace.append('mem[%d] = mem[%d] * mem[%d]' % (dst, src0, src1))
                trace.append('%d = %d * %d' % (self.mem[dst], self.mem[src0], self.mem[src1]))
                self.pc += 4
            if op == 3:  # Input
                if len(self.inputs) <= 0:
                    return False
                input_value = self.inputs.popleft()
                dst = self.mem[self.pc + 1]
                if modes[0]:
                    dst += self.relative_base
                self.mem[dst] = input_value
                trace.append('mem[%d] = input' % dst)
                trace.append('%d = %d' % (self.mem[dst], input_value))
                self.pc += 2
            if op == 4:  # Output
                self.outputs.append(self.mem[src0])
                trace.append('output = mem[%d]' % src0)
                trace.append('output = %d' % self.outputs[-1])
                self.pc += 2
            if op == 5:  # Jump if true
                if self.mem[src0]:
                    self.pc = self.mem[src1]
                else:
                    self.pc += 3
                trace.append('jump to pc mem[%d] if mem[%d]' % (src1, src0))
                trace.append('jump to pc %d if %d' % (self.mem[src1], self.mem[src0]))
            if op == 6:  # Jump if false
                if not self.mem[src0]:
                    self.pc = self.mem[src1]
                else:
                    self.pc += 3
                trace.append('jump to pc mem[%d] if not mem[%d]' % (src1, src0))
                trace.append('jump to pc %d if not %d' % (self.mem[src1], self.mem[src0]))
            if op == 7:  # Less than
                self.mem[dst] = 1 if self.mem[src0] < self.mem[src1] else 0
                trace.append('mem[%d] = mem[%d] < mem[%d]' % (dst, src0, src1))
                trace.append('%d = %d < %d' % (self.mem[dst], self.mem[src0], self.mem[src1]))
                self.pc += 4
            if op == 8:  # Equals
                self.mem[dst] = 1 if self.mem[src0] == self.mem[src1] else 0
                trace.append('mem[%d] = mem[%d] == mem[%d]' % (dst, src0, src1))
                trace.append('%d = %d == %d' % (self.mem[dst], self.mem[src0], self.mem[src1]))
                self.pc += 4
            if op == 9:  # Relative base offset
                self.relative_base += self.mem[src0]
                trace.append('relative_base += mem[%d]' % (src0))
                trace.append('relative_base += %d -> %d' % (self.mem[src0], self.relative_base))
                self.pc += 2

            if self.debug:
                print('  ', '\n   '.join(trace[-2:]))
        return True

    def get_mem(self, size=None):
        if size:
            return self.mem[:size]
        else:
            return self.mem

    def decode_cmd(self, cmd):
        cmd = str(cmd)
        op = int(cmd[-2:])
        modes = self.get_modes(cmd[:-2])  # Other bits are parameter modes
        # print(op, modes)
        return op, modes

    def get_modes(self, p):
        modes = [int(x) for x in p]
        modes = list(reversed(modes))
        while len(modes) < 3:
            modes.append(0)
        return modes

    def set_inputs(self, inputs):
        self.inputs = inputs

    def reset_outputs(self):
        self.outputs = []

    def clone(self):
        return deepcopy(self)

