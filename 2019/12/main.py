import sys
sys.path.append('..')
import util
import operator


class Moon:
    def __init__(self, id, position, velocity):
        self.id = id
        self.orig_position = position
        self.orig_velocity = velocity
        self.reset()

    def reset(self):
        self.position = list(self.orig_position)
        self.velocity = list(self.orig_velocity)

    def __str__(self):
        return 'Moon %0d: pos=%s, vel=%s' % (self.id, self.position, self.velocity)

    def update_position(self):
        self.position = list(map(operator.add, self.position, self.velocity))

    def get_energy(self):
        pe = sum([abs(x) for x in self.position])
        ke = sum([abs(x) for x in self.velocity])
        print(self.id, pe, ke)
        return pe * ke

    def get_axis_state_text(self, axis):
        return '%0d, %0d, %0d' % (self.id, self.position[axis], self.velocity[axis])


def apply_gravity(m0, m1, axis=None):
    v0 = m0.velocity
    v1 = m1.velocity
    if axis is not None:
        axes = [axis]
    else:
        axes = [x for x in range(3)]
    for i in axes:
        if m0.position[i] < m1.position[i]:
            m0.velocity[i] = v0[i] + 1
            m1.velocity[i] = v1[i] - 1
        if m0.position[i] > m1.position[i]:
            m0.velocity[i] = v0[i] - 1
            m1.velocity[i] = v1[i] + 1


def sim_step(moons, axis):
    # Call apply_gravity for each pair of moons
    for j,m0 in enumerate(moons):
        for m1 in moons[j:]:
            if m0 != m1:
                apply_gravity(m0, m1, axis)
    # Update the position of each moon using the new velocity
    for m in moons:
        m.update_position()
        print(m)


def sim_moons_steps(moons, steps):
    for i in range(steps):
        print('step', i)
        sim_step(moons, None)
    print('Finished', steps, 'steps')
    return sum([m.get_energy() for m in moons])


def sim_moons_state(moons):
    # Each axis is independent, so can be simmed separately
    # First, find the number of steps for each axis to repeat its state
    #    This is the number of steps to reach the same initial state
    # Then, to find the first point where all axes repeat use LCM
    vals = []
    for axis in range(3):
        init_state = ''
        for m in moons:
            init_state += m.get_axis_state_text(axis)
        i=0
        done = False
        while not done:
            print('step', i)
            sim_step(moons, axis)
            state = ''
            for m in moons:
                state += m.get_axis_state_text(axis)
            done = state == init_state
            i += 1
        print('Found all zeros for axis', axis, 'at step', i)
        vals.append(i)
    print(vals)
    # Number of steps for all axes is the least common multiplier
    return util.lcmm(*vals)


def test():
    moons = []
    moons.append(Moon(0, [-1,0,2], [0,0,0]))
    moons.append(Moon(1, [2,-10,-7], [0,0,0]))
    moons.append(Moon(2, [4,-8,8], [0,0,0]))
    moons.append(Moon(3, [3,5,-1], [0,0,0]))
    for m in moons:
        print(m)

    # Part 1
    energy = sim_moons_steps(moons, 10)
    print('Energy:', energy)
    assert energy == 179

    for m in moons:
        m.reset()

    # Part 2
    num_steps = sim_moons_state(moons)
    print('Num steps to repeat:', num_steps)
    assert num_steps == 2772

    exit(0)
# test()


with open('input.txt', 'r') as f:
    input = [util.ints(x) for x in f.readlines()]
    temp = input.copy()
    moons = []
    for i, coords in enumerate(input):
        m = Moon(i, coords, [0,0,0])
        moons.append(m)
    print(*moons, sep='\n')

    # Part 1
    energy = sim_moons_steps(moons, 1000)
    print('Energy:', energy)
    assert energy == 7988

    for m in moons:
        m.reset()

    # Part 2
    num_steps = sim_moons_state(moons)
    print('Num steps to repeat:', num_steps)
    assert num_steps == 337721412394184
