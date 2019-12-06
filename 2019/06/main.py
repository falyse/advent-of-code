class Node:
    """Class to define a node in the orbit tree"""
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

    def find_node(self, name):
        """Find descendant node with matching name"""
        if self.name == name:
            return self
        for child in self.children:
            node = child.find_node(name)
            if node:
                return node
        return None


def process_input(input):
    """Parse each orbit definition and return data as a dict
       where key is the orbiter (ie. key orbits value)"""
    orbits = {}
    for line in input:
        a, b = line.strip().split(')')
        orbits[b] = a
    # print(orbits)
    return orbits


def create_tree(orbits, start='COM', depth=0):
    """Construct a tree based on the connections defined in the orbits hash"""
    node = Node(start, depth)
    for k,v in orbits.items():
        if v == start:
            child = create_tree(orbits, k, depth+1)
            node.add_child(child)
    return node


def get_ancestors(node):
    """Return a list of all parent ancestors from the specified node to the tree root"""
    ancestors = []
    while True:
        parent = node.parent
        if parent is None:
            break
        else:
            ancestors.append(parent)
            node = parent
    return ancestors


def find_common_ancestor(node0, node1):
    """Return the nearest common ancestor of two nodes"""
    ancestors0 = get_ancestors(node0)
    ancestors1 = get_ancestors(node1)
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
# with open('test-1.txt', 'r') as f:
# with open('test-2.txt', 'r') as f:
    orbits = process_input(f.readlines())
    tree = create_tree(orbits)
    # print(tree)

    # Part 1:
    #   The number of orbits for each node is the tree depth
    #   Sum all the depths to get the total number of orbits in the system
    num_orbits = tree.get_total_depth()
    print('Num orbits', num_orbits)

    # Part 2:
    #   The minimum number of transfers between YOU and SAN
    #   is the sum of the distances from each node to the nearest common ancestor
    you = tree.find_node('YOU')
    san = tree.find_node('SAN')
    ancestor = find_common_ancestor(you, san)
    num_transfers = (you.depth - ancestor.depth - 1) + (san.depth - ancestor.depth - 1)
    print('Num transfers', num_transfers)

    # Answer assertions for refactoring
    assert num_orbits == 271151
    assert num_transfers == 388




