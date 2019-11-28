from itertools import permutations

class Route():
    def __init__(self, start, end, distance):
        self.start = start
        self.end = end
        self.distance = distance

# with open('test.txt', 'r') as f:
with open('input.txt', 'r') as f:
    input = f.readlines()
    places = {}
    routes = {}
    for line in input:
        start, _to, end, _equals, distance = line.split()
        places[start] = None
        places[end] = None
        # routes.append(Route(start, end, distance))
        distance = int(distance)
        routes[start + end] = distance
        routes[end + start] = distance
    print(places.keys())

    perms = permutations(places)
    min_dist = 0
    max_dist = 0
    for p in list(perms):
        distance = 0
        for i in range(1,len(p)):
            distance += routes[p[i-1] + p[i]]
        print(p, distance)
        if min_dist == 0 or distance < min_dist:
            min_dist = distance
        if distance > max_dist:
            max_dist = distance
    print('Min distance:', min_dist)
    print('Max distance:', max_dist)

