import pprint

pp = pprint .PrettyPrinter()

sigs = {}
gates = []

class Gate():
    def __init__(self, op, dst, src0, src1):
        self.op = op
        self.dst = dst
        self.src0 = src0
        self.src1 = src1
        self.resolved = False

    def resolve(self):
        if self.resolved:
            return True
        dst = self.dst
        src0 = self.resolve_src(self.src0)
        src1 = self.resolve_src(self.src1)
        if src0 != '' and src1 != '':
            if self.op == 'ASSIGN':
                sigs[dst] = src0
            elif self.op == 'NOT':
                sigs[dst] = ~src0
            elif self.op == 'AND':
                sigs[dst] = src0 & src1
            elif self.op == 'OR':
                sigs[dst] = src0 | src1
            elif self.op == 'LSHIFT':
                sigs[dst] = src0 << src1
            elif self.op == 'RSHIFT':
                sigs[dst] = src0 >> src1
            else:
                print('Unrecognized op:', self.op)
            self.resolved = True

    def resolve_src(self, src):
        if src is None:
            return None
        if is_int(src):
            return int(src)
        if src in sigs:
            return sigs[src]
        return ''

def is_int(value):
    try:
        int(value)
    except ValueError:
        return False
    return True

def process_line(line):
    logic, dst = line.split(' -> ')
    dst = dst.strip()
    src0 = None
    src1 = None
    logic_parts = logic.split()
    if len(logic_parts) == 1:
        op = 'ASSIGN'
        src0 = logic_parts[0]
    elif len(logic_parts) == 2:
        op = logic_parts[0]
        src0 = logic_parts[1]
    elif len(logic_parts) == 3:
        op = logic_parts[1]
        src0 = logic_parts[0]
        src1 = logic_parts[2]
    else:
        print('Parse error:', line)
    gates.append(Gate(op, dst, src0, src1))


# with open('input_07-test.txt', 'r') as f:
with open('input_07-2.txt', 'r') as f:
    input = f.readlines()

    for x in input:
        process_line(x)

    while False in [x.resolved for x in gates]:
        for g in gates:
            g.resolve()

    # Convert to unsigned 16-bit ints
    for x in sigs:
        sigs[x] = sigs[x] & 0xffff
    pp.pprint(sigs)
