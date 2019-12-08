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


def merge(layers, width, height):
    image = [['2' for x in range(width)] for y in range(height)]
    print(image)
    for r in range(height):
        for c in range(width):
            for l in layers:
                if l[r][c] != '2' and image[r][c] == '2':
                    image[r][c] = l[r][c]
    print(image)
    return image


def render(image):
    for row in image:
        text = ''.join(row)
        text = text.replace('0', ' ')
        text = text.replace('1', '#')
        print(text)


def test():
    # Part 1
    layers = process_data('123456789012', 3, 2)
    count_zeros(layers)
    # assert layers[0] == [123, 456]
    # Part 2
    # layers = process_data('0222112222120000', 2, 2)
    # image = merge(layers, 2, 2)


test()
exit(0)

with open('input.txt', 'r') as f:
    input = f.read().strip()
    layers = process_data(input, width, height)
    image = merge(layers, width, height)
    render(image)
