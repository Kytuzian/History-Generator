import random


class Armor:
    def __init__(self, name, cost, material_multiplier, defense, defense_skill_multiplier, heavy=False):
        self.name = name

        self.cost = cost

        self.material_multiplier = material_multiplier

        self.defense = defense
        self.defense_skill_multiplier = defense_skill_multiplier

        self.heavy = heavy

    def get_info(self):
        res = {}

        res['name'] = self.name
        res['cost'] = self.cost
        res['material_multiplier'] = self.material_multiplier
        res['defense'] = self.defense
        res['defense_skill_multiplier'] = self.defense_skill_multiplier
        res['heavy'] = self.heavy

        return res

    def upgrade(self, level):
        # self.range += random.randint(0, level)

        self.material_multiplier += random.randint(0, level)

        # self.attack += random.randint(0, level)
        self.defense += random.randint(0, level) * 2

        # self.reload_time += random.randint(0, level)
        # self.ammunition += random.randint(0, level) * 5
        # self.projectile_speed += random.randint(0, level)

    def upgrade_skill(self, level):
        # self.attack_skill_multiplier += random.randint(0, level)
        self.defense_skill_multiplier += random.randint(0, level) / 5

    def get_defense(self, material):
        effective_defense = self.defense

        if material is not None and self.material_multiplier > 0:
            effective_defense = int(effective_defense * self.material_multiplier * material.effect_strength)

        return random.randint(0, int(effective_defense))

    def copy(self):
        return Armor(self.name, self.cost, self.material_multiplier, self.defense, self.defense_skill_multiplier,
                     self.heavy)

    def __call__(self):
        return self.copy()

    def __repr__(self):
        return '{} (x{}): {} ({})'.format(self.name, self.material_multiplier, self.defense,
                                          self.defense_skill_multiplier)