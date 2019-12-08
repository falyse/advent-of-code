def process_data(input, width, height):
    layers = []
    while len(input) > 0:
        layer = []
        for h in range(height):
            row = input[0:width]
            input = input[width:]
            layer.append(row)
        layers.append(layer)
    return layers


def count_digits(layers):
    min = None
    val = None
    for layer in layers:
        num_zeros = 0
        num_ones = 0
        num_twos = 0
        for row in layer:
            num_zeros += row.count('0')
            num_ones += row.count('1')
            num_twos += row.count('2')
        if min is None or num_zeros < min:
            min = num_zeros
            val = num_ones * num_twos
    return val


def merge(layers, width, height):
    image = [['2' for x in range(width)] for y in range(height)]
    for y in range(height):
        for x in range(width):
            for l in layers:
                if l[y][x] != '2' and image[y][x] == '2':
                    image[y][x] = l[y][x]
    return image


def render(image):
    print()
    for row in image:
        text = ''.join(row)
        text = text.replace('0', ' ')
        text = text.replace('1', '#')
        print(text)


def test():
    # Part 1
    layers = process_data('123456789012', 3, 2)
    assert layers == [['123', '456'], ['789', '012']]
    assert count_digits(layers) == 1
    # Part 2
    layers = process_data('0222112222120000', 2, 2)
    image = merge(layers, 2, 2)
    assert image == [['0', '1'], ['1', '0']]


test()

with open('input.txt', 'r') as f:
    width = 25
    height = 6

    input = f.read().strip()
    layers = process_data(input, width, height)

    # Part 1
    digit_val = count_digits(layers)
    print('Digit check:', digit_val)
    assert digit_val == 1224

    # Part 2
    image = merge(layers, width, height)
    render(image)
