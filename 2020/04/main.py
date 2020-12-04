import sys
sys.path.append('../..')
import util
import re


def process(input, validate=False):
    passports = input.split('\n\n')
    cnt = [is_valid(x, validate) for x in passports].count(True)
    return cnt


def is_valid(passport, validate):
    fields = {}
    for x in passport.split():
        k,v = x.split(':')
        fields[k] = v
    # print(fields)

    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    valid = all(x in fields for x in required_fields)

    if not validate or not valid:
        return valid

    if (valid_year(fields['byr'], 1920, 2002) and
        valid_year(fields['iyr'], 2010, 2020) and
        valid_year(fields['eyr'], 2020, 2030) and
        valid_hgt(fields['hgt']) and
        valid_hcl(fields['hcl']) and
        valid_ecl(fields['ecl']) and
        valid_pid(fields['pid'])):
        return True
    return False


def valid_year(field, min, max):
    if not re.match(r'\d\d\d\d', field):
        return False
    y = int(field)
    return (min <= y <= max)

def valid_hgt(field):
    m = re.match(r'(\d+)(cm|in)', field)
    if m:
        num = int(m.group(1))
        unit = m.group(2)
        if unit == 'cm':
            return (150 <= num <= 193)
        if unit == 'in':
            return (59 <= num <= 76)
    return False

def valid_hcl(field):
    m = re.match(r'#[a-f0-9]{6}', field)
    return bool(m)

def valid_ecl(field):
    return field in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def valid_pid(field):
    m = re.match(r'^\d{9}$', field)
    return bool(m)


def test():
    assert(process('''
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
''') == 2)

def test2():
    assert(valid_year('2002', 1920, 2002) is True)
    assert(valid_year('2003', 1920, 2002) is False)
    assert(valid_hgt('60in') is True)
    assert(valid_hgt('190cm') is True)
    assert(valid_hgt('190in') is False)
    assert(valid_hgt('190') is False)
    assert(valid_hcl('#123abc') is True)
    assert(valid_hcl('#123abz') is False)
    assert(valid_hcl('123abc') is False)
    assert(valid_ecl('brn') is True)
    assert(valid_ecl('wat') is False)
    assert(valid_pid('000000001') is True)
    assert(valid_pid('0123456789') is False)

    assert(process('''
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
''', True) == 4)


# test()
test2()


with open('input.txt', 'r') as f:
    input = f.read().strip()
    num = process(input)
    print('Part 1', num)
    num = process(input, validate=True)
    print('Part 2', num)
