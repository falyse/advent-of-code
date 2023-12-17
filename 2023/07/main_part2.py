import sys
sys.path.append('../..')
import util


hex_map = {
    'T': 'a',
    'J': '0',
    'Q': 'c',
    'K': 'd',
    'A': 'e',
}

class Hand:
    def __init__(self, line):
        self.cards, self.bid = line.split()
        self.bid = int(self.bid)
        self.type = get_type(self.cards)
        self.hex = self.get_hex()
    
    def get_hex(self):
        h = self.cards
        for k,v in hex_map.items():
            h = h.replace(k, v)
        return int(h, 16)
    
    def __str__(self):
        return self.cards + ' : type ' + str(self.type) + ' : 0x%0x' % self.hex
    
    def __lt__(self, other):
        if self.type != other.type:
            return self.type > other.type
        else:
            return self.hex < other.hex


def process(input):
    lines = input.strip().splitlines()
    hands = []
    for line in lines:
        hands.append(Hand(line))
    hands = sorted(hands)
    [print(x) for x in hands]

    total = 0
    for i, hand in enumerate(hands):
        val = (i+1) * hand.bid
        total += val
    print('Total:', total)
    return total


def get_type(cards):
    d = {}
    j = 0
    for card in [*cards]:
        if card == 'J':
            j += 1
        else:
            if card not in d:
                d[card] = 0
            d[card] += 1
    vals = sorted(d.values(), reverse=True)
    if j == 5:
        return 1
    vals[0] += j
    if 5 in vals:
        return 1
    if 4 in vals:
        return 2
    if vals == [3, 2]:
        return 3
    if vals == [3, 1, 1]:
        return 4
    if vals == [2, 2, 1]:
        return 5
    if vals == [2, 1, 1, 1]:
        return 6
    return 7


def sort_hands(hand):
    return '%0d%s' % (hand.type, hand.cards)


def test():
    assert(get_type('AAAAA') == 1)
    assert(get_type('AAAA1') == 2)
    assert(get_type('32T3K') == 6)
    assert(get_type('AAAAJ') == 1)
    assert(get_type('QJJQ2') == 2)
    assert(get_type('AAJ22') == 3)
    assert(get_type('A3J22') == 4)
    assert(get_type('A3J12') == 6)
    assert(get_type('JJJJJ') == 1)
    assert(get_type('JJJJA') == 1)

    h = Hand('6J66J 1')
    assert(h.get_hex() == 0x60660)

    test_input = '''
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    '''
    assert(process(test_input) == 5905)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 2:', val)
    # 247968093 too low
