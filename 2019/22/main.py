import sys
sys.path.append('..')
import util


def deal_new(size, index):
    return abs(size - index) - 1

def cut(size, index, n):
    return (index + n + size) % size

def deal_inc(size, index, n):
    t = index
    # print('inc', n, size, t, ':', index)
    while t % n:
        t += size
    index = t // n
    # print('inc', n, size, t, ':', index)
    return index


def shuffle(input, size, index):
    for line in reversed(input.strip().splitlines()):
        if 'new' in line:
            index = deal_new(size, index)
        if 'increment' in line:
            n = util.ints(line)[0]
            index = deal_inc(size, index, n)
        if 'cut' in line:
            n = util.ints(line)[0]
            index = cut(size, index, n)
        # print(line)
        # print('  ', index)
    return index


def test():
    size = 10
    index = 2

    assert deal_new(size, index) == 7
    assert cut(size, index, 3) == 5
    assert cut(size, index, -4) == 8
    assert deal_inc(size, index, 3) == 4

    assert deal_inc(100, 28, 32) == 4

    assert shuffle(r"""
deal with increment 7
deal into new stack
deal into new stack
    """, size, index) == 6

    assert shuffle(r"""
cut 6
deal with increment 7
deal into new stack    
    """, size, index) == 7

    assert shuffle(r"""
deal with increment 7
deal with increment 9
cut -2    
    """, size, index) == 0

    assert shuffle(r"""
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1    
    """, size, index) == 5

    assert shuffle(r"""
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1    
    """, size, 8) == 3
    exit(0)

# test()


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


with open('input.txt', 'r') as f:
    input = f.read()
    # part 1
    card = shuffle(input, 10007, 6129)
    print('Card at index 6129 is', card)
    assert card == 2019

    # Part 2
    # index = 2020
    # for i in range(101741582076661):
    #     if not i % 1000000:
    #         print('Iteration', i)
    #     index = shuffle(input, 119315717514047, index)
    # print('Card at index 2020 is', index)

    D = 119315717514047
    X = 2020
    Y = f(X)
    Z = f(Y)
    A = (Y-Z) * modinv(X-Y+D, D) % D
    B = (Y-A*X) % D
    print(A, B)
    
    n = 101741582076661
    print((pow(A, n, D)*X + (pow(A, n, D)-1) * modinv(A-1, D) * B) % D)