import random

from internal import utility as utility


class Weapon:
    def __init__(self, name, cost, range, material_multiplier, attack, defense, attack_skill_multiplier,
                 defense_skill_multiplier, reload_time=0, ammunition=0, projectile_speed=0, shield=False,
                 armor_pierce=0, siege_weapon=False, projectile_size=5):
        self.name = name

        self.cost = cost

        self.range = range

        self.material_multiplier = material_multiplier

        self.attack = attack
        self.defense = defense

        self.attack_skill_multiplier = attack_skill_multiplier
        self.defense_skill_multiplier = defense_skill_multiplier

        self.reload_time = reload_time
        self.ammunition = ammunition
        self.projectile_speed = projectile_speed

        self.projectile_size = projectile_size

        self.shield = shield
        self.armor_pierce = armor_pierce
        self.siege_weapon = siege_weapon

        self.stats = utility.base_weapon_stats()

    def get_info(self):
        res = {}

        res['name'] = self.name
        res['cost'] = self.cost
        res['range'] = self.range
        res['material_multiplier'] = self.material_multiplier
        res['attack'] = self.attack
        res['defense'] = self.defense
        res['attack_skill_multiplier'] = self.attack_skill_multiplier
        res['defense_skill_multiplier'] = self.defense_skill_multiplier
        res['reload_time'] = self.reload_time
        res['ammunition'] = self.ammunition
        res['projectile_speed'] = self.projectile_speed
        res['stats'] = self.stats
        res['shield'] = self.shield
        res['armor_pierce'] = self.armor_pierce

        return res

    def upgrade(self, level):
        self.range += random.randint(0, level)

        self.material_multiplier += random.randint(0, level)

        self.attack += random.randint(0, level)
        self.defense += random.randint(0, level)

        self.reload_time += random.randint(0, level)
        self.ammunition += random.randint(0, level) * 5
        self.projectile_speed += random.randint(0, level)

    def upgrade_skill(self, level):
        self.attack_skill_multiplier += random.randint(0, level) / 5
        self.defense_skill_multiplier += random.randint(0, level) / 5

    def get_attack(self, material):
        effective_attack = self.attack

        if material is not None and self.material_multiplier > 0:
            effective_attack = int(effective_attack * self.material_multiplier * material.effect_strength)

        return random.randint(0, int(effective_attack))

    def get_defense(self, material):
        effective_defense = self.defense

        if material is not None and self.material_multiplier > 0:
            effective_defense = int(effective_defense * self.material_multiplier * material.effect_strength)

        return random.randint(0, int(effective_defense))

    def copy(self):
        return Weapon(self.name, self.cost, self.range, self.material_multiplier, self.attack, self.defense,
                      self.attack_skill_multiplier, self.defense_skill_multiplier, self.reload_time, self.ammunition,
                      self.projectile_speed)

    def __call__(self):
        return self.copy()

    def __repr__(self):
        return '{} (x{}): {} ({}), {} ({})'.format(self.name, self.material_multiplier, self.attack,
                                                   self.attack_skill_multiplier, self.defense,
                                                   self.defense_skill_multiplier)