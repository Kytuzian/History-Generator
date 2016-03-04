from Tkinter import *

import random

#start - establish basic modifiers

def tech_effects():
    return {'population_capacity': 1.0, 'food_output': 1.0, 'strength': 1.0, 'health': 1.0, 'armor': 0.0, 'tax_rate': 1.0, 'soldier_upkeep': 1.0, 'soldier_cost': 1.0}
def base_tech_tree():
    return Tech('start', tech_effects(), 0, [])

def has_tech(tech_tree, tech_name):
    if tech_tree.name == tech_name:
        return True
    else:
        for next_tech in tech_tree.next_techs:
            if has_tech(next_tech, tech_name):
                return True

        return False

def modify_effects(base_effects, effect, mod_value, mod_type='add'):
    new_effects = dict(base_effects)

    if mod_type == 'add':
        new_effects[effect] += mod_vaue
    else:
        new_effects[effect] *= mod_value

    return new_effects

class Tech:
    def __init__(self, name, effects, research_points, next_techs):
        self.name = name
        self.effects = effects

        self.current_research_points = 0
        self.research_points = research_points

        self.next_techs = next_techs

    def is_unlocked(self):
        return self.current_research_points >= self.research_points

    def get_effects(self):
        effect_multipliers = dict(self.effects) #Don't want to modify this tech's effects

        for next_tech in self.next_techs:
            next_tech_effects = next_tech.get_effects()

            for effect in next_tech.effects:
                base_effects[effect] *= next_tech.effects[effects]

        return effect_multipliers

    def history_step(self, research_amount):
        if not self.is_unlocked:
            self.current_research_points += research_amount
