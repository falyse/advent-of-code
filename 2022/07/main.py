import sys
sys.path.append('../..')
import util


class Node:
    def __init__(self, name, type, parent, size):
        self.name = name
        self.type = type
        self.parent = parent
        self.size = int(size)
        self.children = {}
    def __str__(self):
        parent = None
        if self.parent:
            parent = self.parent.name
        return '%s %s, Parent %s, Size %s' % (self.type, self.name, parent, self.size)


def build_tree(input):
    cmds = input.strip().splitlines()
    all_nodes = []
    head = Node('/', 'dir', None, 0)
    all_nodes.append(head)
    for cmd in cmds:
        if '$ cd /' in cmd:
            cur = head
        elif '$ cd ..' in cmd:
            # Update dir node size as we leave it
            cur.size = sum([int(n.size) for n in cur.children.values()])
            cur = cur.parent
        elif '$ cd' in cmd:
            dir = cmd.split()[-1]
            cur = cur.children[dir]
        elif '$ ls' in cmd:
            pass
        else:
            size, name = cmd.split()
            if size == 'dir':
                type = 'dir'
                size = 0
            else:
                type = 'file'
            n = Node(name, type, cur, size)
            all_nodes.append(n)
            cur.children[name] = n
            print(n)
    
    while True:
        if cur.type == 'dir' and cur.size == 0:
            cur.size = sum([int(n.size) for n in cur.children.values()])
        cur = cur.parent
        if cur is None:
            break

    return all_nodes


def process_part1(all_nodes):
    # print()
    total = 0
    for n in all_nodes:
        if n.type == 'dir' and n.size <= 100000:
            total += n.size
            # print(n, total)
    return total


def process_part2(all_nodes):
    print(all_nodes[0])
    unused = 70000000 - all_nodes[0].size
    target = 30000000 - unused
    print(target)
    min = 70000000
    for n in all_nodes:
        if n.type == 'dir' and n.size > target and n.size < min:
            min = n.size
    return min


def test():
    test_input = '''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
    '''
    nodes = build_tree(test_input)
    assert(process_part1(nodes) == 95437)
    assert(process_part2(nodes) == 24933642)

test()


with open('input.txt', 'r') as f:
    input = f.read()
    nodes = build_tree(input)
    val = process_part1(nodes)
    print('Part 1:', val)
    assert(val == 1428881)
    val = process_part2(nodes)
    print('Part 2:', val)
    assert(val == 10475598)
