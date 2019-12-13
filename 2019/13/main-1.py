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

    computer.initialize(program_code, 0)
    done = False
    while not done:
        done = computer.execute()
        outputs = computer.outputs
        print(outputs)

    i = 0
    cnt = 0
    for o in outputs:
        if not (i+1) % 3:
            print(i, o)
            if o == 2:
                cnt += 1
        i += 1
    print(cnt)

    # items = []
    # for i in range(0, (len(outputs)-2)//3):
    #     items.append((outputs[i], outputs[i+1], outputs[i+2]))
    # print(items)
    #
    # cnt = 0
    # for x, y, id in items:
    #     if id == 2:
    #         cnt += 1
    #     print('x', x, 'y', y, 'id', id)
    #
    # print('cnt', cnt)

#not 181