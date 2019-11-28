start = 'CRnSiRnCaPTiMgYCaPTiRnFArSiThFArCaSiThSiThPBCaCaSiRnSiRnTiTiMgArPBCaPMgYPTiRnFArFArCaSiRnBPMgArPRnCaPTiRnFArCaSiThCaCaFArPBCaCaPTiTiRnFArCaSiRnSiAlYSiThRnFArArCaSiRnBFArCaCaSiRnSiThCaCaCaFYCaPTiBCaSiThCaSiThPMgArSiRnCaPBFYCaCaFArCaCaCaCaSiThCaSiRnPRnFArPBSiThPRnFArSiRnMgArCaFYFArCaSiRnSiAlArTiTiTiTiTiTiTiRnPMgArPTiTiTiBSiRnSiAlArTiTiRnPMgArCaFYBPBPTiRnSiRnMgArSiThCaFArCaSiThFArPRnFArCaSiRnTiBSiThSiRnSiAlYCaFArPRnFArSiThCaFArCaCaSiThCaCaCaSiRnPRnCaFArFYPMgArCaPBCaPBSiRnFYPBCaFArCaSiAl'
# start = 'HOH'
# start = 'HOHOHO'
# start = 'H2O'
# start = 'CaL'

# 193 too low

maps = []
with open('input_19.txt', 'r') as f:
# with open('input_19-test.txt', 'r') as f:
    for line in f.readlines():
        k, v = line.strip().split(' => ')
        maps.append({k: v})
    print(maps)

    words = []
    i = 0
    for char in start:
        for m in maps:
            entries = list(m.items())
            k = entries[0][0]
            v = entries[0][1]
            symbol = char
            next_i = i+1
            if i < len(start) - 1 and start[i+1].islower():
                symbol += start[i+1]
                next_i = i+2
            if symbol == k:
                print(symbol, 'map to', v)
                new_word = ''
                if i > 0:
                    new_word += start[:i]
                new_word += v
                if next_i < len(start):
                    new_word += start[next_i:]
                words.append(new_word)
                print(i, new_word)
                continue
        i += 1
    print(words)
    words = set(words)
    print(words)
    print(len(words))

