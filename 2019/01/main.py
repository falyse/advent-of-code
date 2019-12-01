def get_mass(value):
    if value < 0:
        return 0
    m = int(value / 3) - 2
    # f = get_mass(m)
    # print(m)
    if m < 0:
        return 0
    if m > 0:
        m += get_mass(m)
    return m

with open('input.txt', 'r') as f:
    input = f.readlines()
    # print(get_mass(14))
    # print(get_mass(1969))
    # print(get_mass(100756))
    s = sum([get_mass(int(x)) for x in input])
    print(s)
