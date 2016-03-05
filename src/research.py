from Tkinter import *

import random

class Weapon:
    def __init__(self, name, attack, defense, attack_skill_multiplier, defense_skill_multiplier):
        self.name = name

        self.attack = attack
        self.defense = defense

        self.attack_skill_multiplier = attack_skill_multiplier
        self.defense_skill_multiplier = defense_skill_multiplier

    def get_attack(self, soldier):
        return random.randint(0, self.attack) + self.attack_skill_multiplier * soldier.get_attack()

    def get_defense(self, soldier):
        return random.randint(0, self.defense) + self.defense_skill_multiplier * soldier.get_defense()

    def copy(self):
        return Weapon(self.name, self.attack, self.defense, self.attack_skill_multiplier, self.defense_skill_multiplier)

    def __call__(self):
        return self.copy()

    def __repr__(self):
        return '{}: {} ({}), {} ({})'.format(self.name, self.attack, self.attack_skill_multiplier, self.defense, self.defense_skill_multiplier)

#-------------------
# WEAPON DEFINITIONS
#-------------------
unarmed = Weapon('Unarmed', 1, 1, 1, 1)
dagger = Weapon('Dagger', 2, 2, 1.1, 1)
sword = Weapon('Sword', 6, 3, 2, 1.1)
spear = Weapon('Spear', 4, 4, 1.5, 1.5)
pike = Weapon('Pike', 5, 5, 1.5, 1.5)
axe = Weapon('Axe', 8, 2, 2.5, 0.8)

weapon_list = [dagger, sword, spear, axe]

stones = Weapon('Stones', 1, 1, 1, 1)
sling = Weapon('Sling', 3, 1, 1, 1)
bow = Weapon('Bow', 5, 2, 1, 1)

ranged_weapon_list = [sling, bow]

#-------------------

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
