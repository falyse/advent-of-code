import sys
sys.path.append('../..')
import util

def check_room(input):
    name, rest = input.rsplit('-', 1)
    sector, checksum = rest.split('[')
    sector = int(sector)
    checksum = checksum.replace(']', '')
    # print(name, sector, checksum)
    if checksum == calc_checksum(name):
        dname = decrypt(name, sector)
        if 'north' in dname:
            print(dname, sector)
        return sector
    else:
        return 0

def calc_checksum(name):
    name = name.replace('-', '')
    cnts = {}
    for x in name:
        if x in cnts:
            cnts[x] += 1
        else:
            cnts[x] = 1
    sort = sorted(cnts.items(), key=lambda x: (-1*x[1],x[0]), reverse=False)
    checksum = ''.join([x[0] for x in sort[:5]])
    # print('  checksum:', checksum)
    return checksum

def decrypt(name, sector):
    dname = ''
    for x in name:
        if x == '-':
            dname += ' '
        else:
            pos = ord(x) + (sector % 26)
            if pos > ord('z'):
                pos -= 26
            dname += chr(pos)
    return dname


def test():
    assert check_room('aaaaa-bbb-z-y-x-123[abxyz]') == 123
    assert check_room('a-b-c-d-e-f-g-h-987[abcde]') == 987
    assert check_room('not-a-real-room-404[oarel]') == 404
    assert check_room('totally-real-room-200[decoy]') == 0
    assert decrypt('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'

test()


with open('input.txt', 'r') as f:
    input = f.read().strip().splitlines()
    total = sum([check_room(x) for x in input])
    print('Part 1 total:', total)
