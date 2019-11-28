data = {}

def process_input(input):
    for line in input.splitlines():
        s = line.split(': ')
        name = s[0]
        stats = s[1].split(', ')
        data[name] = {}
        for x in stats:
            t = x.split()
            data[name][t[0]] = int(t[1])

def get_score():
    c = sum([data[x]['ratio'] * data[x]['capacity'] for x in data])
    d = sum([data[x]['ratio'] * data[x]['durability'] for x in data])
    f = sum([data[x]['ratio'] * data[x]['flavor'] for x in data])
    t = sum([data[x]['ratio'] * data[x]['texture'] for x in data])
    c = max(c, 0)
    d = max(d, 0)
    f = max(f, 0)
    t = max(t, 0)
    score = c * d * f *t
    # print(c, d, f, t, '=', score)
    return score

def get_calories():
    return sum([data[x]['ratio'] * data[x]['calories'] for x in data])

# with open('test.txt', 'r') as f:
with open('input.txt', 'r') as f:
    process_input(f.read())
    print(data)

    max_score = 0
    for i0 in range(1, 101):
        for i1 in range(1, 101):
            for i2 in range(1, 101):
                for i3 in range(1, 101):
                    if i0+i1+i2+i3 == 100:
                        data['Frosting']['ratio'] = i0
                        data['Candy']['ratio'] = i1
                        data['Butterscotch']['ratio'] = i2
                        data['Sugar']['ratio'] = i3
                        score = get_score()
                        print(i0, i1, i2, i3, score)
                        if score > max_score and get_calories() == 500:
                            max_score = score
    print('Max', max_score)
