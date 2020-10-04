import sys
sys.path.append('../..')
import util

def get_password(input):
    index = 0
    password = ''
    for i in range(8):
        digit, index = get_digit(input, index)
        password += digit
    print('password', password)
    return password

def get_digit(input, index):
    while True:
        text = input + str(index)
        d = util.md5_hash(text)
        if d[0:5] == '00000':
            print(index, ':', d)
            return str(d[5]), index + 1
        index += 1


def test():
    assert get_password('abc') == '18f47a30'

# test()


with open('input.txt', 'r') as f:
    input = f.read().strip()
    password = get_password(input)
    print('Part 1 password:', password)
