import sys
sys.path.append('../..')
import util


def get_seat_id(code):
    row = code[0:7]
    col = code[7:10]

    row = row.replace('F', '0')
    row = row.replace('B', '1')
    row = int(row, base=2)

    col = col.replace('L', '0')
    col = col.replace('R', '1')
    col = int(col, base=2)

    seat_id = row*8 + col
    # print(code, ':', row, col, '=', seat_id)
    return seat_id


def test():
    assert(get_seat_id('BFFFBBFRRR') == 567)

test()


with open('input.txt', 'r') as f:
    input = f.read().strip().splitlines()
    max_id = 0
    ids = []
    for seat in input:
        seat_id = get_seat_id(seat)
        ids.append(seat_id)
        if seat_id > max_id:
            max_id = seat_id
    print('Part 1:', max_id)

    ids = sorted(ids)
    for i, seat_id in enumerate(ids):
        if i == 0 or i == len(ids)-1:
            continue
        if ids[i+1] != seat_id+1:
            print('Part 2:', seat_id+1)
            break

