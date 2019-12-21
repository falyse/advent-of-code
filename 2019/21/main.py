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


def gen_script():
    max_len = 15
    T = False
    J = False
    script = []
    # script.append('NOT A J')  # hole at 1

    # script.append('NOT A J')  # hole at 1
    script.append('NOT D T')
    script.append('NOT T J')  # no hole at 4
    # script.append('AND T J')

    # script.append('NOT B J')  # hole at 2
    # script.append('NOT C T')
    # script.append('NOT T T')  # no hole at 3
    # script.append('AND T J')

    # A || (B && !C)
    # script.append('NOT A J')
    # script.append('NOT B T')
    # script.append('NOT T T')
    # script.append('AND T J')
    # script.append('NOT A T')
    # script.append('NOT T T')
    # script.append('OR T J')
    # && !(ABCD)
    # script.append('AND B T')
    # script.append('AND C T')
    # script.append('AND D T')
    # script.append('NOT T T')
    # script.append('AND T J')

    script.append('NOT A J')
    script.append('NOT C T')
    script.append('OR T J')
    script.append('AND D J')

    assert len(script) <= max_len

    script.append('WALK')
    return script

def convert_to_ascii(text):
    a = [ord(x) for x in text]
    a.append(ord('\n'))
    return a


def test():
    pass

test()


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)

    script = gen_script()
    print('Script:', script)

    inputs = deque([convert_to_ascii(cmd) for cmd in script])
    inputs = deque(util.flatten(inputs))
    print(inputs)
    computer.initialize(program_code, inputs)

    computer.execute()
    print(computer.outputs)
    status_map = process_outputs(computer.outputs[:-1])
    render(status_map)
    damage_num = computer.outputs[-1]
    print('Damage number:', damage_num)
    assert(damage_num) == 19357290

