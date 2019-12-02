def get_next_code(value):
    value *= 252533
    return value % 33554393


final_row = 2981
final_col = 3075

# final_row = 4
# final_col = 5

data = {}
code = 20151125
row = 1
while row < final_row + final_col:
    while row in data:
        row += 1
    data[row] = {}
    data[row][1] = code
    # print(data)
    code = get_next_code(code)
    for offset in range(1, row):
        # print('row', row, 'off', offset, '->', row-offset, row-offset)
        data[row-offset][offset+1] = code
        # print(data)
        code = get_next_code(code)
    print(len(data))

print('data[%0d][%0d] = %0d' % (final_row, final_col, data[final_row][final_col]))

