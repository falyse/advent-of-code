def process_input(input):
    orbits = {}
    for x in input:
        x = x.strip()
        a, b = x.split(')')
        orbits[b] = a
    # print(orbits)
    return orbits


class Node:
    def __init__(self, name, depth):
        self.name = name
        self.parent = None
        self.depth = depth
        self.children = []

    def __str__(self):
        text = '%sNode %s\n' % (' '*self.depth, self.name)
        for child in self.children:
            text += str(child)
        return text

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def get_total_depth(self):
        return self.depth + sum([x.get_total_depth() for x in self.children])

    def get_node(self, name):
        if self.name == name:
            return self
        for child in self.children:
            node = child.get_node(name)
            if node:
                return node
        return None


def create_tree(orbits, start='COM', depth=0):
    node = Node(start, depth)
    for k,v in orbits.items():
        if v == start:
            child = create_tree(orbits, k, depth+1)
            node.add_child(child)
    return node


def get_ancestors(tree, node):
    ancestors = []
    while True:
        parent = node.parent
        if parent is None:
            break
        else:
            ancestors.append(parent)
            node = parent
    return ancestors


def find_common_ancestor(tree, node0, node1):
    ancestors0 = get_ancestors(tree, node0)
    ancestors1 = get_ancestors(tree, node1)
    path0 = list(reversed(ancestors0))
    path1 = list(reversed(ancestors1))
    common_node = None
    for i in range(len(path0)):
        if path0[i] == path1[i]:
            common_node = path0[i]
        else:
            break
    return common_node


with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
# with open('test1.txt', 'r') as f:
    orbits = process_input(f.readlines())
    tree = create_tree(orbits)
    # print(tree)
    num_orbits = tree.get_total_depth()
    print('Num orbits', num_orbits)

    you = tree.get_node('YOU')
    san = tree.get_node('SAN')
    ancestor = find_common_ancestor(tree, you, san)
    num_transfers = (you.depth - ancestor.depth - 1) + (san.depth - ancestor.depth - 1)
    print('Num transfers', num_transfers)

    # Answer assertions for refactoring
    assert num_orbits == 271151
    assert num_transfers == 388




