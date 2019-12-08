width = 25
height = 6

def process_data(input, width, height):
    layers = []
    while len(input) > 0:
        layer = []
        for h in range(height):
            row = input[0:width]
            input = input[width:]
            print('row', row)
            print('input', input)
            layer.append(row)
        layers.append(layer)
    print(layers)
    return layers

def count_zeros(layers):
    print('asdf0')
    min = None
    val = None
    for l in layers:
        num_zeros = 0
        num_ones = 0
        num_twos = 0
        for row in l:
            num_zeros += sum([1 for x in row if x == '0'])
            num_ones += sum([1 for x in row if x == '1'])
            num_twos += sum([1 for x in row if x == '2'])
        print('zeros', num_zeros, num_ones, num_twos)
        if min is None or num_zeros < min:
            min = num_zeros
            val = num_ones * num_twos
    print(val)

def test():
    width = 3
    height = 2
    input = '123456789012'
    layers = process_data(input, width, height)
    count_zeros(layers)
    # assert layers[0] == [123, 456]
    exit(0)


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    input = f.read().strip()
    # test()
    layers = process_data(input, width, height)
    count_zeros(layers)

# not 0