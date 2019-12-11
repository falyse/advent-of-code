import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util
import threading



def process_input(file_input):
    file_input = file_input.split(',')
    file_input = [int(x) for x in file_input]
    return file_input


class InputSignal:
    def __init__(self):
        self.ready = threading.Event()
        self.ready.set()
        self.value = None

    def set_value(self, value):
        self.value = value
        self.ready.set()

    def get_value(self):
        self.ready.wait()
        self.ready.clear()
        return self.value

    def peek_value(self):
        return self.value


def run_program(code, input_signal, output_signals):
    pc = 0
    out_index = 0
    while code[pc] != 99:  # Halt
        cmd = code[pc]
        op, modes = decode_cmd(cmd)
        # print('pc', pc, 'cmd', cmd, 'op', op, 'modes', modes)

        src0 = pc + 1 if modes[0] == 1 else code[pc + 1]
        src1 = pc + 2 if modes[1] == 1 else code[pc + 2]
        dst = code[pc + 3] if pc + 3 < len(code) else None
        # print('  src0', src0, 'src1', src1, 'dst', dst)

        if op == 1:  # Add
            code[dst] = code[src0] + code[src1]
            pc += 4
        if op == 2:  # Multiply
            code[dst] = code[src0] * code[src1]
            pc += 4
        if op == 3:  # Input
            dst = code[pc + 1]
            # Otherwise, get the current input signal value for this amplifier (waiting if necessary)
            print('wait for input')
            code[dst] = input_signal.get_value()
            print('  got input')
            pc += 2
        if op == 4:  # Output
            output_signals.append(InputSignal())
            output_signals[-1].set_value(code[src0])
            print('set output', out_index)
            # print(output_signals)
            out_index += 1
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

    return output_signals


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


def run_robot(input_signal, output_signals):
    grid = {}
    x = 0
    y = 0
    dir = 0
    num = 0
    while True:
        if not x in grid:
            grid[x] = {}
        if not y in grid[x]:
            grid[x][y] = 0
            num += 1
        input_signal.set_value(grid[x][y])
        print('x,y', x, y, ': input', input_signal.get_value(), 'outputs', [o.peek_value() for o in output_signals])
        color = output_signals[-2].get_value()
        grid[x][y] = color
        next_dir = output_signals[-1].get_value()
        if next_dir == 0:
            dir -= 90
        else:
            dir += 90
        if dir > 180:
            dir -= 360
        print('  dir', dir)
        if dir == 0:
            y += 1
        if dir == 90:
            x += 1
        if dir == 180:
            y -= 1
        if dir == -90:
            x -= 1




def run_code(code):
    # Create a shared list of input signals
    input_signal = InputSignal()
    output_signals = []
    # input_signal.set_value(0)
    # Start a thread to run the code on each amplifier in parallel
    t0 = threading.Thread(target=run_program, args=(code.copy(), input_signal, output_signals))
    t0.start()

    t1 = threading.Thread(target=run_robot, args=(input_signal, output_signals))
    t1.start()

    t0.join()
    print('Done')
    return output_signals



def test():
    pass


test()

with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]

    run_code(program_code)


