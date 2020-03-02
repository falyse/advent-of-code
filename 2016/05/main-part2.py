import sys
sys.path.append('..')
import util

def get_password(input):
    index = 0
    password = ['_' for _ in range(8)]
    while '_' in password:
        pos, digit, index = get_digit(input, index)
        print('pos', pos, 'digit', digit)
        if pos in [str(x) for x in range(8)]:
            pos = int(pos)
            if password[pos] == '_':
                password[pos] = digit
        print(password)
    print('password', password)
    return ''.join(password)

def get_digit(input, index):
    while True:
        text = input + str(index)
        d = util.md5_hash(text)
        if d[0:5] == '00000':
            print(index, ':', d)
            return d[5], d[6], index + 1
        index += 1


def test():
    assert get_password('abc') == '05ace8e3'

# test()


with open('input.txt', 'r') as f:
    input = f.read().strip()
    password = get_password(input)
    print('Part 2 password:', password)
