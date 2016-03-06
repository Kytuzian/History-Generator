from Tkinter import *

import random

class Weapon:
    def __init__(self, name, material_multiplier, attack, defense, attack_skill_multiplier, defense_skill_multiplier, reload_time=0, ammunition=0):
        self.name = name

        self.material_multiplier = material_multiplier

        self.attack = attack
        self.defense = defense

        self.attack_skill_multiplier = attack_skill_multiplier
        self.defense_skill_multiplier = defense_skill_multiplier

        self.reload_time = reload_time
        self.ammunition = ammunition

    def copy(self):
        return Weapon(self.name, self.material_multiplier, self.attack, self.defense, self.attack_skill_multiplier, self.defense_skill_multiplier, self.reload_time, self.ammunition)

    def __call__(self):
        return self.copy()

    def __repr__(self):
        return '{}: {} ({}), {} ({})'.format(self.name, self.attack, self.attack_skill_multiplier, self.defense, self.defense_skill_multiplier)

class Armor:
    def __init__(self, name, material_multiplier, defense, defense_skill_multiplier):
        self.name = name

        self.material_multiplier = material_multiplier

        self.defense = defense
        self.defense_skill_multiplier = defense_skill_multiplier

#-----------------------------
# WEAPON AND ARMOR DEFINITIONS
#-----------------------------
unarmed = Weapon('Unarmed', 0, 1, 1, 1, 1)
dagger = Weapon('Dagger', 1.5, 2, 2, 1.1, 1)
rondel = Weapon('Rondel', 1.6, 3, 1, 1.5, 1)
dirk = Weapon('Dirk', 1.6, 3, 1, 1.5, 1)
shortsword = Weapon('Shortsword', 1.8, 5, 2, 2, 1.1)
sword = Weapon('Sword', 2, 6, 3, 2, 1.1)
club = Weapon('Club', 0, 5, 2, 1, 1)
bastard_sword = Weapon('Bastard Sword', 2.3, 7, 2, 2, 1.5)
claymore = Weapon('Claymore', 2.5, 10, 1, 2.5, 0.5)
staff = Weapon('Staff', 0, 3, 3, 2, 2)
spear = Weapon('Spear', 1.0, 4, 4, 1.5, 1.5)
pike = Weapon('Pike', 1.0, 5, 5, 1.5, 1.5)
sarissa = Weapon('Sarissa', 1.0, 7, 3, 2, 2)
bill = Weapon('Bill', 1.5, 6, 4, 1.5, 1.5)
axe = Weapon('Axe', 1.8, 8, 2, 2.5, 0.8)
flail = Weapon('Flail', 1.2, 6, 0, 2, 0.5)
morning_star = Weapon('Morning Star', 1.5, 8, 0, 2, 0.2)

all_melee_weapons = [unarmed, club, dagger, rondel, dirk, shortsword, sword, bastard_sword, claymore, spear, staff, bill, pike, sarissa, axe, flail, morning_star]
weapon_list = [sword, shortsword, bastard_sword, claymore, spear, staff, pike, sarissa, axe, flail, morning_star, bill]

sidearm_list = [dagger, club, rondel, dirk, staff, shortsword, axe, spear]

stones = Weapon('Stones', 0, 1, 1, 1, 1, reload_time=40, ammunition=6)
sling = Weapon('Sling', 0, 3, 1, 1, 1, reload_time=50, ammunition=25)
javelin = Weapon('Javelin', 1.5, 6, 2, 1, 1, reload_time=40, ammunition=3)
bow = Weapon('Bow', 1.5, 5, 1, 2, 1, reload_time=100, ammunition=15)
crossbow = Weapon('Crossbow', 2, 10, 1, 1, 1, reload_time=300, ammunition=15)
sling_staff = Weapon('Sling Staff', 0, 5, 2, 2, 1, reload_time=60, ammunition=20)

all_ranged_weapons = [stones, sling, javelin, bow, crossbow, sling_staff]
ranged_weapon_list = [sling, javelin, bow, crossbow, sling_staff]

basic_ranged_list = [stones, sling, javelin, bow]

#-----------------------------

def base_tech_tree():
    return Tech('Agriculture', 'agriculture', 0, 1.0,
                [
                    Tech('Stone Working', 'material', 30, 1.1,
                    [
                        Tech('Copper', 'material', 100, 1.5,
                        [
                            Tech('Bronze', 'material', 200, 2.0,
                            [
                                Tech('Iron', 'material', 400, 2.5,
                                [
                                    Tech('Steel', 'material', 800, 3.0, [])
                                ])
                            ])
                        ])
                    ]),
                    Tech('Improved Housing', 'housing', 100, 1.5, []),
                    Tech('Improved Mining', 'mining', 150, 2.0, []),
                    Tech('Improved Agriculture', 'agriculture', 100, 1.1, [])
                ])

class Tech:
    def __init__(self, name, category, research_points, effect_strength, next_techs):
        self.name = name
        self.category = category

        self.current_research_points = 0
        self.research_points = research_points

        self.effect_strength = effect_strength

        self.next_techs = next_techs

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

    def get_best_in_category(self, category_name):
        for i in self.next_techs:
            if i.category == category_name and i.is_unlocked():
                return i.get_best_in_category(category_name)

        if self.category == category_name:
            return self

        return None

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
