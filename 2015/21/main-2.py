weapons_input = """
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0
"""
armor_input = """
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
"""
rings_input = """
Damage+1    25     1       0
Damage+2    50     2       0
Damage+3   100     3       0
Defense+1   20     0       1
Defense+2   40     0       2
Defense+3   80     0       3
"""


class Character():
    def __init__(self, hp, damage, armor):
        self.hp = hp
        self.damage = damage
        self.armor = armor


class Item():
    def __init__(self, stats):
        self.name = stats[0]
        self.cost = int(stats[1])
        self.damage = int(stats[2])
        self.armor = int(stats[3])
    def __str__(self):
        return self.name


def get_items(input):
    input = input.strip()
    items = []
    for line in input.splitlines():
        items.append(Item(line.split()))
    return items


def player_wins(player, boss):
    player_hp = player.hp
    boss_hp = boss.hp
    while True:
        boss_hp -= max(player.damage - boss.armor, 1)
        # print('Boss HP:', boss_hp)
        if boss_hp <= 0:
            return True
        player_hp -= max(boss.damage - player.armor, 1)
        # print('Player HP:', player_hp)
        if player_hp <= 0:
            return False


boss = Character(104, 8, 1)
player_hp = 100
# boss = Character(12, 7, 2)
# player_hp = 8

weapons = get_items(weapons_input)
armor = get_items(armor_input)
armor.append(Item(['None', 0, 0, 0]))
rings = get_items(rings_input)
rings.append(Item(['None', 0, 0, 0]))

losing_costs = []
for w in weapons:
    for a in armor:
        for r0 in rings:
            for r1 in rings:
                total_damage = sum([w.damage, a.damage, r0.damage, r1.damage])
                total_armor = sum([w.armor, a.armor, r0.armor, r1.armor])
                total_cost = sum([w.cost, a.cost, r0.cost, r1.cost])
                player = Character(player_hp, total_damage, total_armor)
                win = player_wins(player, boss)
                print(w, a, r0, r1, ' -> ', win)
                if not win:
                    losing_costs.append(total_cost)

print('Max Cost:', max(losing_costs))
