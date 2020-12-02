import sys
sys.path.append('../..')
import util
import re


def process_line(line):
    m = re.match(r'(\d+)-(\d+) (\w): (\w+)', line)
    if m:
        min = int(m.group(1))
        max = int(m.group(2))
        letter = m.group(3)
        letters = list(m.group(4))
        return (min, max, letter, letters)


def is_valid1(line):
    min, max, letter, letters = process_line(line)
    cnt = letters.count(letter)
    return (int(min) <= cnt <= int(max))

def is_valid2(line):
    min, max, letter, letters = process_line(line)
    min -= 1
    max -= 1
    if letters[min] == letter and letters[max] == letter:
        return False
    if letters[min] == letter or letters[max] == letter:
        return True
    return False


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
    print('Part 2', cnt2)
