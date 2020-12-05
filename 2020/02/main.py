import sys
sys.path.append('../..')
import util
import re


def process_line(line):
    min, max, letter, letters = re.findall(r'(\d+)-(\d+) (\w): (\w+)', line)[0]
    min, max = int(min), int(max)
    letters = list(letters)
    return (min, max, letter, letters)


def is_valid1(line):
    min, max, letter, letters = process_line(line)
    cnt = letters.count(letter)
    return (min <= cnt <= max)

def is_valid2(line):
    min, max, letter, letters = process_line(line)
    return (letters[min-1] == letter) ^ (letters[max-1] == letter)


def test1():
    assert(is_valid1('1-3 a: abcde') is True)
    assert(is_valid1('1-3 b: cdefg') is False)
    assert(is_valid1('2-9 c: ccccccccc') is True)

def test2():
    assert(is_valid2('1-3 a: abcde') is True)
    assert(is_valid2('1-3 b: cdefg') is False)
    assert(is_valid2('2-9 c: ccccccccc') is False)

test1()
test2()


with open('input.txt', 'r') as f:
    input = f.read().strip().splitlines()
    cnt1 = 0
    cnt2 = 0
    for line in input:
        if is_valid1(line):
            cnt1 += 1
        if is_valid2(line):
            cnt2 += 1

    print('Part 1', cnt1)
    assert(cnt1 == 548)
    print('Part 2', cnt2)
    assert(cnt2 == 502)
