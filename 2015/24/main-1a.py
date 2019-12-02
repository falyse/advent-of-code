from itertools import permutations

valid_groups = []

def divide_groups(input, ids):
    print('Checking', ids)
    group1 = []
    group2 = []
    group3 = []
    i = 0
    for id in ids:
        if id == 1:
            group1.append(input[i])
        if id == 2:
            group2.append(input[i])
        if id == 3:
            group3.append(input[i])
        i += 1
    if sum(group1) == sum(group2) == sum(group3):
        print('Match:', group1, group2, group3)
        valid_groups.append(group1)
        return True
    return False

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
        found_valid = False
        for i2 in range(min_i, max_i-i1+1):
            ids = []
            ids.extend(1 for x in range(i1))
            ids.extend(2 for x in range(i2))
            ids.extend(3 for x in range(max_i-i1-i2+1))
            print(ids)
            perms = permutations(ids)
            valid_perms = set(list(perms))
            for p in valid_perms:
                valid = divide_groups(input, p)
                if valid:
                    found_valid = True
        if found_valid:
            print(valid_groups)
            print('Min QE:', min([calc_qe(g) for g in valid_groups]))
            exit(0)
