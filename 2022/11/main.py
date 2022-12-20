import sys
sys.path.append('../..')
import util


class Monkey:
    def __init__(self, id, items, operation, test, test_true, test_false):
        self.id = id
        self.items = items
        self.operation = operation.split('= ')[1]
        self.test = test
        self.test_true = test_true
        self.test_false = test_false
        self.num_inspections = 0

    def __str__(self):
        return 'Monkey %0d: %s' % (self.id, self.items)

    def run_operation(self, old):
        return eval(self.operation)
    
    def run_test(self, item):
        if item % self.test:
            # print('  Current worry level is not divisible by', self.test)
            # print('  Item with worry level', item, 'is thrown to monkey', self.test_false)
            return self.test_false
        else:
            # print('  Current worry level is divisible by', self.test)
            # print('  Item with worry level', item, 'is thrown to monkey', self.test_true)
            return self.test_true
    
    def add_item(self, item):
        self.items.append(item)


def process(input, div, rounds):
    monkeys = parse_input(input)
    lcm = util.lcmm(*[m.test for m in monkeys])
    print('LCM =', lcm)
    for m in monkeys:
        m.lcm = lcm
    return run(monkeys, div, rounds)

def run(monkeys, div, rounds):
    for j in range(rounds):
        round = j + 1
        for m in monkeys:
            # print(self)
            for item in m.items:
                # print(' Monkey inspects an item with worry level of', item)
                new = m.run_operation(item)
                if div == 1:
                    new = new % m.lcm
                else:
                    new = new // div 
                target = m.run_test(new)
                monkeys[target].items.append(new)
                m.num_inspections += 1
            m.items = []

        if round in [1, 20] or round % 1000 == 0:
            print('Round', round)
            print_num_inspections(monkeys)
            print()
        elif round % 100 == 0:
            print('Round', round)

    temp = sorted(monkeys, key=lambda x: x.num_inspections, reverse=True)
    return temp[0].num_inspections * temp[1].num_inspections


def print_num_inspections(monkeys):
    for m in monkeys:
        print('Monkey %0d inspected %0d times' % (m.id, m.num_inspections))


def parse_input(input):
    blocks = input.strip().split('\n\n')
    monkeys = []
    for i, b in enumerate(blocks):
        lines = b.splitlines()
        items = util.ints(lines[1])
        operation = lines[2].split(': ')[1]
        test = util.ints(lines[3])[0]
        test_true = util.ints(lines[4])[0]
        test_false = util.ints(lines[5])[0]
        m = Monkey(i, items, operation, test, test_true, test_false)
        monkeys.append(m)
    return monkeys


def test():
    test_input = '''
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
    '''
    assert(process(test_input, 3, 20) == 10605)
    assert(process(test_input, 1, 10000) == 2713310158)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    val = process(input, 3, 20)
    print('Part 1:', val)
    assert(val == 54036)

    val = process(input, 1, 10000)
    print('Part 2:', val)
    assert(val == 13237873355)