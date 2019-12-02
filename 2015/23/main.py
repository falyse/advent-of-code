pc = 0
a = 1
b = 0

def decode(instr):
    global pc, a, b
    print('Processing', instr)
    cmd, args = instr.split(' ', 1)
    if ',' in args:
        reg, offset = args.split(', ')
    else:
        reg = args
    # Get src reg
    r = 0
    if reg == 'a':
        r = a
    if reg == 'b':
        r = b

    if cmd == 'hlf':
        r = int(r / 2)
    if cmd == 'tpl':
        r = r * 3
    if cmd == 'inc':
        r += 1
    if cmd == 'jmp':
        pc += int(reg) - 1
    if cmd == 'jie':
        if not r % 2:
            pc += int(offset) - 1
    if cmd == 'jio':
        if r == 1:
            pc += int(offset) - 1
    pc += 1

    # Update dest reg
    if args[0] == 'a':
        a = r
    if args[0] == 'b':
        b = r

    display_state()


def display_state():
    print('  pc', pc, ', a', a, ', b', b)


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    input = f.readlines()
    input = [x.strip() for x in input]

    display_state()
    while 0 <= pc < len(input):
        decode(input[pc])
