from Tkinter import *
from time import sleep

import random
import math

import utility

import gui
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

        rank_size = random.randint(4, 15)
        ranks = random.randint(4, 6)

        elite = random.randint(2, 6)

        if ranged:
            weapons = [random.choice(nation.basic_ranged_weapon_list), random.choice(nation.sidearm_list)]
        else:
            weapons = [random.choice(nation.basic_weapon_list), random.choice(nation.basic_weapon_list)]

        #weapons = [random.choice(nation.ranged_weapon_list), random.choice(nation.sidearm_list)]

        armor = random.choice(nation.basic_armor_list)

        mount = nation.mount_none

        if random.randint(0, 100) < elite + 5:
            mount = random.choice(nation.basic_mount_list)
        

        tier = 1

        print "Unknown nation has created a new unit: " + str(name) + ", armed with: " + str(weapons[0].name) +", " + str(weapons[1].name) + ", "+str(armor.name)+", "+str(mount.name)+" elite: "+str(elite)

        return cls(name, strength, health, 0, ranged, speed, discipline, rank_size, ranks, weapons, armor, elite, tier, [], mount, troop_nation=nation)

    def __init__(self, name, strength, health, number, ranged, speed, discipline, rank_size, ranks, weapons, armor, elite, tier, upgrades, mount, stats_history=[], arms_history=[], troop_nation=None):
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
        self.mount = mount

        self.upgrades = upgrades

        self.elite = elite

        self.tier = tier

        self.nation = troop_nation

        if arms_history == []:
            self.arms_history = [(self.weapons, self.armor)]
        else:
            self.arms_history = arms_history

        if stats_history == []:
            self.stats_history = [utility.base_soldier_stats()]
        else:
            self.stats_history = stats_history

        self.quality = 0

        if self.nation != None:
            self.nation.troop_tree.append(self)

        self.experience = 1

    #Creates another troop to add to the troop tree
    @classmethod
    def new_troop(cls, self, nation):
        name = nation.language.make_word(nation.language.name_length, True)

        ranged = random.choice([False, True])

        strength = self.strength + random.randint(1, 10 if not ranged else 5)
        health = self.health + random.randint(1, 4 if not ranged else 2)
        discipline = self.discipline + random.randint(0, 1)

        speed = self.speed + random.randint(1, 2)

        rank_size = random.randint(3, 15)
        ranks = random.randint(3, 5)

        if ranged:
            weapons = [random.choice(nation.ranged_weapon_list), random.choice(nation.sidearm_list)]
        else:
            weapons = [random.choice(nation.weapon_list), random.choice(nation.sidearm_list)]

        armor = random.choice(nation.armor_list)

        mount = nation.mount_none

        elite = random.randint(2, 6)

        if random.randint(0, 100) < (elite * 2) + 5:
            mount = random.choice(nation.mount_list)

        print str(nation.name) + " created a new unit: " + str(name) + ", armed with: " + str(weapons[0].name) +", " + str(weapons[1].name) + ", "+str(armor.name)+", "+str(mount.name)
        #e.append(events.EventTroopCreated('TroopCreated', {'nation_a': nation.name, 'army_a': name, 'equip_a':weapons, 'armor_a':armor}, s_parent.get_current_date()))

        return cls(name, strength, health, 0, ranged, speed, discipline, rank_size, ranks, weapons, armor, elite, self.tier + 1, [], mount, troop_nation=nation)

    def get_info(self):
        res = {}
        res['name'] = self.name
        res['strength'] = self.strength
        res['health'] = self.health
        res['number'] = self.number
        res['speed'] = self.speed
        res['ranged'] = self.ranged
        res['discipline'] = self.discipline
        res['rank_size'] = self.rank_size
        res['ranks'] = self.ranks
        res['weapons'] = map(lambda eqp: eqp.get_info(), self.weapons)
        res['armor'] = self.armor.get_info()
        res['elite'] = self.elite
        res['tier'] = self.tier
        res['mount'] = self.mount

        res['upgrades'] = []
        for upgrade in self.upgrades:
            res['upgrades'].append(upgrade.get_info())

        res['arms_history'] = []
        for weapons, armor in self.arms_history:
            res['arms_history'].append((map(lambda eqp: eqp.get_info(), weapons), armor.get_info()))

        res['stats_history'] = self.stats_history

        return res

    def train(self, amount):
        return 0
        #self.elite += random.randint(0, amount)
        #print self.elite

    def upgrade_gear(self):
        return 0
        # if self.quality > 6:
        #     return

        # self.quality += 1

        # #print "upgrading " + str(self.weapons[0].attack)

        # self.weapons[0].upgrade(1)
        # self.weapons[0].upgrade_skill(1)

        # #Sprint "upgrading to" + str(self.weapons[0].attack)

        # self.weapons[1].upgrade(1)
        # self.weapons[1].upgrade_skill(1)

        # self.armor.upgrade(1)
        # self.armor.upgrade_skill(1)

    def save(self, path):
        with open(path + 'army_structure.txt', 'w') as f:
            f.write(str(self.get_info()))

    def handle_battle_end(self, stats):
        self.stats_history[-1] = utility.zip_dict_with(lambda a,b: a + b, self.stats_history[-1], stats)

    def do_rearm(self, nation):
        if self.tier == 1:
            if self.ranged:
                weapons = [random.choice(nation.basic_ranged_weapon_list), random.choice(nation.sidearm_list)]
            else:
                weapons = [random.choice(nation.basic_weapon_list), random.choice(nation.basic_weapon_list)]

            armor = random.choice(nation.basic_armor_list)

            mount = nation.mount_none

            if random.randint(0, 100) < self.elite + 5:
                mount = random.choice(nation.basic_mount_list)
        else:
            if self.ranged:
                weapons = [random.choice(nation.ranged_weapon_list), random.choice(nation.sidearm_list)]
            else:
                weapons = [random.choice(nation.weapon_list), random.choice(nation.sidearm_list)]

            armor = random.choice(nation.armor_list)

            mount = nation.mount_none

            if random.randint(0, 100) < (self.elite * 2) + 5:
                mount = random.choice(nation.mount_list)

        self.weapons = weapons
        self.armor = armor
        self.mount = mount

        self.arms_history.append((self.weapons, self.armor, self.mount))
        self.stats_history.append(utility.base_soldier_stats())

        return self

    def rearm(self, name, new_weapons, new_armor, new_mount):
        if self.name == name:
            self.weapons = new_weapons
            self.armor = new_armor
            self.mount = new_mount
        else:
            for upgrade in self.upgrades:
                upgrade.rearm(name, new_weapons, new_armor, new_mount)

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title(self.name)
        self.gui_window.geometry("400x625+0+0")
        self.gui_window.config(background='white')

        self.ranged_label = gui.Label(self.gui_window, text='Is ranged: {}'.format(self.ranged))
        self.ranged_label.grid(row=0, sticky=W)

        self.mount_label = gui.Label(self.gui_window, text='Mount: {}'.format(self.mount.name))
        self.mount_label.grid(row=1, sticky=W)

        self.strength_label = gui.Label(self.gui_window, text='Strength: {}'.format(self.strength))
        self.strength_label.grid(row=2, sticky=W)

        self.health_label = gui.Label(self.gui_window, text='Health: {}'.format(self.health))
        self.health_label.grid(row=3, sticky=W)

        self.discipline_label = gui.Label(self.gui_window, text='Discipline: {}'.format(self.discipline))
        self.discipline_label.grid(row=4, sticky=W)


        self.discipline_label = gui.Label(self.gui_window, text='Cost: {}'.format(self.get_soldier_cost()))
        self.discipline_label.grid(row=5, sticky=W)

        self.arrangement = gui.Label(self.gui_window, text='Arrangement: {}x{}'.format(self.rank_size, self.ranks))
        self.arrangement.grid(row=6, sticky=W)

        self.arrangement_canvas = Canvas(self.gui_window, width = (self.rank_size + 1) * (TROOP_RADIUS + 1), height= (self.ranks + 1) * (TROOP_RADIUS + 1))
        self.arrangement_canvas.config(background='white')
        self.arrangement_canvas.grid(row=7, sticky=W)

        for x in xrange(1, self.rank_size + 1):
            for y in xrange(1, self.ranks + 1):
                base_x, base_y = x * (TROOP_RADIUS + 1), y * (TROOP_RADIUS + 1)
                self.arrangement_canvas.create_oval(base_x, base_y, base_x + TROOP_RADIUS, base_y + TROOP_RADIUS)

        self.upgrade_label = gui.Label(self.gui_window, text='Upgrades:')
        self.upgrade_label.grid(row=8, sticky=W)

        self.upgrade_buttons = []
        for (i, upgrade) in enumerate(self.upgrades):
            new_upgrade_button = gui.Button(self.gui_window, text=upgrade.name, command=upgrade.show_information_gui)
            new_upgrade_button.grid(row=9, column=i, sticky=W)

            self.upgrade_buttons.append(new_upgrade_button)

        self.history_choice = StringVar()
        self.history_choice.set(self.stringify_history(0))

        self.stats_label = gui.Label(self.gui_window, text='Stats:')
        self.stats_label.grid(row=10, column=0, sticky=W)

        self.stats_choice = OptionMenu(self.gui_window, self.history_choice, *map(self.stringify_history, range(len(self.arms_history))))
        self.stats_choice.config(background='white')
        self.stats_choice['menu'].config(background='white')
        self.stats_choice.grid(row=10, column=1, sticky=W)

        self.stats_select = gui.Button(self.gui_window, text='Select', command=self.select_history)
        self.stats_select.grid(row=10, column=2, sticky=W)

        self.stats_display = Listbox(self.gui_window)
        self.stats_display.grid(row=11, column=0, columnspan=3, sticky=W+E)

        self.select_history()

    def get_soldier_cost(self):
        amount = 0
        for weapon in self.weapons:
            amount += weapon.cost

        amount += self.armor.cost
        amount += self.mount.cost

        return amount

    def stringify_history(self, i):
        weapon_str = ', '.join(map(lambda i: i.name, self.arms_history[i][0]))
        armor_str = self.arms_history[i][1].name
        mount_str = self.mount.name
        return '{}: ({}, {}), {}'.format(i, weapon_str, armor_str, mount_str)

    def select_history(self):
        history_index = int(self.history_choice.get().split(':')[0])

        self.stats_display.delete(0, END)
        for stat in self.stats_history[history_index]:
            self.stats_display.insert(END, '{}: {}'.format(utility.displayify_text(stat), self.stats_history[history_index][stat]))

    def add_number(self, number, nation):
        self.number += number
        #e.append(events.EventArmyRaised('ArmyRaised', {'nation_a': nation.name, 'army_a': self.name, 'raised_a':number}, s_parent.get_current_date()))

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
                    #print str(nation.name) + " raised an army of " + str(number) + " " + str(self.name)
                else:
                    self.number += per_upgrade #Add these people back, because they weren't actually upgraded.

        nation.update_tree(self)

        return self

    def reset(self):
        return self.zero().reset_stats()

    def reset_stats(self):
        self.stats_history = [utility.base_soldier_stats()]

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
        return Troop(self.name, self.strength, self.health, 0, self.ranged, self.speed, self.discipline, self.rank_size, self.ranks, [i.copy() for i in self.weapons], self.armor.copy(), self.elite, self.tier, map(lambda i: i.copy(), self.upgrades), self.mount, stats_history=map(dict, self.stats_history), arms_history=list(self.arms_history))

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
