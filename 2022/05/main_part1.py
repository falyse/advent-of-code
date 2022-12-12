import sys
sys.path.append('../..')
import util


def process(input):
    state, instrs = parse_input(input)
    final = execute_moves(state, instrs)
    return final


def parse_input(input):
    state_str, instr = input.strip('\n\n').split('\n\n')
    state = parse_state(state_str)
    print(state)
    instrs = instr.strip().splitlines()
    return state, instrs


def parse_state(state_str):
    lines = state_str.splitlines()
    rows, nums = lines[:-1], lines[-1]
    num_cols = int(nums.strip()[-1])
    boxes = []
    for i in range(num_cols):
        boxes.append([])
        for row in reversed(rows):
            char = row[4*i+1]
            if char != ' ':
                boxes[i].append(char)
    return boxes


def execute_moves(state, instrs):
    for instr in instrs:
        state = execute_instr(state, instr)
    final = ''.join([col[-1] for col in state])
    return final


def execute_instr(state, instr):
    print(instr)
    repeat, fr, to = util.ints(instr)
    for _ in range(repeat):
        state = do_move(state, fr, to)
        print(state)
    return state


def do_move(state, fr, to):
    char = state[fr-1].pop()
    state[to-1].append(char)
    return state


def test():
    test_input = '''
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
    '''
    assert(process(test_input) == 'CMZ')

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
    assert(val == 'BWNCQRMDB')
