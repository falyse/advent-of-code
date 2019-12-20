import sys
sys.path.append('..')
import collections
import operator
import util


def text_to_maze(text):
    loc = (0,0)
    maze = collections.defaultdict(str)
    for line in text.splitlines():
        for char in line:
            maze[loc] = char
            loc = (loc[0] + 1, loc[1])
        loc = (0, loc[1] + 1)
    return maze

def render(maze, loc=None):
    maze = maze.copy()
    if loc is not None:
        maze[loc] = '@'
    image = []
    x_vals, y_vals = zip(*maze.keys())
    for y in range(min(y_vals), max(y_vals)+1):
        row = []
        for x in range(min(x_vals), max(x_vals)+1):
            value = maze.get((x, y))
            if value is None:
                char = ' '
            else:
                char = value
            row.append(char)
        image.append(''.join(row))
    text = '\n'.join(image)
    print(text)

def solve_maze(input):
    maze = text_to_maze(input)
    render(maze)
    portals, jumps = find_portals(maze)
    dist = walk_maze(maze, jumps, list(portals['AA'])[0], list(portals['ZZ'])[0])
    print('Dist:', dist)
    return dist


def find_portals(maze):
    portals = {}
    for loc in maze:
        if maze[loc].isupper():
            for dir in get_open_dirs(maze, loc):
                next_loc = get_next_loc(loc, dir)
                if maze[next_loc].isupper():
                    letters = [maze[loc], maze[next_loc]]
                    pname = ''.join(sorted(letters))
                    test_loc = get_next_loc(next_loc, dir)
                    if maze.get(test_loc) == '.':
                        ploc = test_loc
                    else:
                        ploc = get_next_loc(loc, reverse_dir(dir))
                    # print('Found portal', pname, 'at loc', ploc)
                    if not pname in portals:
                        portals[pname] = set()
                    portals[pname].add(ploc)
    print(portals)
    jumps = {}
    for pname, locs in portals.items():
        locs = list(locs)
        if len(locs) == 2:
            jumps[locs[0]] = locs[1]
            jumps[locs[1]] = locs[0]
    return portals, jumps


def walk_maze(maze, jumps, start_loc, end_loc):
    bfs = collections.deque([start_loc])
    distance = {start_loc: 0}
    while bfs:
        h = bfs.popleft()
        for dir in get_open_dirs(maze, h):
            if h == end_loc:
                print('Done at loc', h, 'dist', distance[h])
                exit(0)
            if h in jumps and jumps[h] not in distance:
                loc = jumps[h]
                print('Portal from', h, 'to', loc)
            else:
                if maze[h].isupper():
                    continue
                loc = get_next_loc(h, dir)
            if loc in distance:
                continue
            # print('Visit loc', loc)
            render(maze, loc)
            distance[loc] = distance[h] + 1
            bfs.append(loc)
    print(distance)
    return distance[loc]


def get_next_loc(loc, dir):
    moves = {1: (0,1),
             2: (0,-1),
             3: (-1,0),
             4: (1,0)}
    deltas = moves[dir]
    next_loc = tuple(map(operator.add, loc, deltas))
    return next_loc

def reverse_dir(dir):
    if dir == 1:
        return 2
    if dir == 2:
        return 1
    if dir == 3:
        return 4
    if dir == 4:
        return 3

def get_open_dirs(maze, loc):
    opens = []
    for d in range(1, 5):
        val = maze.get(get_next_loc(loc, d))
        if val is not None and val != '#':
            opens.append(d)
    return opens


def test0():
    assert solve_maze(r"""
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z      
    """) == 23
    exit(0)

def test1():
    assert solve_maze(r"""
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P  
    """) == 58
    exit(0)

# test1()


with open('input.txt', 'r') as f:
    input = f.read()
    dist = solve_maze(input)
    print('Final dist:', dist)
    assert dist == 606
