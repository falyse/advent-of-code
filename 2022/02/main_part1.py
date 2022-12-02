import sys
sys.path.append('../..')
import util


scores = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

matchups = {
    ('A', 'X'): 3,
    ('A', 'Y'): 6,
    ('A', 'Z'): 0,
    ('B', 'X'): 0,
    ('B', 'Y'): 3,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,
    ('C', 'Y'): 0,
    ('C', 'Z'): 3,
}

def process(input):
    rounds = input.strip().splitlines()
    total_score = 0
    for round in rounds:
        opp, you = round.split()
        # print(opp, you)
        score = scores[you] + matchups[(opp, you)]
        # print(score)
        total_score += score
    return total_score


def test():
    test_input = '''
A Y
B X
C Z
    '''
    assert(process(test_input) == 15)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 1:', val)
