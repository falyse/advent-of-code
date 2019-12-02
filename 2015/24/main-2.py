from itertools import permutations
from itertools import combinations

valid_groups = []


def calc_qe(group):
    qe = 1
    for x in group:
        qe = qe * x
    return qe

def has_group_match(remaining, min_i, max_i, i1, level=0):
    for i2 in range(min_i, max_i-i1+1):
        combos2 = combinations(remaining, i2)
        print('    i2', i2)
        for g2 in combos2:
            if sum(g2) == group_weight:
                print('      ', g1, g2)
                valid_groups.append(g1)
                if level == 1:
                    return True
                else:
                    remaining = [x for x in remaining if x not in g2]
                    return has_group_match(remaining, min_i, max_i, i2, 1)
    return False


with open('input.txt', 'r') as f:
    # with open('test.txt', 'r') as f:
    input = [int(x.strip()) for x in f.readlines()]

    total_weight = sum([x for x in input])
    group_weight = int(total_weight/4)
    print('Total weight', total_weight, 'Group weight', group_weight)

    min_i = 5
    max_i = len(input) - min_i
    for i1 in range(min_i, min_i+1):
        combos1 = combinations(input, i1)
        print('i1', i1)
        for g1 in combos1:
            if sum(g1) != group_weight:
                continue
            print('  g1', g1)
            remaining = [x for x in input if x not in g1]
            if has_group_match(remaining, min_i, max_i, i1):
                continue

    print(valid_groups)
    min_len = min([len(x) for x in valid_groups])
    ideal_groups = [x for x in valid_groups if len(x) == min_len]
    print(ideal_groups)
    print('Min QE:', min([calc_qe(g) for g in ideal_groups]))
