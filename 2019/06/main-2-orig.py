from collections import OrderedDict

orbits = OrderedDict()
num = {}

# cnt = 0
def get_num(k):
    num = 0
    if orbits[k] == 'COM':
        num += 1
    else:
        num += get_num(orbits[k])
    return num

steps = {'COM': 0}
depth = 0
def get_orbits(src, cnt=0):
    global depth
    print('asdf', src, cnt, depth)
    depth += 1
    for k,v in orbits.items():
        temp = cnt
        if v == src:
            temp += 1
            print(k, v, temp)
            steps[k] = temp
            get_orbits(k, temp)
            depth -= 1

def trace(node):
    n = node
    t = []
    while n != 'COM':
        t.append(orbits[n])
        n = orbits[n]
    print(t)
    return t


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
# with open('test1.txt', 'r') as f:
    input = f.readlines()
    for x in input:
        x = x.strip()
        a, b = x.split(')')
        orbits[b] = a
    print(orbits)

    get_orbits('COM')
    # print(cnt)
    print(steps)
    print('sum', sum(v for k,v in steps.items()))
    print('YOU', steps['YOU'])
    print('SAN', steps['SAN'])

    y = trace('YOU')
    s = trace('SAN')

    y = list(reversed(y))
    s = list(reversed(s))
    c = 0
    for i in range(len(y)):
        if not y[i] == s[i]:
            break
        c += 1
    print(c)
    print('dist', steps['YOU']-c + steps['SAN']-c)



