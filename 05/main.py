from unittest import TestCase

def is_nice(str):
    nice = num_vowels(str) >= 3 and has_double_letter(str) and not has_bad_string(str)
    return nice

def is_nice_part2(str):
    nice = has_repeated_pair(str) and has_interrupted_repeat(str)
    return nice

def num_vowels(str):
    num = 0
    for x in str:
        if x in 'aeiou':
            num += 1
    # print(str, num)
    return num

def has_double_letter(str):
    last_letter = ''
    for letter in str:
        if letter == last_letter:
            return True
        last_letter = letter
    return False

def has_bad_string(str):
    bad_strings = ['ab', 'cd', 'pq', 'xy']
    for s in bad_strings:
        if s in str:
            return True
    return False

def has_repeated_pair(str):
    i = 0
    for x in str:
        if i > 0:
            pair = str[i-1:i+1]
            # print('pair', pair, str[i+1:])
            if pair in str[i+1:]:
                return True
        i += 1
    return False

def has_interrupted_repeat(str):
    i = 0
    for x in str:
        if i >= 2 and x == str[i-2]:
            return True
        i += 1
    return False

with open('input_05.txt', 'r') as f:
    input = f.readlines()
    # input = ['ugknbfddgicrmopn', 'aaa', 'jchzalrnumimnmhp', 'haegwjzuvuyypxyu', 'dvszwmarrgswjxmb']
    # input = ['qjhvhtzxzqqjkmpb', 'xxyxx', 'uurcxstgmygtbstg', 'ieodomkazucvgmuy']
    nice = [is_nice_part2(x) for x in input]
    print(nice)
    num_nice = sum(nice)
    print('Num nice', num_nice)
