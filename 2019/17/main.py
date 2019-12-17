import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
from collections import deque
import util
import operator
import re


class Routine():
    def __init__(self, main, a, b, c, debug):
        self.main = main
        self.a = a
        self.b = b
        self.c = c
        self.debug = 'y\n' if debug else 'n\n'
        self.debug = 'n\n'

    def __str__(self):
        return 'Routine: ' + ', '.join([str(x) for x in [self.main, self.a, self.b, self.c, self.debug]])

    def flatten(self):
        instr = []
        for cmd in self.main:
            instr.append(cmd)
            if cmd == 'A':
                instr.extend(text_to_list(self.a))
            if cmd == 'B':
                instr.extend(text_to_list(self.b))
            if cmd == 'C':
                instr.extend(text_to_list(self.c))
        return instr

    def get_intcode_inputs(self):
        inputs = []
        inputs.extend(self.main_to_ascii())
        inputs.extend(self.func_to_ascii(self.a))
        inputs.extend(self.func_to_ascii(self.b))
        inputs.extend(self.func_to_ascii(self.c))
        inputs.extend([ord(x) for x in self.debug])
        return inputs

    def main_to_ascii(self):
        instr = []
        for x in self.main:
            instr.append(ord(x))
            instr.append(ord(','))
        instr[-1] = ord('\n')
        print('Main length:', len(instr))
        return instr

    def func_to_ascii(self, text):
        pairs = text_to_pairs(text)
        instr = []
        for p in pairs:
            instr.append(ord(p[0]))
            instr.append(ord(','))
            for x in str(p[1]):
                instr.append(ord(x))
            instr.append(ord(','))
        instr[-1] = ord('\n')
        print('Func length:', len(instr))
        print(pairs)
        print(instr)
        return instr


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


def find_intersections(status_map):
    inters = []
    for loc in status_map:
        if is_intersection(status_map, loc):
            inters.append(loc)
            status_map[loc] = 'O'
    print('Intersections:', inters)
    return inters


def calc_param(inters):
    value = 0
    for int in inters:
        value += int[0] * int[1]
    return value


def is_intersection(status_map, loc):
    locs = [loc]
    for dir in range(1, 5):
        locs.append(get_next_loc(loc, dir))
    for l in locs:
        if l not in status_map or status_map[l] != '#':
            return False
    return True


def get_next_loc(loc, dir):
    moves = {1: (0,1),
             2: (0,-1),
             3: (-1,0),
             4: (1,0)}
    deltas = moves[dir]
    next_loc = tuple(map(operator.add, loc, deltas))
    return next_loc


def turn(dir, cmd):
    left_turn = {
        1: 4,
        2: 3,
        3: 1,
        4: 2
    }
    right_turn = {
        1: 3,
        2: 4,
        3: 2,
        4: 1
    }
    # print(cmd, 'turn from dir', dir)
    if cmd == 'L':
        return left_turn[dir]
    elif cmd == 'R':
        return right_turn[dir]
    else:
        print('Invalid turn command', cmd)
        exit(1)


def get_current_loc(status_map):
    for k,v in status_map.items():
        if v == '^':
            return k, 2
        if v == 'v':
            return k, 1
        if v == '<':
            return k, 3
        if v == '>':
            return k, 4


def text_to_status_map(text):
    loc = (0,0)
    status_map = {}
    for line in text.strip().splitlines():
        for char in line.strip():
            status_map[loc] = char
            loc = (loc[0] + 1, loc[1])
        loc = (0, loc[1] + 1)
    return status_map


def check_path(status_map, routine):
    status_map = status_map.copy()
    print('Checking path', routine)
    instr = routine.flatten()
    print(instr)
    loc, dir = get_current_loc(status_map)
    current_routine = 'M'
    for cmd in instr:
        if cmd in ['A', 'B', 'C']:
            current_routine = cmd
        elif cmd == 'L' or cmd == 'R':
            dir = turn(dir, cmd)
        else:
            for i in range(int(cmd)):
                loc = get_next_loc(loc, dir)
                status_map[loc] = current_routine
    render(status_map)
    print()
    if '#' in status_map.values():
        return False
    else:
        return True


def map_path(status_map):
    status_map = status_map.copy()
    _ = find_intersections(status_map)
    loc, dir = get_current_loc(status_map)
    path = find_path(status_map, loc, dir)
    return path


def find_path(status_map, loc, dir, path=[]):
    print('current loc', loc, 'dir', dir)
    print(path)
    # Continue straight as far as possible
    next_loc = get_next_loc(loc, dir)
    steps = 0
    while status_map.get(next_loc) in ['#', 'O']:
        steps += 1
        loc = next_loc
        if status_map[loc] != 'O':
            status_map[loc] = '+'
        next_loc = get_next_loc(loc, dir)
        # print('  continue to loc', loc, 'dir', dir, 'steps', steps)
    if steps > 0:
        path.append(steps)
    render(status_map)
    # If there is an open direction, turn and recurse
    open_dirs = get_open_dirs(status_map, loc)
    # print('open dirs', open_dirs)
    for open_dir in open_dirs:
        turn_cmd = None
        if open_dir == turn(dir, 'L'):
            turn_cmd = 'L'
        if open_dir == turn(dir, 'R'):
            turn_cmd = 'R'
        if turn_cmd is not None:
            path.append(turn_cmd)
            dir = open_dir
            find_path(status_map, loc, dir, path)
    return path


def get_open_dirs(status_map, loc):
    opens = []
    for d in range(1, 5):
        if status_map.get(get_next_loc(loc, d)) in ['#', 'O']:
            opens.append(d)
    return opens


def create_routine(path, complex=False):
    pairs = [(path[i], path[i+1]) for i in range(0, len(path), 2)]
    print(pairs)
    i = 0
    routine = None
    while routine is None:
        print('Iteration', i)
        if complex:
            routine = search_for_valid_routine_complex(path, i)
        else:
            routine = search_for_valid_routine(pairs, i)
        i += 1
        if i > 1000:
            print('Hit max iterations in routine search')
            exit(1)
    return routine


def search_for_valid_routine(pairs, skip):
    pair_limit = 5  # 20 mem size, each pair is turn, steps, and 2 commas
    pairs = pairs.copy()
    text = pairs_to_text(pairs)
    funcs = []
    func_num = 0
    cnt = 0
    for l in reversed(range(2, pair_limit)):
        sub_found = True
        while sub_found:
            sub_found = False
            for i in range(len(pairs)):
                if i+l > len(pairs):
                    continue
                sub_pairs = pairs[i:i+l]
                sub_text = pairs_to_text(sub_pairs)
                right_text = pairs_to_text(pairs[i + 2:])
                if 'f' in sub_text:
                    continue
                # print('checking sub', sub_text, 'in', right_text)
                if sub_text in right_text:
                    cnt += 1
                    if cnt <= skip:
                        print('  sub skip', sub_text, 'skip', skip, cnt)
                        continue
                    print('  sub match', sub_text)
                    funcs.append(sub_text)
                    text = re.sub(sub_text, 'f'+str(func_num), text)
                    pairs = text_to_pairs(text)
                    func_num += 1
                    # print('  new', text)
                    sub_found = True
    text = text.replace('f0', 'A')
    text = text.replace('f1', 'B')
    text = text.replace('f2', 'C')
    print(text)
    print(funcs)
    if 'R' in text or 'L' in text or len(funcs) > 3:
        print('  Invalid routine')
        return None
    r = Routine(text, *funcs, True)
    print(r)
    return r


def search_for_valid_routine_complex(path, skip):
    len_limit = 10
    text = path_to_text(path)
    funcs = []
    func_char = 'A'
    cnt = 0
    for l in reversed(range(1, len_limit)):
        sub_found = True
        while sub_found:
            sub_found = False
            for i in range(0, len(text)-l):
                sub_text = text[i:i+l]
                right_text = text[i+2:]
                if re.search(r'[A-C]', sub_text):
                    continue
                # print('checking sub', sub_text, 'in', right_text)
                if sub_text in right_text:
                    cnt += 1
                    if cnt <= skip:
                        print('  sub skip', sub_text, 'skip', skip, cnt)
                        continue
                    print('  sub match', sub_text)
                    funcs.append(sub_text)
                    if len(funcs) > 3:
                        return None
                    text = re.sub(sub_text, func_char, text)
                    func_char = chr(ord(func_char) + 1)
                    # print('  new', text)
                    sub_found = True
    text = text.replace('f0', 'A')
    text = text.replace('f1', 'B')
    text = text.replace('f2', 'C')
    print(text)
    print(funcs)
    if 'R' in text or 'L' in text or len(funcs) > 3:
        print('  Invalid routine')
        return None
    r = Routine(text, *funcs, True)
    print(r)
    return r


def pairs_to_text(pairs):
    text = ''
    for pair in pairs:
        text += pair[0] + str(pair[1])
    return text


def text_to_pairs(text):
    dirs = util.words(text)
    steps = util.ints(text)
    pairs = list(zip(dirs, steps))
    return pairs


def path_to_text(path):
    return ''.join([str(x) for x in path])


def text_to_path(text):
    return [x for x in text]


def text_to_list(text):
    pairs = text_to_pairs(text)
    return [val for pair in pairs for val in pair]


def test():
    # Test map
    status_map = text_to_status_map(r"""
#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####...... 
""")
    render(status_map)

    # Test check_path method with given example routine
    routine = Routine('ABCBAC', 'R8R8', 'R4R4R8', 'L6L2', True)
    # routine = Routine('A,B,C,B,A,C', 'R,8,R,8', 'R,4,R,4,R,8', 'L,6,L,2', True)
    assert check_path(status_map, routine) is True

    # Check routine to ascii inputs
    inputs = routine.get_intcode_inputs()
    exp_inputs = [65, 44, 66, 44, 67, 44, 66, 44, 65, 44, 67, 10,  # 12
                  82, 44, 56, 44, 82, 44, 56, 10,
                  82, 44, 52, 44, 82, 44, 52, 44, 82, 44, 56, 10,
                  76, 44, 54, 44, 76, 44, 50, 10,
                  121, 10]
    assert inputs == exp_inputs

    # Test map_path method
    path = map_path(status_map)
    # Double check that the path works
    routine = Routine(['A'], path, [], [], True)
    assert check_path(status_map, routine) is True

    # Divide the path into valid routine (main and 3 functions) and make sure that still works
    routine = create_routine(path)
    assert check_path(status_map, routine) is True

    exit(0)
# test()


with open('input.txt', 'r') as f:
    program_code = [int(x) for x in f.read().split(',')]
    computer = IntcodeComputer(debug=False)
    inputs = deque()

    # Part 1
    computer.run(program_code, inputs)
    status_map = process_outputs(computer.outputs)
    # render(status_map)
    inters = find_intersections(status_map)
    render(status_map)
    alignment_param = calc_param(inters)
    print('Alignment parameter:', alignment_param)
    assert alignment_param == 5724

    # Part 2
    # Get valid path routine
    path = map_path(status_map)
    routine = create_routine(path)
    assert check_path(status_map, routine) is True

    print(''.join([str(x) for x in path]))

    # Run routine
    program_code[0] = 2
    inputs = deque(routine.get_intcode_inputs())
    computer.run(program_code, inputs)
    status_map = process_outputs(computer.outputs[:-1])
    render(status_map)
    dust_collected = computer.outputs[-1]
    print(computer.outputs)
    print('Dust collected:', dust_collected)
    assert dust_collected == 732985

    exit(0)
    
    # Part 3 - More challenging scaffolding
    # https://www.reddit.com/r/adventofcode/comments/ebz338/2019_day_17_part_2_pathological_pathfinding/
    with open('pathological_pathfinding.txt', 'r') as f0:
        status_map = text_to_status_map(f0.read())
        render(status_map)
        path = map_path(status_map)
        routine = create_routine(path, complex=True)
        assert check_path(status_map, routine) is True

