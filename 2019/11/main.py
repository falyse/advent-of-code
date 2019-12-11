import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util
import threading

grid = {}
grid[0] = {0: 1}
rx = 0
ry = 0
dir = 0
rnum = 1
# input_param = 0

def init_memory(code):
    for _ in range(2000):
        code.append(0)
    return code


def run_program(code):
    pc = 0
    relative_base = 0
    output_params = []
    output_index = 0
    code = init_memory(code)
    debug = []
    while code[pc] != 99:  # Halt
        # print('pc', pc, ':', code[pc:pc+4])
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
            input_param = grid[rx][ry]
            code[dst] = input_param
            # print(' input', input_param)
            debug.append('code[%d] = input' % dst)
            debug.append('%d = %d' % (code[dst], input_param))
            pc += 2
        if op == 4:  # Output
            output_params.append(code[src0])
            # print(' output', code[src0])
            debug.append('output = code[%d]' % src0)
            debug.append('output = %d' % output_params[-1])
            output_index += 1
            if not output_index % 2:
                run_robot(output_params[-2:])
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

        # print('  ', '\n   '.join(debug[-2:]))

    return output_params



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


def run_robot(outputs):
    global rnum
    global grid
    global rx
    global ry
    global dir
    # global input_param
    # input_param = grid[rx][ry]
    color = outputs[0]
    next_dir = outputs[1]
    if rx == 36:
        print('x,y', rx, ry, 'orig', grid[rx][ry], 'new', color, 'rnum', rnum)
    grid[rx][ry] = color
    # print('x,y', rx, ry, 'color', grid[rx][ry], 'rnum', rnum)
    if next_dir == 0:
        dir -= 90
    else:
        dir += 90
    if dir <= -180:
        dir += 360
    if dir > 180:
        dir -= 360
    # print('  dir', dir)
    if dir == 0:
        ry += 1
    elif dir == 90:
        rx += 1
    elif dir == 180:
        ry -= 1
    elif dir == -90:
        rx -= 1
    else:
        print('Unknown dir', dir)
        exit(1)
    if not rx in grid:
        grid[rx] = {}
    if not ry in grid[rx]:
        grid[rx][ry] = 0
        rnum += 1
    return grid[rx][ry]




def test():
    pass


test()

with open('input.txt', 'r') as f:
    # with open('test.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]

    run_program(program_code)
    print('Final rnum', rnum)

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    min_x, max_x = util.min_max(grid.keys())
    for row in grid.keys():
        a, b = util.min_max(grid[row].keys())
        if a < min_y:
            min_y = a
        if b > max_y:
            max_y = b

    # for ix in range(max_x):
    #     if len(grid[ix]) < min_y:
    #         min_y = len(grid[ix])
    #     if len(grid[ix]) > max_y:
    #         max_y = len(grid[ix])
    print('maxes', min_x, max_x, min_y, max_y)
    temp = util.make_grid(abs(min_y), max_x, fill = ' ')
    for ix in range(min_x, max_x+1):
        # for iy in range(max_y+2, min_y-1, -1):
        for iy in range(0, -6, -1):
            print('ix', ix, 'iy', iy)
            # if ix in grid.keys() and iy in grid[ix].keys():
            #     print('here')
            #     temp[iy][ix] = '#'
            # else:
            #     temp[iy][ix] = '#'
            try:
                if grid[ix][iy] == 1:

                    temp[abs(iy)][ix] = '#'
                # print('asdf', ix, iy)
            except:
                pass
    print(util.grid_to_text(temp, map={}))

# not 6
# not 7
# not 39

# not main.py URCAFLCY