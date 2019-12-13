import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
import util


def test():
    pass


test()

with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
#     input = f.readlines()
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)

    # program_code[0] = 2
    computer.initialize(program_code, 0)
    done = False
    while not done:
        done = computer.execute()
        outputs = computer.outputs
        print(outputs)

    items = []
    item = []
    i = 0
    for o in outputs:
        item.append(o)
        if not (i+1) % 3:
            items.append(item)
            item = []
        i += 1
    print(items)

    cnt = 0
    for x, y, id in items:
        if id == 2:
            cnt += 1
        print('x', x, 'y', y, 'id', id)

    print('cnt', cnt)
    assert cnt == 344

#not 181