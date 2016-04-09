from Tkinter import *
from time import sleep

import random
import math

import utility

from nation import *
from language import *
from battle import TROOP_RADIUS

from research import all_ranged_weapons, unarmed

class Troop:
    @classmethod
    def init_troop(cls, name, nation):
        strength = random.randint(1, 3)
        health = random.randint(1, 3)
        ranged = random.choice([False, True]) #Starting troops are always melee random.choice([False, True])

        speed = random.randint(2, 4)

        discipline = random.randint(1, 2)

        rank_size = random.randint(2, 20)
        ranks = random.randint(2, 5)

        elite = random.randint(2, 10)

        if ranged:
            weapons = [random.choice(nation.basic_ranged_weapon_list), random.choice(nation.sidearm_list)]
        else:
            weapons = [random.choice(nation.basic_weapon_list), random.choice(nation.basic_weapon_list)]

        armor = random.choice(nation.basic_armor_list)

        tier = 1

        return cls(name, strength, health, 0, ranged, speed, discipline, rank_size, ranks, weapons, armor, elite, tier, [])

    def __init__(self, name, strength, health, number, ranged, speed, discipline, rank_size, ranks, weapons, armor, elite, tier, upgrades):
        self.name = name
        self.strength = strength
        self.health = health
        self.number = number

        self.speed = speed

        self.originally_ranged = ranged #This one won't change when the unit swiches to melee mode.
        self.ranged = ranged

        self.discipline = discipline

        self.rank_size = rank_size
        self.ranks = ranks

        self.weapons = weapons
        self.armor = armor

        self.upgrades = upgrades

        self.elite = elite

        self.tier = tier

    #Creates another troop to add to the troop tree
    @classmethod
    def new_troop(cls, self, nation):
        name = nation.language.make_word(nation.language.name_length, True)

        ranged = random.choice([False, True])

        strength = self.strength + random.randint(1, 20 if not ranged else 10)
        health = self.health + random.randint(1, 6 if not ranged else 2)
        discipline = self.discipline + random.randint(1, 10)

        speed = self.speed + random.randint(1, 4)

        rank_size = random.randint(2, 18)
        ranks = random.randint(2, 6)

        if ranged:
            weapons = [random.choice(nation.ranged_weapon_list), random.choice(nation.sidearm_list)]
        else:
            weapons = [random.choice(nation.weapon_list), random.choice(nation.sidearm_list)]

        armor = random.choice(nation.armor_list)

        elite = random.randint(2, 10)

        return cls(name, strength, health, 0, ranged, speed, discipline, rank_size, ranks, weapons, armor, elite, self.tier + 1, [])

    def do_rearm(self, nation):
        if self.tier == 1:
            if self.ranged:
                weapons = [random.choice(nation.basic_ranged_weapon_list), random.choice(nation.sidearm_list)]
            else:
                weapons = [random.choice(nation.basic_weapon_list), random.choice(nation.basic_weapon_list)]

            armor = random.choice(nation.basic_armor_list)
        else:
            if self.ranged:
                weapons = [random.choice(nation.ranged_weapon_list), random.choice(nation.sidearm_list)]
            else:
                weapons = [random.choice(nation.weapon_list), random.choice(nation.sidearm_list)]

            armor = random.choice(nation.armor_list)

        self.weapons = weapons
        self.armor = armor

        return self

    def rearm(self, name, new_weapons, new_armor):
        if self.name == name:
            self.weapons = new_weapons
            self.armor = new_armor
        else:
            for upgrade in self.upgrades:
                upgrade.rearm(name, new_weapons, new_armor)

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title(self.name)
        self.gui_window.geometry("300x325+0+0")

        self.ranged_label = Label(self.gui_window, text='Is ranged: {}'.format(self.ranged))
        self.ranged_label.grid(row=0, sticky=W)

        self.strength_label = Label(self.gui_window, text='Strength: {}'.format(self.strength))
        self.strength_label.grid(row=1, sticky=W)

        self.health_label = Label(self.gui_window, text='Health: {}'.format(self.health))
        self.health_label.grid(row=2, sticky=W)

        self.discipline_label = Label(self.gui_window, text='Discipline: {}'.format(self.discipline))
        self.discipline_label.grid(row=3, sticky=W)

        self.arrangement = Label(self.gui_window, text='Arrangement: {}x{}'.format(self.rank_size, self.ranks))
        self.arrangement.grid(row=4, sticky=W)

        self.arrangement_canvas = Canvas(self.gui_window, width = (self.rank_size + 1) * (TROOP_RADIUS + 1), height= (self.ranks + 1) * (TROOP_RADIUS + 1))
        self.arrangement_canvas.grid(row=5, sticky=W)

        for x in xrange(1, self.rank_size + 1):
            for y in xrange(1, self.ranks + 1):
                base_x, base_y = x * (TROOP_RADIUS + 1), y * (TROOP_RADIUS + 1)
                self.arrangement_canvas.create_oval(base_x, base_y, base_x + TROOP_RADIUS, base_y + TROOP_RADIUS)

        self.upgrade_label = Label(self.gui_window, text='Upgrades:')
        self.upgrade_label.grid(row=6, sticky=W)

        self.upgrade_buttons = []
        for (i, upgrade) in enumerate(self.upgrades):
            new_upgrade_button = Button(self.gui_window, text=upgrade.name, command=upgrade.show_information_gui)
            new_upgrade_button.grid(row=7, column=i, sticky=W)

            self.upgrade_buttons.append(new_upgrade_button)

    def add_number(self, number, nation):
        self.number += number

        if self.number > self.elite**sqrt(self.tier): #If we have enough troops, we will create another, better, rank of troops
            if len(self.upgrades) < 3:
                self.upgrades.append(Troop.new_troop(self, nation))

                self.upgrades[-1].upgrades = [] #Because it wants to put itself as an upgrade, for some reason. TODO

        if self.number < 0:
            self.number = 0

        #Upgrade troops if possible.
        if self.number > (self.elite * self.tier) and len(self.upgrades) > 0:
            upgrading = random.randint(1, self.number // self.elite)
            self.number -= upgrading

            per_upgrade = upgrading // len(self.upgrades)
            for upgrade in self.upgrades:
                total_cost = nation.get_soldier_cost(upgrade)

                if nation.money > total_cost:
                    upgrade.add_number(per_upgrade, nation)
                else:
                    self.number += per_upgrade #Add these people back, because they weren't actually upgraded.

        return self

    def zero(self):
        return self.copy().remove_number('', self.size())

    def add_army(self, other):
        self.add_to(other.name, other.number)

        for i in other.upgrades:
            self.add_army(i)

    def add_to(self, type, number):
        if self.name == type:
            self.number += number

            return self
        else:
            for upgrade in self.upgrades:
                if upgrade.name == type:
                    upgrade.number += number

                    return self

            for upgrade in self.upgrades:
                val = upgrade.add_to(type, number)

                if val != None:
                    return self

            return None

    #Returns a list of the unit + it's upgrades
    def make_upgrade_list(self):
        return sorted([self] + reduce(lambda a, b: a + b, [i.make_upgrade_list() for i in self.upgrades], []), key=lambda a: a.strength * a.health)

    def copy(self):
        return Troop(self.name, self.strength, self.health, 0, self.ranged, self.speed, self.discipline, self.rank_size, self.ranks, [i.copy() for i in self.weapons], self.armor.copy(), self.elite, self.tier, map(lambda i: i.copy(), self.upgrades))

    def is_empty(self):
        return all(map(lambda i: i.is_empty(), self.upgrades)) and self.number == 0

    def trim_empty(self):
        i = 0
        while i < len(self.upgrades):
            if self.upgrades[i].is_empty():
                self.upgrades.pop(i)
            else:
                self.upgrades[i] = self.upgrades[i].trim_empty()

                i += 1

        return self

    def take_number(self, number):
        upgrade_list = self.make_upgrade_list()

        result = self.copy()

        for upgrade in upgrade_list:
            upgraded_amount = 0

            if upgrade.number > number:
                upgrade.number -= number
                upgraded_amount = number

                number = 0
            else:
                upgraded_amount = upgrade.number
                number -= upgrade.number

                upgrade.number = 0

            result.add_to(upgrade.name, upgraded_amount)

            if number == 0:
                break

        return result.trim_empty()

    def remove_number(self, type, number):
        if type == '':
            upgrade_list = self.make_upgrade_list()

            for upgrade in upgrade_list:
                if upgrade.number > number:
                    upgrade.number -= number

                    number = 0

                    return self
                else:
                    number -= upgrade.number

                    upgrade.number = 0

            return self
        else:
            if type == self.name:
                self.number -= number

                return self.number

            for i in self.upgrades:
                if i.name == type:
                    i.number -= number

                    return i.number

            #If not found in any of them, let's check all the children
            for i in self.upgrades:
                val = i.remove_number(type, number)

                if val >= 0:
                    return val

            return -1

    def size(self):
        return self.number + sum(map(lambda t: t.size(), self.upgrades))

    def merge_all(self, other):
        if self.name == other.name:
            self.number += other.number

            for index, upgrade in enumerate(other.upgrades):
                if not upgrade in self.upgrades:
                    self.upgrades.append(upgrade.copy())

                    self.upgrades[-1] = self.upgrades[-1].merge_all(upgrade)
                else:
                    self_upgrade = self.upgrades.index(upgrade)

                    self.upgrades[self_upgrade] = self.upgrades[self_upgrade].merge_all(upgrade)

            return self

    def merge_structure(self, other):
        result = self.zero()

        if result.name == other.name:
            for index, upgrade in enumerate(other.upgrades):
                if not upgrade in result.upgrades:
                    result.upgrades.append(upgrade.zero())

                    result.upgrades[-1] = result.upgrades[-1].merge_structure(upgrade)
                else:
                    self_upgrade = self.upgrades.index(upgrade)

                    result.upgrades[self_upgrade] = result.upgrades[self_upgrade].merge_structure(upgrade)

        return result

    def __eq__(self, other):
        try:
            return self.name == other.name
        except:
            return False

    def __repr__(self):
        return "{0}({1}, {2}): {3} {4}".format(self.name, self.strength, self.health, self.number, self.upgrades)
