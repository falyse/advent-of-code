from itertools import permutations
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


def run_program(code, id, phase, input_signals):
    pc = 0
    first_input = True
    output_param = None
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
            # For the first input, use the phase
            # Otherwise, get the current input signal value for this amplifier (waiting if necessary)
            if first_input:
                code[dst] = phase
                first_input = False
            else:
                code[dst] = input_signals[id].get_value()
            pc += 2
        if op == 4:  # Output
            output_param = code[src0]
            # Set the next amplifier's input signal to this output value
            out_id = 0 if id == 4 else id + 1
            input_signals[out_id].set_value(output_param)
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
    # Create a shared list of input signals
    input_signals = [InputSignal() for _ in range(len(sequence))]
    input_signals[0].set_value(0)  # Send 0 to first amplifier once
    # Start a thread to run the code on each amplifier in parallel
    threads = []
    for id, phase in enumerate(sequence):
        x = threading.Thread(target=run_program, args=(code.copy(), id, phase, input_signals))
        threads.append(x)
        x.start()
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    return input_signals[0].get_value()


def test():
    assert run_amps([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [9,8,7,6,5]) == 139629729
    assert run_amps([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], [9,7,8,5,6]) == 18216


with open('input.txt', 'r') as f:
    program_code = process_input(f.read())
    # test()

    # Part 1
    # perms = permutations(range(0,5))

    # Part 2
    perms = permutations(range(5,10))
    max = 0
    for p in perms:
        print(p)
        value = run_amps(program_code.copy(), list(p))
        if value > max:
            max = value
        print('  output', value, 'max', max)
    print('Max value:', max)
    assert max == 69816958
