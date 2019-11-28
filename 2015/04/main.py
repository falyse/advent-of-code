import hashlib

input = 'The quick brown fox jumps over the lazy dog'
input = 'abcdef609043'

input = input.encode('utf-8')
m = hashlib.md5()
m.update(input)
hash = m.hexdigest()
print(input, hash)

input = 'abcdef'
input = 'pqrstuv'
input = 'ckczppom'
i = 0
hash = ''
# while hash[0:5] != '00000':
while hash[0:6] != '000000':
    i += 1
    m = hashlib.md5()
    str = '%s%0d' % (input, i)
    str = str.encode('utf-8')
    m.update(str)
    hash = m.hexdigest()
    print(i, str, hash)
print(i)

