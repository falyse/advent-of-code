import re

def num_code_chars(str):
    num = len([x for x in str])
    print('%50s %0d' % (str, num))
    return num

def num_mem_chars(str):
    str = str.replace(r'\\', '.')
    str = str.replace('\\\"', '.')
    str = re.sub(r'\\x[a-fA-F0-9]{2}', '.', str)
    str = str.replace('"', '')
    return num_code_chars(str)

def num_encoded_chars(str):
    str = str.replace(r'\\', r'....')
    str = re.sub(r'\\x[a-fA-F0-9]{2}', r'..x..', str)
    str = str.replace(r'\"', r'....')
    str = str.replace('"', r'.""')
    str = str.replace('\\', '..')
    return num_code_chars(str)

# with open('test.txt', 'r') as f:
with open('input.txt', 'r') as f:
    input = f.readlines()
    input = [x.strip() for x in input]

    num_code = 0
    num_mem = 0
    num_enc = 0
    for x in input:
        num_code += num_code_chars(x)
        # num_mem += num_mem_chars(x)
        num_enc += num_encoded_chars(x)

    # print(num_code - num_mem)
    print(num_enc - num_code)
