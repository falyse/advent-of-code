def match(value):
    password = str(value)
    return (len(password) == 6 and
            has_double(password) and
            increasing(password))


def has_double(password):
    last_char = None
    for char in password:
        if char == last_char:
            if not (char + char + char) in password:  # Part 2
                return True
        last_char = char
    return False


def increasing(password):
    last_char = None
    for x in password:
        if last_char is not None and int(x) < int(last_char):
            return False
        last_char = x
    return True


def test():
    assert match(112233)
    assert match(123444) is False
    assert match(111122)


test()

input_range = range(134792, 675810 + 1)
cnt = sum([match(x) for x in input_range])
print('Num matches:', cnt)
assert cnt == 1319
