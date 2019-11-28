def get_dims(dims):
    return [int(d) for d in dims.split('x')]

def get_area(dims):
    l, w, h = get_dims(dims)
    sides = [l*w, w*h, h*l]
    surface = 2 * sum(sides)
    extra = min(sides)
    total = surface + extra
    # print('surface', surface, ', extra', extra, ', total', total)
    return total

def get_ribbon(dims):
    l, w, h = get_dims(dims)
    perimeters = [2*l+2*w, 2*w+2*h, 2*h+2*l]
    wrap = min(perimeters)
    bow = l * w * h
    total = wrap + bow
    print('wrap', wrap, ', bow', bow, ', total', total)
    return total

with open('input.txt', 'r') as f:
    input = f.readlines()
    # input = ['2x3x4', '1x1x10']
    area = sum([get_area(x) for x in input])
    print('Total Area:', area)
    ribbon = sum([get_ribbon(x) for x in input])
    print('Total Ribbon:', ribbon)
