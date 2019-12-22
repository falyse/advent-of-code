import sys
sys.path.append('..')
import util


def deal_new(deck):
    return list(reversed(deck))

def cut(deck, n):
    cut = deck[:n]
    deck = deck[n:]
    return deck + cut

def deal_inc(deck, n):
    new = list(deck)
    for i in range(len(deck)):
        index = (n * i) % len(deck)
        new[index] = deck[i]
    return new


def shuffle(input, deck):
    for line in input.strip().splitlines():
        if 'new' in line:
            deck = deal_new(deck)
        if 'increment' in line:
            n = util.ints(line)[0]
            deck = deal_inc(deck, n)
        if 'cut' in line:
            n = util.ints(line)[0]
            deck = cut(deck, n)
        print(line)
        print('  ', deck)
    return deck


def test():
    deck = [x for x in range(10)]
    assert deck[7] == 7

    assert deal_new(deck) == util.ints('9 8 7 6 5 4 3 2 1 0')
    assert cut(deck, 3) == util.ints('3 4 5 6 7 8 9 0 1 2')
    assert cut(deck, -4) == util.ints('6 7 8 9 0 1 2 3 4 5')
    assert deal_inc(deck, 3) == util.ints('0 7 4 1 8 5 2 9 6 3')

    assert shuffle(r"""
deal with increment 7
deal into new stack
deal into new stack
    """, deck) == util.ints('0 3 6 9 2 5 8 1 4 7')

    assert shuffle(r"""
cut 6
deal with increment 7
deal into new stack    
    """, deck) == util.ints('3 0 7 4 1 8 5 2 9 6')

    assert shuffle(r"""
deal with increment 7
deal with increment 9
cut -2    
    """, deck) == util.ints('6 3 0 7 4 1 8 5 2 9')

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
    """, deck) == util.ints('9 2 5 8 1 4 7 0 3 6')

test()


with open('input.txt', 'r') as f:
    input = f.read()
    deck = [x for x in range(10007)]
    deck = shuffle(input, deck)
    card_index = 2018
    print('Card at index', card_index, 'is', deck[card_index])
    # 3201 too low
    # 7058 too high

