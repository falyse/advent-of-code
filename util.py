import re
import typing
import functools
import operator
import hashlib
import pprint
import math

PIXEL_BLACK = '█'
PIXEL_LIGHT = '░'
PIXEL_WHITE = ' '


# Extract types
def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"-?\d+", s))

def positive_ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"\d+", s))

def floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))

def positive_floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))

def words(s: str) -> typing.List[str]:
    return re.findall(r"[a-zA-Z]+", s)


# List
def make_list(start, stop):
    return list(range(start, stop))

def print_list(values, sep='\n'):
    print(*values, sep=sep)

def min_max(values):
    return min(values), max(values)

def max_minus_min(values):
    return max(values) - min(values)

def list_element_delta(x):
    """Return the delta between each item in the list"""
    return [b-a for a, b in zip(x, x[1:])]

def lmap(func, *iterables):
    return list(map(func, *iterables))

def attribute_min_max(values, attribute):
    return min(values, key=operator.attrgetter(attribute)), max(values, key=operator.attrgetter(attribute))

def rotate_list(values, shift, dir='left'):
    if dir == 'right':
        values = values[-1*shift:] + values[:-1*shift]
    else:
        values = values[shift:] + values[:shift]
    return values


# Dict
def sort_by_value(d, reverse=False):
    return sorted(d.items(), key=operator.itemgetter(1), reverse=reverse)

def sort_by_value_then_key(d, reverse=False):
    return sorted(d.items(), key=lambda x: (x[1], x[0]), reverse=reverse)

def key_with_min_value(d):
    return min(d.items(), key=operator.itemgetter(1))[0]

def key_with_max_value(d):
    return max(d.items(), key=operator.itemgetter(1))[0]


# Grid
def make_grid(*dimensions: typing.List[int], fill=None):
    """Returns a grid such that 'dimensions' is just out of bounds"""
    if len(dimensions) == 1:
        return [fill for _ in range(dimensions[0])]
    next_down = make_grid(*dimensions[1:], fill=fill)
    return [list(next_down) for _ in range(dimensions[0])]

def text_to_grid(text, map={}):
    grid = [[x for x in line.strip()] for line in text.split('\n')]
    if map.keys():
        grid = grid_map(grid, map)
    return grid

def text_to_grid_dict(text, map={}):
    grid = {}
    for y, line in enumerate(text.split('\n')):
        for x, value in enumerate(line.strip()):
            if value in map.keys():
                value = map[value]
            grid[(x, y)] = value
    return grid

def grid_to_text(grid, map={}):
    if map.keys():
        grid = grid_map(grid, map)
    return '\n'.join([''.join([x for x in line]) for line in grid])

def grid_dict_to_text(grid, map={}):
    min = max = (None, None)
    for (x, y), value in grid.items():
        if min[0] is None:
            min = max = (x, y)
        if x < min[0]:
            min = (x, min[1])
        if x > max[0]:
            max = (x, max[1])
        if y < min[1]:
            min[1] = y
            min = (min[0], y)
        if y > max[1]:
            max = (max[0], y)
        if value in map.keys():
            value = map[value]
    return '\n'.join([''.join(grid[(x, y)] for x in range(min[0], max[0]+1)) for y in range(min[1], max[1]+1)])

def grid_min_max(grid):
    return min(map(min, grid)), max(map(max, grid))

def grid_map(grid, map={}):
    return [[map[x] if x in map.keys() else x for x in y] for y in grid]

def flatten_grid(grid):
    return [i for x in grid for i in x]

def grid_count(grid, value):
    flat = flatten_grid(grid)
    return flat.count(value)

def grid_count_adjacent(grid, loc, value, include_loc=False):
    x, y = loc
    cnt = 0
    for dy in range(-1,2):
        for dx in range(-1,2):
            y_test = y + dy
            x_test = x + dx
            if not include_loc and (x_test, y_test) == loc:
                continue
            if (y_test >= 0 and y_test < len(grid) and
                x_test >= 0 and x_test < len(grid[y])):
                if grid[y_test][x_test] == value:
                    cnt += 1
    return cnt

def grid_count_visible(grid, loc, value, blockers=[], valid_angles=None):
    '''Count the number of "value" items in the grid in direct line of sight from "loc"
       The "blockers" list can be used to add other items that block line of sight
       The "valid_angles" list can be used to only allow matches at certain angles'''
    search_list = [value] + blockers
    matches = []
    all_angles = set()
    # First, calculate the distance and angle to all other matching points in the grid
    for y_test, row in enumerate(grid):
        for x_test, val in enumerate(row):
            if (x_test, y_test) == loc:
                continue
            if val in search_list:
                dist, angle = get_path_between_points(loc, (x_test, y_test))
                if valid_angles is None or angle in valid_angles:
                    matches.append((dist, angle, val))
                    all_angles.add(angle)
    # Then, discard any match that is not visible due to a closer blocker at the same angle
    cnt = 0
    for angle in all_angles:
        matching_angle = sorted([x for x in matches if x[1] == angle])
        closest = matching_angle[0]
        if closest[2] == value:
            cnt += 1
    return cnt

def grid_locate_item(grid, search_value):
    for y, row in enumerate(grid):
        for x, item in enumerate(row):
            if item == search_value:
                return (x, y)
    return None

def grid_dict_locate_item(grid, search_value):
    return [loc for loc, value in grid.items() if value == search_value][0]


def get_path_between_points(coord0, coord1):
    dx = coord1[0] - coord0[0]
    dy = coord1[1] - coord0[1]
    dist = dx**2 + dy**2
    angle = math.atan2(-1*dy, dx) * 180/math.pi
    angle = (90 - angle) % 360  # Convert to clockwise angle
    return dist, angle


# Algorithms
def bisect(f, lo=0, hi=None, eps=1e-9):
    """
    Returns a value x such that f(x) is true.
    Based on the values of f at lo and hi.
    Assert that f(lo) != f(hi).
    """
    lo_bool = f(lo)
    if hi is None:
        offset = 1
        while f(lo+offset) == lo_bool:
            offset *= 2
        hi = lo + offset
    else:
        assert f(hi) != lo_bool
    while hi - lo > eps:
        mid = (hi + lo) / 2
        if f(mid) == lo_bool:
            lo = mid
        else:
            hi = mid
    if lo_bool:
        return lo
    else:
        return hi

def binary_search(f, lo=0, hi=None):
    """
    Returns a value x such that f(x) is true.
    Based on the values of f at lo and hi.
    Assert that f(lo) != f(hi).
    """
    lo_bool = f(lo)
    if hi is None:
        offset = 1
        while f(lo+offset) == lo_bool:
            offset *= 2
        hi = lo + offset
    else:
        assert f(hi) != lo_bool
    best_so_far = lo if lo_bool else hi
    while lo <= hi:
        mid = (hi + lo) // 2
        result = f(mid)
        if result:
            best_so_far = mid
        if result == lo_bool:
            lo = mid + 1
        else:
            hi = mid - 1
    return best_so_far

def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next in graph[start] - visited:
        dfs(graph, next, visited)
    return visited

def dfs_paths(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next in graph[start] - set(path):
        yield from dfs_paths(graph, next, goal, path + [next])

def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None

# Encryption
def md5_hash(input):
    m = hashlib.md5()
    m.update(input.encode('utf-8'))
    return m.hexdigest()

# Math
def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)
    
    while r != 0:
        quotient = old_r / r
        (old_r, r) = (r, old_r - quotient * r)
        (old_s, s) = (s, old_s - quotient * s)
        (old_t, t) = (t, old_t - quotient * t)
    
    print("Bezout coefficients:", (old_s, old_t))
    print("greatest common divisor:", old_r)
    print("quotients by the gcd:", (t, s))

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def lcmm(*args):
    """Return lcm of args."""
    return functools.reduce(lcm, args)


# Coordinate system movement
def coord_move(loc, dir, num_steps=1):
    dir_deltas = {'N': (0, num_steps),
                  'S': (0, -1*num_steps),
                  'E': (num_steps, 0),
                  'W': (-1*num_steps, 0)}
    delta = dir_deltas[dir]
    next_loc = tuple_add(loc, delta)
    return next_loc

def tuple_add(tuple0, tuple1):
    return tuple(map(operator.add, tuple0, tuple1))

def tuple_sub(tuple0, tuple1):
    return tuple(map(operator.sub, tuple0, tuple1))

def coord_turn(current_dir, turn_dir):
    if turn_dir in ['L', 'l', 'left']:
        turn = {'N': 'W',
                'S': 'E',
                'E': 'N',
                'W': 'S'}
    if turn_dir in ['R', 'r', 'right']:
        turn = {'W': 'N',
                'E': 'S',
                'N': 'E',
                'S': 'W'}
    if turn_dir in ['reverse']:
        turn = {'N': 'S',
                'S': 'N',
                'E': 'W',
                'W': 'E'}
    return turn[current_dir]

def taxi_distance(loc, origin=(0, 0)):
    diff = tuple(map(operator.sub, loc, origin))
    return abs(diff[0]) + abs(diff[1])


# Util
pp = pprint.PrettyPrinter(indent=4)
def pretty_print(x):
    pp.pprint(x)
