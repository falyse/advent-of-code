sues = {}
result = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}

def process_input(input):
    input = input.replace('Sue ', '')
    for line in input.splitlines():
        id, entries = line.split(': ', 1)
        id = int(id)
        # print(id, entries)
        sues[id] = {}
        for entry in entries.split(', '):
            k,v = entry.split(': ')
            sues[id][k] = int(v)
    # print(sues)

with open('input_16.txt', 'r') as f:
    process_input(f.read())
    for sue in sues.keys():
        match = True
        for k,v in sues[sue].items():
            if k in ['cats', 'trees']:
                if v <= result[k]:
                    match = False
            elif k in ['pomeranians', 'goldfish']:
                if v >= result[k]:
                    match = False
            elif result[k] != v:
                match = False
        if match:
            print(sue, sues[sue])


