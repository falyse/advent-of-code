houses = {}
goal = 3400000

# for i in range(1, max_houses):
# i = 1 to 77000
# i = 500000 to 522000
i = 2**19 * 3 # 1572864 too high
i = 2**3 * 3**2 * 5**2 * 7**2
print(i)
# i = 900000 to 900900
# too high: 1000080, 900900
x = True
while x:
    if i not in houses:
        houses[i] = 0
    for e in range(1, i+1):
        if not i % e:
            houses[i] += e
            # if not i % 1000:
            print('i', i, ', e', e, ' -> ', houses[i])
            if houses[i] >= goal:
                print('House', i, 'met goal with', houses[i])
                exit(0)
    i += 1
    x = False

print(houses)
print('Max:', max([x for x in houses.values()]))
