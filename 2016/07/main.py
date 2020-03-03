import sys
sys.path.append('..')
import util
import re

def split_sections(text):
    hypers = re.findall(r'\[.*?\]', text)
    supers = re.sub(r'\[.*?\]', ' ', text).split()
    return hypers, supers

def tls(text):
    hypers, supers = split_sections(text)
    if any([has_abba(x) for x in hypers]):
        return False
    if any([has_abba(x) for x in supers]):
        return True
    return False

def has_abba(text):
    for i in range(3, len(text)):
        if (text[i] == text[i - 3] and
                text[i - 1] == text[i - 2] and
                text[i] != text[i - 1]):
            return True
    return False


def ssl(text):
    hypers, supers = split_sections(text)
    for s in supers:
        abas = get_aba_list(s)
        for aba in abas:
            for h in hypers:
                if has_bab(h, aba):
                    return True
    return False

def get_aba_list(text):
    abas = []
    for i in range(2, len(text)):
        if (text[i] == text[i - 2] and
                text[i] != text[i - 1]):
            abas.append(text[i-2:i])
    return abas

def has_bab(text, aba):
    for i in range(2, len(text)):
        if (text[i] == text[i - 2] == aba[1] and
                text[i-1] == aba[0]):
            return True
    return False


def test():
    assert tls('abba[mnop]qrst') is True
    assert tls('abcd[bddb]xyyx') is False
    assert tls('aaaa[qwer]tyui') is False
    assert tls('ioxxoj[asdfgh]zxcvbn') is True
    assert tls('abba[mnop]qrst[abba]') is False

    assert ssl('aba[bab]xyz') is True
    assert ssl('xyx[xyx]xyx') is False
    assert ssl('aaa[kek]eke') is True
    assert ssl('zazbz[bzb]cdb') is True

test()


with open('input.txt', 'r') as f:
    input = f.read().strip().splitlines()
    cnt = sum([tls(x) for x in input])
    print('Part 1 count:', cnt)
    cnt = sum([ssl(x) for x in input])
    print('Part 2 count:', cnt)
