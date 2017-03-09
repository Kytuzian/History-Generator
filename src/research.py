from Tkinter import *

import random

import utility

class Weapon:
    def __init__(self, name, cost, range, material_multiplier, attack, defense, attack_skill_multiplier, defense_skill_multiplier, reload_time=0, ammunition=0, projectile_speed=0):
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

        return res

    def get_attack(self, material):
        effective_attack = self.attack

        if material != None and self.material_multiplier > 0:
            effective_attack = int(effective_attack * self.material_multiplier * material.effect_strength)

        return random.randint(0, effective_attack)

    def get_defense(self, material):
        effective_defense = self.defense

        if material != None and self.material_multiplier > 0:
            effective_defense = int(effective_defense * self.material_multiplier * material.effect_strength)

        return random.randint(0, effective_defense)

    def copy(self):
        return Weapon(self.name, self.cost, self.range, self.material_multiplier, self.attack, self.defense, self.attack_skill_multiplier, self.defense_skill_multiplier, self.reload_time, self.ammunition, self.projectile_speed)

    def __call__(self):
        return self.copy()

    def __repr__(self):
        return '{} (x{}): {} ({}), {} ({})'.format(self.name, self.material_multiplier, self.attack, self.attack_skill_multiplier, self.defense, self.defense_skill_multiplier)

class Armor:
    def __init__(self, name, cost, material_multiplier, defense, defense_skill_multiplier):
        self.name = name

        self.cost = cost

        self.material_multiplier = material_multiplier

        self.defense = defense
        self.defense_skill_multiplier = defense_skill_multiplier

    def get_info(self):
        res = {}

        res['name'] = self.name
        res['cost'] = self.cost
        res['material_multiplier'] = self.material_multiplier
        res['defense'] = self.defense
        res['defense_skill_multiplier'] = self.defense_skill_multiplier

        return res

    def get_defense(self, material):
        effective_defense = self.defense

        if material != None and self.material_multiplier > 0:
            effective_defense = int(effective_defense * self.material_multiplier * material.effect_strength)

        return random.randint(0, effective_defense)

    def copy(self):
        return Armor(self.name, self.cost, self.material_multiplier, self.defense, self.defense_skill_multiplier)

    def __call__(self):
        return self.copy()

    def __repr__(self):
        return '{} (x{}): {} ({})'.format(self.name, self.material_multiplier, self.defense, self.defense_skill_multiplier)

#------------------------------
# WEAPON AND ARMOR DEFINITIONS
#------------------------------

#Short
unarmed = Weapon('Unarmed', 0, 5, 0, 1, 1, 1, 1, reload_time=1)
dagger = Weapon('Dagger', 10, 5, 1.5, 2, 2, 1.1, 1, reload_time=2)
rondel = Weapon('Rondel', 25, 5, 1.6, 3, 1, 1.5, 1, reload_time=2)
dirk = Weapon('Dirk', 25, 5, 1.6, 3, 1, 1.5, 1, reload_time=2)
kopis = Weapon('Kopis', 40, 6, 1.8, 6, 1, 2, 1, reload_time=3)
shortsword = Weapon('Shortsword', 50, 7, 1.8, 5, 2, 2, 1.1, reload_time=4)
club = Weapon('Club', 10, 7, 0, 5, 2, 1, 1, reload_time=6)
hammer = Weapon('Hammer', 25, 7, 1.3, 6, 1, 1.5, 0.8, reload_time=5)
mace = Weapon('Mace', 40, 7, 1.5, 6, 1, 1.8, 1.0, reload_time=5)
axe = Weapon('Axe', 30, 7, 1.8, 8, 2, 2.5, 0.8, reload_time=7)
morning_star = Weapon('Morning Star', 200, 7, 1.5, 8, 0, 2, 0.2, reload_time=10)

#Medium
sword = Weapon('Sword', 100, 10, 2, 6, 3, 2, 1.1, reload_time=5)
bastard_sword = Weapon('Bastard Sword', 150, 12, 2.3, 7, 2, 2, 1.5, reload_time=6)
claymore = Weapon('Claymore', 200, 15, 2.5, 10, 1, 2.5, 0.5, reload_time=7)
bill = Weapon('Bill', 50, 12, 1.5, 6, 4, 1.5, 1.5, reload_time=8)
flail = Weapon('Flail', 50, 12, 1.2, 6, 0, 2, 0.5, reload_time=12)
falx = Weapon('Falx', 75, 14, 1.8, 8, 1, 2, 0.8, reload_time=7)

#Long
polehammer = Weapon('Polehammer', 100, 15, 1.0, 8, 2, 2, 1, reload_time=11)
staff = Weapon('Staff', 10, 15, 0, 3, 3, 2, 2, reload_time=7)
spear = Weapon('Spear', 40, 20, 1.0, 4, 4, 1.5, 1.5, reload_time=7)
pike = Weapon('Pike', 80, 25, 1.0, 5, 5, 1.5, 1.5, reload_time=9)
sarissa = Weapon('Sarissa', 160, 35, 1.0, 7, 3, 2, 2, reload_time=12)

all_melee_weapons = [unarmed, polehammer, kopis, mace, falx, club, hammer, dagger, rondel, dirk, shortsword, sword, bastard_sword, claymore, spear, staff, bill, pike, sarissa, axe, flail, morning_star]
weapon_list = [polehammer, sword, mace, falx, shortsword, bastard_sword, claymore, spear, staff, pike, sarissa, axe, flail, morning_star, bill]

sidearm_list = [dagger, club, mace, kopis, hammer, rondel, dirk, staff, shortsword, axe, spear]
basic_weapon_list = [club, mace, hammer, staff, shortsword, axe, spear]

sling = Weapon('Sling', 15, 250, 0, 3, 1, 1.8, 1, reload_time=60, ammunition=25, projectile_speed=7)
javelin = Weapon('Javelin', 100, 125, 0.5, 6, 2, 1.5, 1, reload_time=20, ammunition=3, projectile_speed=5)
atlatl = Weapon('Atlatl', 150, 175, 0.5, 8, 1, 2.0, 1, reload_time=70, ammunition=8, projectile_speed=6)
shortbow = Weapon('Shortbow', 75, 300, 0.5, 4, 1, 2, 1, reload_time=70, ammunition=15, projectile_speed=10)
bow = Weapon('Bow', 125, 350, 0.5, 5, 1, 2, 1, reload_time=80, ammunition=15, projectile_speed=12)
longbow = Weapon('Longbow', 200, 400, 0.5, 6, 1, 2.5, 1, reload_time=90, ammunition=15, projectile_speed=14)
crossbow = Weapon('Crossbow', 250, 450, 1.5, 10, 1, 1, 1, reload_time=200, ammunition=15, projectile_speed=20)
sling_staff = Weapon('Sling Staff', 60, 300, 0, 5, 2, 2, 1, reload_time=60, ammunition=20, projectile_speed=12)

all_ranged_weapons = [atlatl, sling, shortbow, longbow, javelin, bow, crossbow, sling_staff]
ranged_weapon_list = [sling, atlatl, javelin, shortbow, longbow, bow, crossbow, sling_staff]

basic_ranged_weapon_list = [sling, javelin, shortbow, bow]

cloth_armor = Armor('Cloth Armor', 100, 0, 2, 0.5)
padded_armor = Armor('Padded Armor', 200, 0, 3, 0.5)
leather_armor = Armor('Leather Armor', 300, 0, 4, 0.4)
wood_armor = Armor('Wood Armor', 300, 0, 5, 0.3)
chainmail = Armor('Chaimail', 1000, 1, 8, 0.25)
plate = Armor('Plate', 2000, 2, 12, 0.15)

armor_list = [cloth_armor, padded_armor, leather_armor, wood_armor, chainmail, plate]

armor_list = [wood_armor, chainmail, plate]
basic_armor_list = [cloth_armor, leather_armor, wood_armor, padded_armor]

#------------------------------

def base_tech_tree():
    return Tech('Agriculture', 'agriculture', 0, 1.0,
                [
                    Tech('Stone Working', 'material', 400, 1.1,
                    [
                        Tech('Copper', 'material', 1600, 1.5,
                        [
                            Tech('Bronze', 'material', 3200, 2.0,
                            [
                                Tech('Iron', 'material', 6400, 2.5,
                                [
                                    Tech('Steel', 'material', 12800, 3.0, [])
                                ])
                            ])
                        ])
                    ]),
                    Tech('Housing I', 'housing', 250, 1.25,
                    [
                        Tech('Housing II', 'housing', 400, 1.5,
                        [
                            Tech('Housing III', 'housing', 600, 1.75,
                            [
                                Tech('Housing IV', 'housing', 800, 2.0,
                                [
                                    Tech('Housing V', 'housing', 1200, 2.5, [])
                                ])
                            ])
                        ]),
                        Tech('Compact Building I', 'compact_building', 800, 1.15,
                        [
                            Tech('Compact Building II', 'compact_building', 1600, 1.5, [])
                        ])
                    ]),
                    Tech('Mining I', 'mining', 400, 1.25,
                    [
                        Tech('Mining II', 'mining', 600, 1.5,
                        [
                            Tech('Mining III', 'mining', 700, 1.75,
                            [
                                Tech('Mining IV', 'mining', 900, 2.0,
                                [
                                    Tech('Mining V', 'mining', 1200, 2.5, [])
                                ])
                            ])
                        ])
                    ]),
                    Tech('Agriculture I', 'agriculture', 200, 1.1,
                    [
                        Tech('Agriculture II', 'agriculture', 300, 1.2,
                        [
                            Tech('Agriculture III', 'agriculture', 400, 1.3,
                            [
                                Tech('Agriculture IV', 'agriculture', 600, 1.4,
                                [
                                    Tech('Agriculture V', 'agriculture', 800, 1.5, [])
                                ])
                            ])
                        ])
                    ]),
                ])

def tech_categories():
    return ['agriculture', 'material', 'housing', 'mining']

class Tech:
    def __init__(self, name, category, research_points, effect_strength, next_techs):
        self.name = name
        self.category = category

        self.current_research_points = 0
        self.research_points = research_points

        self.effect_strength = effect_strength

        self.next_techs = next_techs

        self.best_techs = {}

        self.get_best_in_categories()

    def get_info(self):
        res = {}
        res['name'] = self.name
        res['category'] = self.category
        res['current_research_points'] = self.current_research_points
        res['research_points'] = self.research_points

        res['effect_strength'] = self.effect_strength
        res['next_techs'] = map(lambda tech: tech.get_info(), self.next_techs)
        # We don't need to save best_techs, we can just recalculate them when we load.

        return res

    def save(self, path):
        with open(path + 'tech.txt', 'w') as f:
            f.write(str(self.get_info()))

    def is_unlocked(self):
        return self.current_research_points >= self.research_points

    def get_tech(self, tech_name):
        if self.name == tech_name and self.is_unlocked():
            return self
        else:
            for next_tech in self.next_techs:
                res = next_tech.get_tech(tech_name)
                if res != None:
                    return res

            return None

    def has_tech(self, tech_name):
        if self.name == tech_name:
            return self.is_unlocked()
        else:
            for next_tech in self.next_techs:
                if has_tech(next_tech, tech_name):
                    return True

            return False

    def get_best_in_categories(self):
        for category in tech_categories():
            self.best_techs[category] = self.get_best_in_category(category, True)

    def get_best_in_category(self, category_name, calc=False):
        if calc or not category_name in self.best_techs:
            for i in self.next_techs:
                if i.category == category_name and i.is_unlocked():
                    return i.get_best_in_category(category_name)

            if self.category == category_name:
                return self

            return None
        else:
            return self.best_techs[category_name]

    def get_available_research(self):
        if self.is_unlocked():
            result = []
            for next_tech in self.next_techs:
                result.extend(next_tech.get_available_research())
            return result
        else:
            return [self]

    def do_research(self, research_amount):
        if not self.is_unlocked():
            self.current_research_points += research_amount

            self.get_best_in_categories()
