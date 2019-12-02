goal = 19690720
# 144000 wrong
with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    input = f.read()
    input = input.split(',')
    input = [int(x) for x in input]
    input_orig = input.copy()
    # print(input)
    for noun in range(0,100):
        for verb in range(0,100):
            print(noun, verb)
            print(input)
            input = input_orig.copy()
            print(input)
            input[1] = noun
            input[2] = verb
            pc = 0
            stop = False
            while not stop:
                # print('pc', pc)
                op = input[pc]
                # print('op', op)
                if op == 99:
                    break
                if op == 1:
                    src0 = input[pc+1]
                    src1 = input[pc+2]
                    dst = input[pc+3]
                    # print('src0', src0, 'src1', src1, 'dst', dst)
                    input[dst] = input[src0] + input[src1]
                if op == 2:
                    src0 = input[pc+1]
                    src1 = input[pc+2]
                    dst = input[pc+3]
                    input[dst] = input[src0] * input[src1]
                pc += 4
                if pc >= len(input):
                    break
            # print(input)
            output = input[0]
            if output == goal:
                print('Done', noun, verb)
                print(100*noun+verb)
                exit(0)


