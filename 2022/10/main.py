import sys
sys.path.append('../..')
import util


def process(input):
    history = get_history(input)
    return calc_signal(history)


def get_history(input):
    lines = input.strip().splitlines()
    history = {}
    cycle = 1
    x = 1
    for line in lines:
        history[cycle] = x
        if line == 'noop':
            cycle += 1
        elif 'addx' in line:
            val = int(line.split()[1])
            history[cycle + 1] = x
            cycle += 2
            x += val
        # print(cycle, line, 'x =', x)
    # print(history)
    return history


def calc_signal(history):
    points = [20, 60, 100, 140, 180, 220]
    score = sum([p * history[p] for p in points])
    print(score)
    return score


def display(input):
    history = get_history(input)
    out = []
    for j in range(6):
        row = ''
        for i in range(40):
            cycle = 40*j + i + 1
            x = history[cycle]
            # print(cycle, x)
            if x - 1 <= i <= x + 1:
                row += '#'
            else:
                row += '.'
            # print(row)
        out.append(row)
    text = '\n'.join(out)
    print(text)
    return text


def test():
    test_input = '''
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
    '''
#     test_input = '''
# noop
# addx 3
# addx -5
# '''
    assert(process(test_input) == 13140)
    assert(display(test_input) == '''
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
'''.strip())

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)

    print('Part 2:')
    display(input)  # ZFBFHGUP
