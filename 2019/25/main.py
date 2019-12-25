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

def convert_to_ascii(text):
    a = [ord(x) for x in text]
    a.append(ord('\n'))
    return a

def get_inputs(script):
    inputs = deque([convert_to_ascii(cmd) for cmd in script])
    inputs = deque(util.flatten(inputs))
    return inputs

def get_cmds():
    cmds = []
    cmds.append('east') # south, west
    # Crew Quarters
    # cmds.append('take photons')
    cmds.append('north')
    # Warp drive maintenance
    cmds.append('west')
    # Science Lab
    cmds.append('north')
    # Arcade
    cmds.append('take whirled peas')
    cmds.append('west')
    # Storage
    # cmds.append('take giant electromagnet')
    cmds.append('west')
    # Hot Chocolate Fountain
    cmds.append('take astronaut ice cream')
    cmds.append('south')
    # Security Checkpoint
    cmds.append('south')  # too heavy
    return cmds


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)
    cmds = get_cmds()
    inputs = get_inputs(cmds)
    computer.run(program_code, inputs)
    status_map = process_outputs(computer.outputs)
    render(status_map)
