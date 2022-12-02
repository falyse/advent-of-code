import sys
sys.path.append('../..')
import util


scores = {
    'X': 0,
    'Y': 3,
    'Z': 6,
}

matchups = {
    ('A', 'X'): 3,
    ('A', 'Y'): 1,
    ('A', 'Z'): 2,
    ('B', 'X'): 1,
    ('B', 'Y'): 2,
    ('B', 'Z'): 3,
    ('C', 'X'): 2,
    ('C', 'Y'): 3,
    ('C', 'Z'): 1,
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
    assert(process(test_input) == 12)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input)
    print('Part 2:', val)
