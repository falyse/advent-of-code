from itertools import permutations
from itertools import combinations

valid_groups = []


def calc_qe(group):
    qe = 1
    for x in group:
        qe = qe * x
    return qe


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    input = [int(x.strip()) for x in f.readlines()]

    min_i = 5
    max_i = len(input) - 1
    for i1 in range(min_i, max_i):
        combos1 = combinations(input, i1)
        print('i1', i1)
        for g1 in combos1:
            print('  g1', g1)
            remaining = [x for x in input if x not in g1]
            for i2 in range(min_i, max_i-i1-min_i+1):
                combos2 = combinations(remaining, i2)
                print('    i2', i2)
                for g2 in combos2:
                    if sum(g1) != sum(g2):
                        continue
                    g3 = [x for x in remaining if x not in g2]
                    if sum(g1) != sum(g3):
                        continue
                    print(g1, g2, g3)
                    valid_groups.append(g1)

    print(valid_groups)
    min_len = min([len(x) for x in valid_groups])
    ideal_groups = [x for x in valid_groups if len(x) == min_len]
    print(ideal_groups)
    print('Min QE:', min([calc_qe(g) for g in ideal_groups]))
