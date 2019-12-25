import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util
from itertools import combinations

def render(status_map, display=True):
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
    if display:
        print(text)
    return text

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

def gather_items_cmds():
    cmds = []
    cmds.append('west')
    # Holodeck
    cmds.append('take hypercube')
    # cmds.append('south')
    # Corridor
    cmds.append('west')
    # Stables
    cmds.append('take space law space brochure')
    cmds.append('west')
    # Sick Bay
    # cmds.append('take infinite loop')
    # cmds.append('west')
    # Navigation
    # cmds.append('take escape pod')
    cmds.append('north')
    # Gift wrapping center
    cmds.append('take shell')
    cmds.append('west')
    # Engineering
    cmds.append('take mug')
    cmds.append('south')
    # Kitchen
    cmds.append('take festive hat')

    # Backtrack to Hull Breach
    cmds.append('north')
    cmds.append('east')
    cmds.append('south')
    cmds.append('east')
    cmds.append('east')
    cmds.append('east')

    cmds.append('south')
    # Hallway
    cmds.append('east')
    # Passages
    cmds.append('take boulder')
    cmds.append('west')
    # Hallway
    cmds.append('west')
    # Observatory
    # cmds.append('take molten lava')
    # cmds.append('drop boulder')

    # Backtrack to Hull Breach
    cmds.append('east')
    cmds.append('east')
    cmds.append('west')
    cmds.append('north')

    cmds.append('east')
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

    return cmds

def get_item_cmds(all_items, held_items):
    cmds = []
    for item in all_items:
        if item in held_items:
            cmds.append('take %s' % item)
        else:
            cmds.append('drop %s' % item)
    cmds.append('inv')
    cmds.append('south')
    return cmds


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)

    cmds = gather_items_cmds()
    inputs = get_inputs(cmds)
    computer.run(program_code, inputs)

    items = [
        'boulder',
        'shell',
        'mug',
        'hypercube',
        'space law space brochure',
        'festive hat',
        'astronaut ice cream',
        'whirled peas']

    for i in reversed(range(1,8)):
        print('\nTesting 8 choose', i, '\n')
        combos = combinations(items, i)
        for combo in list(combos):
            print('Combo:', combo)
            cmds = get_item_cmds(items, combo)
            inputs.clear()
            inputs.extend(get_inputs(cmds))
            computer.reset_outputs()
            computer.execute()
            status_map = process_outputs(computer.outputs)
            text = render(status_map, False)
            if 'lighter' in text:
                print('  lighter')
            if 'heavier' in text:
                print('  heavier')
            if 'ejected back to the checkpoint' not in text:
                print(text)
                exit(0)


# Items in your inventory:
# - hypercube
# - festive hat
# - shell
# - astronaut ice cream
