import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util


def render(status_map):
    smap = status_map.copy()
    image = []
    x_vals, y_vals = zip(*smap.keys())
    for y in range(min(y_vals), max(y_vals)+1):
        row = []
        for x in range(min(x_vals), max(x_vals)+1):
            value = smap.get((x, y))
            if value is None:
                # print('None at', x, y)
                char = ' '
            else:
                char = value
            row.append(char)
        image.append(''.join(row))
    text = '\n'.join(image)
    print(text)

def process_outputs(outputs):
    status_map = {}
    loc = (0,0)
    for o in outputs:
        if o == 10:
            loc = (0, loc[1] + 1)
        else:
            status_map[loc] = chr(o)
            loc = (loc[0] + 1, loc[1])
    return status_map


def gen_script(cases):
    max_len = 15
    script = []

    # (!A || !C) && D
    script.append('NOT A J')
    script.append('NOT C T')
    script.append('OR T J')
    script.append('AND D J')
    # && G
    script.append('AND G J')

    # || (!I && D && E && F)
    script.append('NOT I T')
    script.append('AND D T')
    script.append('AND E T')
    script.append('AND F T')
    script.append('OR T J')

    script.append('NOT G T')
    script.append('AND D T')
    # script.append('AND F T')
    script.append('AND H T')
    script.append('OR T J')

    assert len(script) <= max_len

    script.append('RUN')
    return script

def convert_to_ascii(text):
    a = [ord(x) for x in text]
    a.append(ord('\n'))
    return a

def get_inputs(script):
    inputs = deque([convert_to_ascii(cmd) for cmd in script])
    inputs = deque(util.flatten(inputs))
    return inputs


# def gen_script(cases):
#     print(cases)
#     max_len = 15
#     script = []
#
#     script.append('NOT C J')
#     script.append('NOT D T')
#     script.append('AND T J')
#     # script.append('AND F J')
#
#     assert len(script) <= max_len
#
#     script.append('RUN')
#     return script

def extract_case(case_map):
    ground, jump_loc, fall_loc = parse_fall_output(case_map)
    letters = [chr(ord('A')+i) for i in range(9)]
    if jump_loc != -1:
        status = [x == '#' for x in ground[jump_loc:]]
        # status = [not x for x in status]
    else:
        status = [x == '#' for x in ground[fall_loc-2:]]
    # print(letters)
    # print(status)
    case = list(zip(letters, status))
    eqn = []
    for c in case:
        eqn.append(('' if c[1] else '!') + c[0])
    eqn = ' && '.join(eqn)
    print(eqn)
    return case


def parse_fall_output(case_map):
    jump_row = {}
    ground_row = {}
    for loc, char in case_map.items():
        if loc[1] == 1:
            jump_row[loc[0]] = char
        if loc[1] == 3:
            ground_row[loc[0]] = char
    jump_row = list(jump_row.values())
    ground_row = list(ground_row.values())
    if '@' in jump_row:
        jump_loc = jump_row.index('@')
    else:
        jump_loc = -1
    if '@' in ground_row:
        fall_loc = ground_row.index('@')
    else:
        fall_loc = -1
    # print('Jump loc', jump_loc, 'Fall loc', fall_loc)
    return ground_row, jump_loc, fall_loc

def merge(status_map):
    case_map = {}
    max_y = 0
    for loc, char in status_map.items():
        if loc[1] in [7,8,9,10]:
            case_map[(loc[0], loc[1]-7)] = char
        if loc[1] > max_y:
            max_y = loc[1]
    for loc, char in status_map.items():
        for y in range(7, max_y+1, 5):
            if loc[1] in [y, y+1, y+2, y+3]:
                if char == '@':
                    case_map[(loc[0], loc[1]-y)] = char
    print('=================')
    render(case_map)
    # print('=================')
    return case_map

def test():
    pass

test()


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)

    fell = True
    cases = []
    while fell:
        script = gen_script(cases)
        print('Script:', script)

        inputs = get_inputs(script)
        print(inputs)
        computer.run(program_code, inputs)
        print(computer.outputs)

        status_map = process_outputs(computer.outputs[:-1])
        render(status_map)
        fell = 'D' in status_map.values()

        print('\nNum instructions:', computer.instr_cnt)
        case_map = merge(status_map)
        cases.append(extract_case(case_map))
        # print('\n'.join([str(x) for x in cases]))
        fell = False

    damage_num = computer.outputs[-1]
    print('Damage number:', damage_num)
    # assert(damage_num) == 19357290

