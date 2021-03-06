import re
import typing
import functools
import operator
import pprint

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


# Dict
def sort_by_value(x):
    return sorted(x.items(), key=operator.itemgetter(1))


# Grid
def text_to_grid(text, map):
    grid = [[x for x in line.strip()] for line in text.split('\n')]
    if map.keys():
        grid = grid_map(grid, map)
    return grid

def grid_to_text(grid, map):
    if map.keys():
        grid = grid_map(grid, map)
    return '\n'.join([''.join([x for x in line]) for line in grid])

def grid_min_max(grid):
    return min(map(min, grid)), max(map(max, grid))

def grid_map(grid, map={}):
    return [[map[x] if x in map.keys() else x for x in y] for y in grid]

def make_grid(*dimensions: typing.List[int], fill=None):
    """Returns a grid such that 'dimensions' is just out of bounds"""
    if len(dimensions) == 1:
        return [fill for _ in range(dimensions[0])]
    next_down = make_grid(*dimensions[1:], fill=fill)
    return [list(next_down) for _ in range(dimensions[0])]

def flatten(grid):
    return [i for x in grid for i in x]


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


# Math
def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def lcmm(*args):
    """Return lcm of args."""
    return functools.reduce(lcm, args)


# Util
pp = pprint.PrettyPrinter(indent=4)
def pretty_print(x):
    pp.pprint(x)
