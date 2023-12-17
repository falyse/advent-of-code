import sys
sys.path.append('../..')
import util


def process(input):
    cards = {}
    lines = input.strip().splitlines()
    total = 0
    for j, line in enumerate(lines):
        id = j + 1
        add_card(cards, id)
        _, info = line.split(":")
        win, card = info.split('|')
        win = util.ints(win)
        card = util.ints(card)
        have = list(set(win) & set(card))
        if len(have):
            num = len(have)
            print(id, have, num)
            for i in range(num):
                add_card(cards, id+i+1, cards[id])
        print(cards)
    total = sum(cards.values())
    print(total)
    return total

def add_card(cards, id, num=1):
    if id not in cards:
        cards[id] = 0 
    cards[id] += num

def test():
    test_input = '''
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

    '''
    assert(process(test_input) == 30)

    test_input = '''
Card 1: 0 | 1
Card 2: 0 | 1
'''
    assert(process(test_input) == 2)

test()

with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
