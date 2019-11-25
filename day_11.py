def increment(input):
    chars = [x for x in input]
    chars[-1] = increment_char(chars[-1])
    i = 1
    for x in reversed(chars):
        if x == '{':
            chars[-i] = 'a'
            chars[-i-1] = increment_char(chars[-i-1])
        i += 1
    output = ''.join(chars)
    # print(output)
    return output

def increment_char(char):
    return chr(ord(char) + 1)

def check_conditions(input):
    if num_pairs(input) < 2:
        return False
    if has_bad_letters(input):
        return False
    if not has_straight(input):
        return False
    return True

def has_bad_letters(input):
    if 'i' in input:
        return True
    if 'o' in input:
        return True
    if 'l' in input:
        return True
    return False

def has_straight(input):
    for x in input:
        y = increment_char(x)
        z = increment_char(y)
        straight = x + y + z
        if straight in input and y != '{' and z != '{':
            return True
    return False

def num_pairs(input):
    pairs = {}
    last = ''
    for x in input:
        if x == last:
            pairs[x] = True
        last = x
    return len(pairs.keys())


if __name__ == '__main__':
    # input = 'hepxcrrq'
    input = 'hepxxyzz'
    while True:
        input = increment(input)
        ok = check_conditions(input)
        print(input, ok)
        if ok:
            break
