from itertools import product

# debug = True
debug = False

class Character():
    def __init__(self, name, hp, damage, armor, mana):
        self.name = name
        self.base_hp = hp
        self.base_damage = damage
        self.base_armor = armor
        self.base_mana = mana
        self.reset()

    def reset(self):
        self.hp = self.base_hp
        self.damage = self.base_damage
        self.armor = self.base_armor
        self.mana = self.base_mana
        self.effects = []

    def __str__(self):
        return '%s has %0d hp, %0d armor, %0d mana' % (self.name, self.hp, self.armor, self.mana)

    def process_effects(self):
        self.armor = self.base_armor
        for e in self.effects:
            if e.timer > 0:
                if e.stat == 'armor':
                    self.armor = self.base_armor + e.delta
                if e.stat == 'mana':
                    self.mana += e.delta
                if e.stat == 'hp':
                    self.hp += e.delta
                    if debug:
                        print('  Poison for', e.delta)
            e.timer -= 1

    def has_effect(self, stat):
        for e in self.effects:
            if e.stat == stat and e.timer > 1:
                return True
        return False


class Effect():
    def __init__(self, stat, delta, timer):
        self.stat = stat
        self.delta = delta
        self.timer = timer


def player_wins(player, boss, spells):
    spent_mana = 0
    for s in spells:
        # Part 2
        player.hp -= 1
        if player.hp <= 0:
            return (False, 0)
        if debug:
            print('-- Player turn --')
            print(player)
            print(boss)
        player.process_effects()
        boss.process_effects()
        if boss.hp <= 0:
            return (True, spent_mana)
        if player.hp <= 0:
            return (False, 0)

        if debug:
            print(' Player casts', s)
        player.mana -= spell_list[s]
        spent_mana += spell_list[s]
        if s == 'Magic Missile':
            boss.hp -= 4
        if s == 'Drain':
            boss.hp -= 2
            player.hp += 2
        if s == 'Shield':
            if player.has_effect('armor'):
                return (False, 0)
            player.effects.append(Effect('armor', 7, 6))
        if s == 'Poison':
            if boss.has_effect('hp'):
                return (False, 0)
            boss.effects.append(Effect('hp', -3, 6))
        if s == 'Recharge':
            if player.has_effect('mana'):
                return (False, 0)
            player.effects.append(Effect('mana', 101, 5))
        # if debug:
        #     print('Boss HP:', boss.hp)
        if player.mana <= 0:
            return (False, 0)
        if boss.hp <= 0:
            return (True, spent_mana)

        if debug:
            print('-- Boss turn --')
            print(player)
            print(boss)
        player.process_effects()
        boss.process_effects()
        if boss.hp <= 0:
            return (True, spent_mana)
        if player.hp <= 0:
            return (False, 0)

        player.hp -= max(boss.damage - player.armor, 1)
        # if debug:
        #     print('Player HP:', player.hp)
        if player.hp <= 0:
            return (False, 0)
    if debug:
        print('Ran out of spells')
    return (False, 0)


boss = Character('Boss', 55, 8, 0, 0)
player = Character('Player', 50, 0, 0, 500)
# boss = Character('Boss', 14, 8, 0, 0)
# player = Character('Player', 10, 0, 0, 250)

spell_list = {'Magic Missile': 53,
              'Drain': 73,
              'Shield': 113,
              'Poison': 173,
              'Recharge': 229}
num_spells = 9
# 7 spells -> 854 too low
# 9 spells -> 953 correct
spells = product(spell_list.keys(), repeat=num_spells)

# spells = [['Recharge', 'Shield', 'Drain', 'Poison', 'Magic Missile']]
# spells = [['Magic Missile', 'Poison', 'Recharge', 'Poison', 'Poison', 'Magic Missile', 'Drain']]
# spells = [['Poison', 'Magic Missile', 'Magic Missile', 'Poison', 'Magic Missile', 'Magic Missile', 'Magic Missile']]
# spells = [['Shield', 'Recharge', 'Poison', 'Magic Missile', 'Magic Missile', 'Poison', 'Magic Missile', 'Magic Missile', 'Magic Missile']]

winning_mana = []
for s in list(spells):
    player.reset()
    boss.reset()
    win, spent_mana = player_wins(player, boss, s)
    if win:
        print(s, spent_mana)
        winning_mana.append(spent_mana)
    # print('Win:', win)

print()
if len(winning_mana):
    print('Min:', min(winning_mana))
else:
    print('No wins')
