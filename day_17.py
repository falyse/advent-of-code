from itertools import combinations

with open('input_17.txt', 'r') as f:
    containers = [int(x) for x in f.readlines()]
    # containers = [20, 15, 10, 5, 5]
    # total = 25
    total = 150

    cnt = 0
    options = []
    min_containers = len(containers)
    for r in range(2,len(containers)+1):
        # print('Choose', r)
        combos = combinations(containers, r)
        for c in combos:
            if sum(list(c)) == total:
                print(c)
                cnt += 1
                options.append(list(c))
                num_containers = len(list(c))
                if num_containers < min_containers:
                    min_containers = num_containers
    print('Count', cnt)

    options = [x for x in options if len(x) == min_containers]
    print(options)
    print('Min', min_containers, 'Count', len(options))





