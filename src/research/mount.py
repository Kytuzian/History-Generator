import random


class Mount:
    def __init__(self, name, cost, speed, attack, defense, attack_skill_multiplier, defense_skill_multiplier,
                 heavy=False):
        self.name = name

        self.cost = cost

        self.speed = speed
        self.attack = attack
        self.defense = defense
        self.attack_skill_multiplier = attack_skill_multiplier
        self.defense_skill_multiplier = defense_skill_multiplier

        self.heavy = heavy

    def get_info(self):
        res = {}

        res['name'] = self.name
        res['cost'] = self.cost
        res['speed'] = self.speed
        res['attack'] = self.attack
        res['defense'] = self.defense
        res['attack_skill_multiplier'] = self.attack_skill_multiplier
        res['defense_skill_multiplier'] = self.defense_skill_multiplier
        res['heavy'] = self.heavy

        return res

    def get_defense(self):
        effective_defense = self.defense
        return random.randint(0, int(effective_defense))

    def copy(self):
        return Mount(self.name, self.cost, self.speed, self.attack, self.defense, self.attack_skill_multiplier,
                     self.defense_skill_multiplier, self.heavy)

    def __call__(self):
        return self.copy()

    def __repr__(self):
        return '{} ({}, {})'.format(self.name, self.attack, self.defense)