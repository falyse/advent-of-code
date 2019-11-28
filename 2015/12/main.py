import re
import json

def get_sum(input):
    print('get_sum', type(input), input)
    if type(input) == int:
        return int(input)
    elif type(input) == list:
        return sum([get_sum(x) for x in input])
    elif type(input) == dict:
        if 'red' in input.values():
            return 0
        return sum([get_sum(k) + get_sum(v) for k,v in input.items()])
    else:
        return 0

with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    # input = f.read()
    # matches = re.findall(r'-?\d+', input)
    # print(matches)
    # matches = [int(x) for x in matches]
    # print('Sum:', sum(matches))

    input = json.load(f)
    print(input)
    sum = get_sum(input)
    print('Sum:', sum)
