def calc_fuel(mass, recurse):
    m = int(mass / 3) - 2
    if m <= 0:
        return 0
    if recurse:
        m += calc_fuel(m, recurse)
    return m


def get_total_fuel(masses, recurse):
    total = sum([calc_fuel(m, recurse) for m in masses])
    print('Total fuel', total)
    return total


def test():
    # No recursion
    assert calc_fuel(12, False) == 2
    assert calc_fuel(14, False) == 2
    assert calc_fuel(1969, False) == 654
    assert calc_fuel(100756, False) == 33583
    # With recursion
    assert calc_fuel(14, True) == 2
    assert calc_fuel(1969, True) == 966
    assert calc_fuel(100756, True) == 50346


test()

with open('input.txt', 'r') as f:
    masses = [int(x) for x in f.readlines()]

    # Part 1: No recursion
    total = get_total_fuel(masses, False)
    assert total == 3455717

    # Part 2: With recursion
    total = get_total_fuel(masses, True)
    assert total == 5180690
