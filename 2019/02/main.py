with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    input = f.read()
    input = input.split(',')
    input = [int(x) for x in input]
    print(input)
    print('len', len(input))
    input[1] = 12
    input[2] = 2
    pc = 0
    stop = False
    while not stop:
        print('pc', pc)
        op = input[pc]
        print('op', op)
        if op == 99:
            break
        if op == 1:
            src0 = input[pc+1]
            src1 = input[pc+2]
            dst = input[pc+3]
            print('src0', src0, 'src1', src1, 'dst', dst)
            input[dst] = input[src0] + input[src1]
        if op == 2:
            src0 = input[pc+1]
            src1 = input[pc+2]
            dst = input[pc+3]
            input[dst] = input[src0] * input[src1]
        pc += 4
        if pc >= len(input):
            break
    print(input)


