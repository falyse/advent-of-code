import math
houses = {}
goal = 34000000/11

def meets_goal(i):
    score = 0
    for e in range(math.ceil(i/50), i+1):
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
    nums = []
    for i2 in range(10):
        for i3 in range(10):
            for i5 in range(10):
                for i7 in range(10):
                    for i11 in range(5):
                        for i13 in range(5):
                            for i17 in range(5):
                                for i19 in range(5):
                                    for i23 in range(5):
                                        for i29 in range(5):
                                            for i31 in range(5):
                                                for i37 in range(5):
                                                    for i41 in range(5):
                                                        for i43 in range(5):
                                                            for i47 in range(5):
                                                                nums.append(2**i2 * 3**i3 * 5**i5 * 7**i7 * 11**i11 * 13*i13 * 17**i17 * 19**i19 * 23**i23 * 29**i29 *
                                                                            31**i31 * 37**i37 * 41**i41 * 43**i43 * 47**i47)
    nums = sorted(set(nums))
    nums = [x for x in nums if x <= 873600]
    nums = [x for x in nums if x > 0]
    print(nums)
    # exit(1)
    return nums

# too high: 873600, 875160

# meets_goal(100)
# exit(1)

# for i in get_candidates():
#     meets_goal(i)


for i in range(686880, 873600, 60):
    meets_goal(i)

print('No match')
