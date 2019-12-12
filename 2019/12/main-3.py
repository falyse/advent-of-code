import sys
sys.path.append('../intcode')
sys.path.append('..')
from intcode import IntcodeComputer
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
        # print('  asdf0', self.position)
        self.position = list(map(operator.add, self.position, self.velocity))
        # print('  asdf1', self.position)

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
    if axis:
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
        # m0.velocity[i] = v0 + 1 if m0.position[i] > m1.position[i] else v0 - 1 if m0.position[i] < m1.position[i] else v0
        # m1.velocity[i] = v1 + 1 if m1.position[i] > m0.position[i] else v1 - 1 if m1.position[i] < m0.position[i] else v1
    # print('old v0', v0, 'new', m0.velocity)
    # print('apply moons %0d and %0d' % (m0.id, m1.id))

def print_moons(moons):
    for m in moons:
        print(m)


def sim_moons(moons, steps):
    vals = []
    for axis in range(3):
    # for axis in range(2,3):
        for m in moons:
            m.reset()
        init_state = ''
        for m in moons:
            init_state += m.get_axis_state_text(axis)
        print(init_state)
        i=1
        done = False
        while not done:
            # print('step', i)
            for j,m0 in enumerate(moons):
                for m1 in moons[j:]:
                    if m0 != m1:
                        apply_gravity(m0, m1, axis)
            text = ''
            all_zeros = True
            state = ''
            for m in moons:
                m.update_position()
                state += m.get_axis_state_text(axis)
                # print(m)
                # if m.velocity[axis] != 0:
                #     all_zeros = False
            done = state == init_state
            i += 1
        print('Found all zeros for axis', axis, 'at step', i)
        print(state)
        print_moons(moons)
        print()
        vals.append(i)
    print(vals)
    print(vals[0] * vals[1] * vals[2])


def test():
    # apply_gravity(Moon([3,0,0], [0,0,0]), Moon([5,0,0], [0,0,0]))

    moons = []
    moons.append(Moon(0, [-1,0,2], [0,0,0]))
    moons.append(Moon(1, [2,-10,-7], [0,0,0]))
    moons.append(Moon(2, [4,-8,8], [0,0,0]))
    moons.append(Moon(3, [3,5,-1], [0,0,0]))
    for m in moons:
        print(m)
    sim_moons(moons, 10)

    exit(0)
test()



with open('input.txt', 'r') as f:
# with open('test.txt', 'r') as f:
    input = f.readlines()
    # program_code = [int(x) for x in f.read().split(',')]
    # computer = IntcodeComputer(debug=False)
    moons = []
    for i,line in enumerate(input):
        line = line.replace('>', '')
        line = line.replace('<', '')
        line = line.replace('x=', '')
        line = line.replace('y=', '')
        line = line.replace('z=', '')
        vals = line.strip().split(', ')
        vals = [int(x.strip()) for x in vals]
        print(vals)
        m = Moon(i,vals, [0,0,0])
        moons.append(m)
    print(moons)

    sim_moons(moons, 1000)

# Mem error at 44739242
