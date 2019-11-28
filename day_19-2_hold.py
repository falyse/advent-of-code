import re

start = 'CRnSiRnCaPTiMgYCaPTiRnFArSiThFArCaSiThSiThPBCaCaSiRnSiRnTiTiMgArPBCaPMgYPTiRnFArFArCaSiRnBPMgArPRnCaPTiRnFArCaSiThCaCaFArPBCaCaPTiTiRnFArCaSiRnSiAlYSiThRnFArArCaSiRnBFArCaCaSiRnSiThCaCaCaFYCaPTiBCaSiThCaSiThPMgArSiRnCaPBFYCaCaFArCaCaCaCaSiThCaSiRnPRnFArPBSiThPRnFArSiRnMgArCaFYFArCaSiRnSiAlArTiTiTiTiTiTiTiRnPMgArPTiTiTiBSiRnSiAlArTiTiRnPMgArCaFYBPBPTiRnSiRnMgArSiThCaFArCaSiThFArPRnFArCaSiRnTiBSiThSiRnSiAlYCaFArPRnFArSiThCaFArCaCaSiThCaCaCaSiRnPRnCaFArFYPMgArCaPBCaPBSiRnFYPBCaFArCaSiAl'
start = 'HOH'
# start = 'HOHOHO'

maps = []
solution_steps = []

def run(word, steps=1):
    print('Running on', word, 'steps', steps)
    new_words = []
    for i in range(len(word)):
        for m in maps:
            entries = list(m.items())
            k = entries[0][0]
            v = entries[0][1]
            new_word, match = re.subn(k, v, word[i:], 1)
            if i > 0:
                new_word = word[:i] + new_word
            if match:
                new_words.append(new_word)
                print(k, 'map to', v, 'at i=%0d' % i, ': ', word, '->', new_word)
                if new_word == 'e':
                    print('Found solution in', steps, 'steps')
                    solution_steps.append(steps)
                else:
                    run(new_word, steps+1)
                continue
        i += 1
    new_words = set(new_words)
    print(new_words)

# with open('input_19.txt', 'r') as f:
with open('input_19-test.txt', 'r') as f:
    for line in f.readlines():
        k, v = line.strip().split(' => ')
        maps.append({v: k})
    print(maps)
    run(start)
    print()
    print('Min steps:', min(solution_steps))
