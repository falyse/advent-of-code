def process_input(file_input):
    file_input = file_input.split(',')
    file_input = [int(x) for x in file_input]
    return file_input


def run_program(code):
    pc = 0
    while code[pc] != 99:  # Halt
        op = code[pc]
        src0 = code[pc + 1]
        src1 = code[pc + 2]
        dst = code[pc + 3]
        # print('pc', pc, 'op', op, 'src0', src0, 'src1', src1, 'dst', dst)

        if op == 1:  # Add
            code[dst] = code[src0] + code[src1]
            pc += 4
        if op == 2:  # Multiply
            code[dst] = code[src0] * code[src1]
            pc += 4

    return code


def test():
    assert run_program([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70, 2,3,11,0, 99, 30,40,50]
    assert run_program([1,0,0,0,99]) == [2,0,0,0,99]
    assert run_program([2,3,0,3,99]) == [2,3,0,6,99]
    assert run_program([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    assert run_program([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]


test()

with open('input.txt', 'r') as f:
    program_code = process_input(f.read())

    # Part 1
    code = program_code.copy()
    code[1] = 12
    code[2] = 2
    code = run_program(code)
    print('Part 1 output', code[0])
    assert code[0] == 3166704

    # Part 2
    goal = 19690720
    for noun in range(0,100):
        for verb in range(0,100):
            code = program_code.copy()
            code[1] = noun
            code[2] = verb
            code = run_program(code)
            if code[0] == goal:
                result = 100*noun+verb
                print('Part 2 result', result)
                assert result == 8018
                break
