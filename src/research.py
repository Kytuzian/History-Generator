from Tkinter import *

import random

class Weapon:
    def __init__(self, name, attack, defense, attack_skill_multiplier, defense_skill_multiplier, reload_time=0, ammunition=0):
        self.name = name

        self.attack = attack
        self.defense = defense

        self.attack_skill_multiplier = attack_skill_multiplier
        self.defense_skill_multiplier = defense_skill_multiplier

        self.reload_time = reload_time
        self.ammunition = ammunition

    def copy(self):
        return Weapon(self.name, self.attack, self.defense, self.attack_skill_multiplier, self.defense_skill_multiplier, self.reload_time, self.ammunition)

    def __call__(self):
        return self.copy()

    def __repr__(self):
        return '{}: {} ({}), {} ({})'.format(self.name, self.attack, self.attack_skill_multiplier, self.defense, self.defense_skill_multiplier)

class Armor:
    def __init__(self, name, material, defense, defense_skill_multiplier):
        self.name = name

        self.material = material

        self.defense = defense
        self.defense_skill_multiplier = defense_skill_multiplier

#-----------------------------
# WEAPON AND ARMOR DEFINITIONS
#-----------------------------
unarmed = Weapon('Unarmed', 1, 1, 1, 1)
dagger = Weapon('Dagger', 2, 2, 1.1, 1)
rondel = Weapon('Rondel', 3, 1, 1.5, 1)
dirk = Weapon('Dirk', 3, 1, 1.5, 1)
shortsword = Weapon('Shortsword', 5, 2, 2, 1.1)
sword = Weapon('Sword', 6, 3, 2, 1.1)
club = Weapon('Club', 5, 2, 1, 1)
bastard_sword = Weapon('Bastard Sword', 7, 2, 2, 1.5)
claymore = Weapon('Claymore', 10, 1, 2.5, 0.5)
staff = Weapon('Staff', 3, 3, 2, 2)
spear = Weapon('Spear', 4, 4, 1.5, 1.5)
pike = Weapon('Pike', 5, 5, 1.5, 1.5)
sarissa = Weapon('Sarissa', 7, 3, 2, 2)
bill = Weapon('Bill', 6, 4, 1.5, 1.5)
axe = Weapon('Axe', 8, 2, 2.5, 0.8)
flail = Weapon('Flail', 6, 0, 2, 0.5)
morning_star = Weapon('Morning Star', 8, 0, 2, 0.2)

all_melee_weapons = [unarmed, club, dagger, rondel, dirk, shortsword, sword, bastard_sword, claymore, spear, staff, bill, pike, sarissa, axe, flail, morning_star]
weapon_list = [sword, shortsword, bastard_sword, claymore, spear, staff, pike, sarissa, axe, flail, morning_star, bill]

sidearm_list = [dagger, club, rondel, dirk, staff, shortsword, axe, spear]

stones = Weapon('Stones', 1, 1, 1, 1, reload_time=40, ammunition=6)
sling = Weapon('Sling', 3, 1, 1, 1, reload_time=50, ammunition=25)
javelin = Weapon('Javelin', 6, 2, 1, 1, reload_time=40, ammunition=3)
bow = Weapon('Bow', 5, 1, 2, 1, reload_time=100, ammunition=15)
crossbow = Weapon('Crossbow', 10, 1, 1, 1, reload_time=300, ammunition=15)
sling_staff = Weapon('Sling Staff', 5, 2, 2, 1, reload_time=60, ammunition=20)

all_ranged_weapons = [stones, sling, javelin, bow, crossbow, sling_staff]
ranged_weapon_list = [sling, javelin, bow, crossbow, sling_staff]

basic_ranged_list = [stones, sling, javelin, bow]

#-----------------------------

def base_tech_tree():
    return Tech('Agriculture', 0, 0,
                [Tech('Stone Working', 30, 0,
                    [Tech('Copper', 100, 0,
                        [Tech('Bronze', 200, 0,
                            [Tech('Iron', 400, 0, [])
                            ])
                        ])
                    ]),
                 Tech('Improved Agriculture', 100, 1.1, [])
                ])

class Tech:
    def __init__(self, name, research_points, effect_strength, next_techs):
        self.name = name

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
