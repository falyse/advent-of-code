houses = {}
goal = 3400000

def meets_goal(i):
    score = 0
    for e in range(1, i+1):
        if not i % e:
            score += e
            # print('i', i, ', e', e, ' -> ', score)
            if score >= goal:
                print('House', i, 'met goal with', score)
                exit(0)
                return True
    print(i, score)
    return False

def get_candidates():
    # primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    primes = [2, 3]
    size = range(3)
    size = range(10)
    # y = []
    # for p in primes:
    #     x = []
    #     for i in range(size):
    #         x.append(p**i)
    #     y.append(x)
    # print(y)
    nums = []
    for i2 in range(10):
        for i3 in range(10):
            for i5 in range(8):
                for i7 in range(6):
                    for i11 in range(5):
                        for i13 in range(4):
                            for i17 in range(3):
                                for i19 in range(3):
                                    for i23 in range(2):
                                        nums.append(2**i2 * 3**i3 * 5**i5 * 7**i7 * 11**i11 * 13*i13 * 17**i17 * 19**i19 * 23**i23)
    nums = sorted(set(nums))
    nums = [x for x in nums if x <= 840840]
    nums = [x for x in nums if x > 522000]
    print(nums)
    # exit(1)
    return nums

# i = 1 to 77000
# i = 500000 to 522000
i = 2**19 * 3 # 1572864 too high
i = 900900
i = 840840
print(i)
# i = 900000 to 900900
# too high: 1000080, 900900
# meets_goal(i)

for i in get_candidates():
    meets_goal(i)
print('No match')
