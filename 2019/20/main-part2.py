import sys
sys.path.append('..')
import collections
import operator
import util


def text_to_maze(text):
    loc = (0,0)
    maze = collections.defaultdict(str)
    for line in text.splitlines():
        for char in line.rstrip():
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
    util.pretty_print(portals)
    jumps = {}
    for pname, locs in portals.items():
        locs = list(locs)
        if len(locs) == 2:
            jumps[locs[0]] = {'dst': locs[1], 'name': pname, 'used': False}
            jumps[locs[1]] = {'dst': locs[0], 'name': pname, 'used': False}
    return portals, jumps

def get_portal_from_loc(portals, loc):
    for p,l in portals.items():
        if loc in l:
            return p


def walk_maze(maze, jumps, start_loc, end_loc):
    key = (start_loc, 0)
    bfs = collections.deque([key])
    distance = {key: 0}
    while bfs:
        h, level = bfs.popleft()
        lh = level
        # print('At level', lh, h)
        if level > 10:
            continue
        for dir in get_open_dirs(maze, h):
            level = lh
            if h == end_loc and level == 0:
                print('Done at loc', h, 'dist', distance[(h, level)])
                return distance[(h, level)]
            take_jump = False
            if h in jumps:
                if level == 0 and h not in [start_loc, end_loc] and is_outer(maze, h):
                    take_jump = False
                else:
                    take_jump = True
                    loc = jumps[h]['dst']
                    if is_outer(maze, h):
                        level -= 1
                    else:
                        level += 1
                    if level < 0:
                        take_jump = False
                    if jumps[h]['used']:
                        take_jump = False
                    if (loc, level) in distance:
                        take_jump = False
                    if take_jump:
                        # print(distance)
                        print('Portal', jumps[h]['name'], 'from level', lh, h, 'to level', level, loc, is_outer(maze, h))
                        # distance[(h,level)] = distance[(h,lh)]
                        jumps[h]['used'] = True
                    else:
                        level = lh
            if not take_jump:
                if maze[h].isupper():
                    continue
                loc = get_next_loc(h, dir)
            if (loc, level) in distance:
                continue
            # if level == 1:
            #     print('  dir', dir, 'loc', loc, 'lh', lh)
            # render(maze, loc)
            distance[(loc,level)] = distance[(h,lh)] + 1
            bfs.append((loc, level))
            # if level == 1:
            #     print('  ', bfs)
    print(distance)
    return distance[(loc, level)]


def is_outer(maze, h):
    x_max = max([loc[0] for loc in maze.keys()])
    y_max = max([loc[1] for loc in maze.keys()])
    r = list(range(4))
    rx = r + [x_max - i for i in range(4)]
    ry = r + [y_max - i for i in range(4)]
    return h[0] in rx or h[1] in ry


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
    """) == 26
    exit(0)

def test1():
    assert solve_maze(r"""
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                         
    """) == 396
    exit(0)

test1()


with open('input.txt', 'r') as f:
    input = f.read()
    dist = solve_maze(input)
    print('Final dist:', dist)
