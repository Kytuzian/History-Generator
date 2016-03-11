from Tkinter import *
from time import sleep

import random
import math

import utility

from nation import *
from language import *

from research import all_melee_weapons, weapon_list,\
                     basic_weapon_list,\
                     all_ranged_weapons, ranged_weapon_list,\
                     sidearm_list, basic_ranged_list,\
                     all_armor_list, armor_list,\
                     basic_armor_list, unarmed

PROJECTILE_MOVEMENT_SPEED = 6
PROJECTILE_RADIUS = 3

TROOP_MOVEMENT_SPEED = 1
TROOP_RADIUS = 5

#How many steps away the target unit should be before switching to melee.
CC_RANGE = 50

#How often on average to check for a new target for the unit
SWITCH_TARGET_COUNT = 8

#The maximum number of troops on either side of the battle
BATTLE_SIZE = 250

class Troop:
    @classmethod
    def init_troop(cls, name):
        strength = random.randint(1, 3)
        health = random.randint(1, 3)
        ranged = random.choice([False, True]) #Starting troops are always melee random.choice([False, True])

        discipline = random.randint(1, 2)

        rank_size = random.randint(2, 20)
        ranks = random.randint(2, 5)

        elite = random.randint(2, 10)

        if ranged:
            weapons = [random.choice(basic_ranged_list), random.choice(sidearm_list)]
        else:
            weapons = [random.choice(basic_weapon_list), random.choice(basic_weapon_list)]

        armor = random.choice(basic_armor_list)

        tier = 1

        return cls(name, strength, health, 0, ranged, discipline, rank_size, ranks, weapons, armor, elite, tier, [])

    def __init__(self, name, strength, health, number, ranged, discipline, rank_size, ranks, weapons, armor, elite, tier, upgrades):
        self.name = name
        self.strength = strength
        self.health = health
        self.number = number

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

        rank_size = random.randint(2, 18)
        ranks = random.randint(2, 6)

        if ranged:
            weapons = [random.choice(ranged_weapon_list), random.choice(sidearm_list)]
        else:
            weapons = [random.choice(weapon_list), random.choice(sidearm_list)]

        armor = random.choice(armor_list)

        elite = random.randint(2, 10)

        return cls(name, strength, health, 0, ranged, discipline, rank_size, ranks, weapons, armor, elite, self.tier + 1, [])

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
            upgrading = random.randint(1, self.number // self.elite // self.tier)
            self.number -= upgrading

            per_upgrade = upgrading // len(self.upgrades)
            for upgrade in self.upgrades:
                upgrade.add_number(per_upgrade, nation)

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
        return Troop(self.name, self.strength, self.health, 0, self.ranged, self.discipline, self.rank_size, self.ranks, [i.copy() for i in self.weapons], self.armor.copy(), self.elite, self.tier, map(lambda i: i.copy(), self.upgrades))

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

class Soldier:
    def __init__(self, unit, name, health, strength, ranged, weapons, armor, discipline, canvas):
        self.unit = unit

        self.name = name
        self.health = health
        self.strength = strength

        self.ranged = ranged

        self.weapons = weapons
        self.armor = armor

        use_weapon = self.get_ranged_weapon()

        if use_weapon == None:
            self.shoot = 0
            self.shoot_counter = 0
        else:
            # print('Reload time: {}'.format(use_weapon.reload_time))
            self.shoot = 0
            self.shoot_counter = use_weapon.reload_time

        self.discipline = discipline

        self.fatigue = 2

        self.target = None
        self.targeted = None

        self.id = -1

        self.x = 0
        self.y = 0

        self.canvas = canvas

    def get_melee_weapon(self):
        for weapon in self.weapons:
            if weapon.name in map(lambda w: w.name, all_melee_weapons):
                return weapon

                break

        return None

    def get_ranged_weapon(self):
        for weapon in self.weapons:
            if weapon.name in map(lambda w: w.name, all_ranged_weapons):
                return weapon

        return None

    def calculate_position(self):
        coords = self.canvas.coords(self.id)[:2]

        if len(coords) == 2:
            self.x, self.y = coords

            return (self.x, self.y)
        else:
            return (-1, -1)

    def get_ranged_attack(self, material):
        fatigue_loss = random.randint(0, self.fatigue // 2)

        #Find our ranged weapon. Should be first, but better to check in case it's not.
        use_weapon = self.get_ranged_weapon()

        if use_weapon == None: #Shouldn't actually happen, but just in case.
            return random.randint(0, 1)
        else:
            weapon_attack = use_weapon.get_attack(material)
            normal_attack = use_weapon.attack_skill_multiplier * random.randint(0, self.strength)

            result = weapon_attack + normal_attack - fatigue_loss

            # print('{} from weapon ({}), {} from strength, {} lost from fatigue = {}'.format(weapon_attack, use_weapon.name, normal_attack, fatigue_loss, result))

            if result > 0:
                return result
            else:
                return random.randint(0, 1)

    def get_melee_attack(self, material):
        fatigue_loss = random.randint(0, self.fatigue // 2)

        #Find our melee weapon
        use_weapon = self.get_melee_weapon()

        if use_weapon == None: #This could happen if ALL of our weapons have broken.
            use_weapon = unarmed()

        weapon_attack = use_weapon.get_attack(material)
        normal_attack = use_weapon.attack_skill_multiplier * random.randint(0, self.strength)

        result = weapon_attack + normal_attack - fatigue_loss

        # print('{} from weapon ({}), {} from strength, {} lost from fatigue = {}'.format(weapon_attack, use_weapon.name, normal_attack, fatigue_loss, result))

        if result > 0:
            return result
        else:
            return random.randint(0, 1)

    def get_ranged_defense(self, material):
        fatigue_loss = random.randint(0, self.fatigue // 2)
        armor_defense = self.armor.get_defense(material)
        skill_defense = self.armor.defense_skill_multiplier * random.randint(0, self.strength)

        return max(0, armor_defense + skill_defense - fatigue_loss)

    def get_melee_defense(self, material):
        fatigue_loss = random.randint(0, self.fatigue // 2)

        #Find our ranged weapon. Should be first, but better to check in case it's not.
        use_weapon = self.get_melee_weapon()

        if use_weapon == None: #This could happen if ALL of our weapons have broken.
            use_weapon = unarmed()

        weapon_defense = use_weapon.get_defense(material)
        armor_defense = self.armor.get_defense(material)
        normal_defense = self.armor.defense_skill_multiplier * use_weapon.defense_skill_multiplier * random.randint(0, self.strength)

        result = weapon_defense + armor_defense + normal_defense - fatigue_loss

        # print('{} from weapon ({}), {} from armor ({}), {} from strength, {} lost from fatigue = {}'.format(weapon_defense, use_weapon.name, armor_defense, self.armor.name, normal_defense, fatigue_loss, result))

        if result > 0:
            return result
        else:
            return random.randint(0, 1)

class Projectile:
    def __init__(self, (dx, dy), strength, target):
        self.dx = dx
        self.dy = dy

        self.skip_step = 0
        self.kill_range = 1000

        self.strength = strength / 2

        if self.strength <= 0:
            self.strength = 1

        self.id = -1

        self.target = target

class Unit:
    def __init__(self, soldier_type, soldiers, canvas):
        self.soldier_type = soldier_type

        self.soldiers = soldiers

        self.target = None
        self.targeted = None

        self.x = 0
        self.y = 0

        self.name_id = 0

        self.shoot_angle = 0
        self.shoot_time = 0
        self.shoot_position = (0, 0)

        use_weapon = None
        for weapon in self.soldier_type.weapons:
            if weapon.name in map(lambda w: w.name, all_ranged_weapons):
                use_weapon = weapon

        if use_weapon == None:
            self.ammunition = 0
        else:
            self.ammunition = use_weapon.ammunition * len(soldiers)

        self.canvas = canvas

    def get_movement_vector(self, vector_format='xy'):
        if self.target != None and not self.soldier_type.ranged:
            d = utility.distance((self.x, self.y), (self.target.x, self.target.y))
            dx = self.target.x - self.x
            dy = self.target.y - self.y

            if vector_format == 'xy':
                return (float(dx) / d * TROOP_MOVEMENT_SPEED, float(dy) / d * TROOP_MOVEMENT_SPEED)
            elif vector_format == 'polar': #Magnitude and angle
                return (TROOP_MOVEMENT_SPEED, math.atan2(dy, dx))
        else:
            return (0, 0)

    def calculate_shoot_position(self):
        self.calculate_shoot_angle()

        x = PROJECTILE_MOVEMENT_SPEED * math.cos(self.shoot_angle) * self.shoot_time
        y = PROJECTILE_MOVEMENT_SPEED * math.sin(self.shoot_angle) * self.shoot_time

        self.shoot_position = (x, y)

        return self.shoot_position

    def calculate_shoot_angle(self):
        if self.target != None:
            speed, angle = self.target.get_movement_vector(vector_format='polar')
            # print((speed, PROJECTILE_MOVEMENT_SPEED, (self.target.x, self.target.y), (self.x, self.y), angle))
            self.shoot_time, self.shoot_angle = utility.calculate_interception(speed, PROJECTILE_MOVEMENT_SPEED, (self.target.x, self.target.y), (self.x, self.y), angle)
        else:
            self.shoot_angle = 0

        return self.shoot_angle

    def get_position(self):
        return (self.x, self.y)

    def calculate_position(self):
        total_x = 0
        total_y = 0

        for i in self.soldiers:
            sx, sy = i.calculate_position()

            if sx >= 0 and sy >= 0:
                total_x += sx
                total_y += sy
            else:
                self.soldiers.remove(i)

        if len(self.soldiers) > 0:
            self.x = total_x // len(self.soldiers)
            self.y = total_y // len(self.soldiers)

        return (self.x, self.y)

class Battle:
    def __init__(self, nation_a, a_army, nation_b, b_army, attacking_city, city, battle_over):
        self.a = nation_a
        self.b = nation_b

        self.a_army = a_army
        self.b_army = b_army

        self.parent = Tk()
        self.parent.title("{}({}) vs. {}({})".format(self.a.name, self.a_army.size(), self.b.name, self.b_army.size()))
        self.parent.geometry("1000x600+0+0")

        if utility.START_BATTLES_MINIMIZED:
            self.parent.wm_state('iconic')

        self.delay = 1

        self.canvas = Canvas(self.parent, width=1000, height=600)
        self.canvas.pack()

        self.force_a = []
        self.force_b = []

        self.proj_a = []
        self.proj_b = []

        self.battle_over = battle_over
        self.over = False

        self.a_amount = 0
        self.b_amount = 0

        self.attacking_city = attacking_city
        self.city = city

        self.create_gui()

    def create_gui(self):
        self.battle_speed = Scale(self.parent, from_=1, to=200, orient=HORIZONTAL)
        self.battle_speed.pack()
        self.battle_speed.place(x=10, y=30)

        self.battle_speed_label = Label(self.parent, text='Battle Speed (ms):')
        self.battle_speed_label.pack()
        self.battle_speed_label.place(x=10, y = 10)

    def setup_army(self, army, force, color, (xmin, xmax), (ymin, ymax), limit):
        sx, sy = 0, 0

       # print("Setting up a max of {} soldiers of {} for this unit type.".format(limit, army.number))

        for soldier in xrange(army.number):
            if soldier % (army.ranks * army.rank_size) == 0:
                force.append(Unit(army.zero(), [], self.canvas))

                sx, sy = random.randint(xmin, xmax), random.randint(ymin, ymax)

            force[-1].soldiers.append(Soldier(force[-1], army.name, army.health, army.strength, army.ranged, army.weapons, army.armor, army.discipline, self.canvas))

            x,y = sx + len(force[-1].soldiers[:-1]) % army.rank_size * (TROOP_RADIUS + 1), sy + len(force[-1].soldiers[:-1]) / army.rank_size * (TROOP_RADIUS + 1)

            force[-1].soldiers[-1].id = self.canvas.create_oval(x, y, x + TROOP_RADIUS, y + TROOP_RADIUS, fill=color)

            limit -= 1
            army.number -= 1

            if limit <= 0:
                return

        if len(army.upgrades) > 0:
            for i in army.upgrades:
                self.setup_army(i, force, color, (xmin, xmax), (ymin, ymax), limit)

    def setup_soldiers(self):
        if self.a_army.size() > self.b_army.size():
            self.a_amount = BATTLE_SIZE
            self.b_amount = int(BATTLE_SIZE * (float(self.b_army.size() + 1) / float(self.a_army.size() + 1)))
        else:
            self.a_amount = int(BATTLE_SIZE * (float(self.a_army.size() + 1) / float(self.b_army.size() + 1)))
            self.b_amount = BATTLE_SIZE

        self.setup_army(self.a_army, self.force_a, self.a.color, (100, 900), (50, 300), self.a_amount)
        self.setup_army(self.b_army, self.force_b, self.b.color, (100, 900), (300, 550), self.b_amount)

    def get_nearest_enemy(self, unit, check, check_unit = None):
        min_distance = 1000000000

        target = None

        for i in check:
            d = utility.distance_squared((unit.x, unit.y), (i.x, i.y))

            if d < min_distance:
                target = i

                min_distance = d

        return target

    def handle_projectiles(self, owner_nation, proj, enemy, enemy_force):
        i = 0
        for p in proj:
            hit = False

            self.canvas.move(p.id, p.dx * PROJECTILE_MOVEMENT_SPEED, p.dy * PROJECTILE_MOVEMENT_SPEED)

            x,y = self.canvas.coords(p.id)[:2]

            try:
                tx,ty = self.canvas.coords(p.target.id)[:2]

                if p.skip_step <= 0:
                    if p.kill_range > 0:
                        p.kill_range -= 1

                        if utility.collided((x, y, PROJECTILE_RADIUS), (tx, ty, TROOP_RADIUS)):
                            hit = True

                            damage = p.strength

                            #Allow the troop being hit by the projectile to try and defend a little.
                            defense = p.target.get_ranged_defense(owner_nation.tech.get_best_in_category('material'))

                            if random.randint(0, p.target.discipline) == 0:
                                p.target.fatigue += 1

                            #Can't do more damage than we would've originally, and can't do less than 0
                            total_damage = max(damage - defense, 0)

                            # print('Damage {} - Defense {} = {}'.format(damage, defense, total_damage))

                            p.target.health -= total_damage

                            if p.target.health <= 0:
                                self.canvas.delete(p.target.id)

                                if len(p.target.unit.soldiers) == 1: #Remove one more, like we are about to, and it's empty
                                    self.canvas.delete(p.target.unit.name_id)
                                    enemy_force.remove(p.target.unit)
                                else:
                                    if p.target in p.target.unit.soldiers:
                                        p.target.unit.soldiers.remove(p.target)
                else:
                    p.skip_step -= 1

                if hit or x < 0 or x > 1000 or y < 0 or y > 600:
                    self.canvas.delete(p.id)

                    proj.remove(p)
            except: #Remove this if we don't have a target
                self.canvas.delete(p.id)

                proj.remove(p)

    def check_end_battle(self):
        #if there are no units left, end the battle
        if (self.size(self.force_a) <= 0 and self.a_army.size() <= 0) or (self.size(self.force_b) <= 0 and self.b_army.size() <= 0):
            #Zero the army just in case anything got messed up
            if self.size(self.force_a) <= 0: #A is always the attackers
                self.a_army.remove_number('', self.a_army.size())
            elif self.size(self.force_b) <= 0:
                self.b_army.remove_number('', self.b_army.size())

                for i in self.force_a:
                    self.a_army.add_to(i.soldier_type.name, len(i.soldiers))
            self.parent.destroy()

            self.over = True
            self.battle_over(self)

            return True
        else:
            return False

    def handle_units(self, force, nation, proj, enemy_force, enemy_nation, color):
        for current_unit in force:
            if self.check_end_battle():
                return True

            if len(current_unit.soldiers) == 0: #No soldiers, remove this and untarget
                if current_unit.targeted != None:
                    current_unit.targeted.target = None

                force.remove(current_unit)

                continue

            self.canvas.coords(current_unit.name_id, current_unit.x, current_unit.y - 20)

            if current_unit.target != None: #if we have a target make sure it still exists
                if not current_unit.target in enemy_force:
                    current_unit.target = None

            current_unit.calculate_position()

            #If we don't have a target, target the closest unit.
            if current_unit.target == None or random.randint(0, SWITCH_TARGET_COUNT) == 0:
                current_unit.target = self.get_nearest_enemy(current_unit, enemy_force)

                if current_unit.target != None:
                    current_unit.target.targeted = current_unit
                else:
                    continue

            for soldier in current_unit.soldiers:
                if current_unit.target == None:
                    continue

                if soldier.target != None: #If we have a target, make sure it still exists.
                    if not soldier.target in current_unit.target.soldiers:
                        soldier.target = None

                if soldier.target == None:
                    soldier.target = random.choice(current_unit.target.soldiers) #self.get_nearest_enemy(soldier, current_unit.target.soldiers)

                    if soldier.target != None:
                        soldier.target.targeted = soldier
                    else:
                        continue

                x, y = soldier.x, soldier.y
                tx, ty = soldier.target.x, soldier.target.y

                d = utility.distance((x, y), (tx, ty))

                if soldier.ranged:
                    if d < TROOP_MOVEMENT_SPEED * CC_RANGE:
                        soldier.ranged = False

                    if d > soldier.get_ranged_weapon().range:
                        self.canvas.move(soldier.id, (tx - x) / d * TROOP_MOVEMENT_SPEED, (ty - y) / d * TROOP_MOVEMENT_SPEED)
                    elif soldier.shoot > soldier.shoot_counter:
                        if d > 0 and current_unit.ammunition > 0:
                            m, tangle = current_unit.target.get_movement_vector(vector_format='polar')

                            if m > 0:
                                t, angle = utility.calculate_interception(m, PROJECTILE_MOVEMENT_SPEED, (tx, ty), (x, y), tangle)

                                tx += math.cos(tangle) * t * m
                                ty += math.sin(tangle) * t * m

                                d = utility.distance((x, y), (tx, ty))

                            damage = soldier.get_ranged_attack(nation.tech.get_best_in_category('material'))
                            proj.append(Projectile(((tx - x) / d, (ty - y) / d), damage, soldier.target))

                            proj[-1].id = self.canvas.create_oval(x, y, x + PROJECTILE_RADIUS, y + PROJECTILE_RADIUS, width=0, fill=color)
                            proj[-1].skip_step = d // PROJECTILE_MOVEMENT_SPEED // 2
                            proj[-1].kill_range = d // PROJECTILE_MOVEMENT_SPEED * 2

                            soldier.shoot = 0

                            current_unit.ammunition -= 1
                        else:
                            for s in current_unit.soldiers:
                                s.ranged = False

                            current_unit.soldier_type.ranged = False
                    else:
                        soldier.shoot += sqrt(soldier.discipline) / 2 + random.randint(0, 1) * log(soldier.discipline)
                else:
                    #If the target moves out of range, then switch back to ranged.
                    if d > TROOP_MOVEMENT_SPEED * CC_RANGE:
                        if current_unit.soldier_type.ranged:
                            soldier.ranged = True

                    if d < soldier.get_melee_weapon().range:
                        attack = soldier.get_melee_attack(nation.tech.get_best_in_category('material'))
                        defense = soldier.target.get_melee_defense(enemy_nation.tech.get_best_in_category('material'))

                        if random.randint(0, soldier.discipline) == 0:
                            soldier.fatigue += 1
                        if random.randint(0, soldier.target.discipline) == 0:
                            soldier.target.fatigue += 1

                        if attack > defense:
                            soldier.target.health -= 1
                        elif defense > attack:
                            soldier.health -= 1

                        if soldier.target.health <= 0:
                            self.canvas.delete(soldier.target.id)

                            if soldier.target in current_unit.target.soldiers:
                                current_unit.target.soldiers.remove(soldier.target)

                            soldier.target = None

                            if len(current_unit.target.soldiers) == 0:
                                if current_unit.target in enemy_force:
                                    enemy_force.remove(current_unit.target)

                                    self.canvas.delete(current_unit.target.name_id)

                                current_unit.target = None
                        elif soldier.health <= 0:
                            self.canvas.delete(soldier.id)

                            if soldier.targeted:
                                soldier.targeted.target = None

                            current_unit.soldiers.remove(soldier)

                            if len(current_unit.soldiers) == 0:
                                if current_unit.targeted != None:
                                    current_unit.targeted.target = None

                                force.remove(current_unit)

                                self.canvas.delete(current_unit.name_id)
                    else: #Not in range, so we need to get closer.
                        self.canvas.move(soldier.id, (tx - x) / d * TROOP_MOVEMENT_SPEED, (ty - y) / d * TROOP_MOVEMENT_SPEED)

        return False

    def size(self, force):
        total = 0

        for i in force:
            total += len(i.soldiers)

        return total

    def main_phase(self):
        if self.check_end_battle():
            return True

        self.parent.title("Battle for {}: {}(Reinforcments: {}) vs. {}(Reinforcments: {})".format(self.city.name, self.a.name.short_name(), self.a_army.size(), self.b.name.short_name(), self.b_army.size()))

        self.handle_projectiles(self.a, self.proj_a, self.b, self.force_b)
        self.handle_projectiles(self.b, self.proj_b, self.a, self.force_a)

        self.handle_units(self.force_a, self.a, self.proj_a, self.force_b, self.b, self.a.color)
        if self.over:
            return

        self.handle_units(self.force_b, self.b, self.proj_b, self.force_a, self.a, self.b.color)
        if self.over:
            return

        a_force_size = self.size(self.force_a)
        b_force_size = self.size(self.force_b)

        # print(a_force_size, b_force_size)

        #Add more troops if possible
        if a_force_size < 10 or a_force_size < self.a_amount // 2:
            self.setup_army(self.a_army, self.force_a, self.a.color, (350, 650), (50, 100), max(10, self.a_amount - a_force_size))
        if b_force_size < 10 or b_force_size < self.b_amount // 2:
            self.setup_army(self.b_army, self.force_b, self.b.color, (350, 650), (500, 550), max(10, self.b_amount - b_force_size))

        if self.a_army.size() > 0 and a_force_size == 0:
            self.setup_army(self.a_army, self.force_a, self.a.color, (350, 650), (50, 100), self.a_amount)

        if self.b_army.size() > 0 and b_force_size == 0:
            self.setup_army(self.b_army, self.force_b, self.b.color, (350, 650), (500, 550), self.b_amount)

        for unit in self.force_a + self.force_b:
            if unit.name_id == 0: #It was just created, set it up
                unit.calculate_position()
                unit.ammunition = len(unit.soldiers) * 10
                unit.name_id = self.canvas.create_text(unit.x, unit.y - 20, text=("{} ({}; {}): {}, {}".format(unit.soldier_type.name, ', '.join(map(lambda w: w.name, unit.soldier_type.weapons)), unit.soldier_type.armor.name, unit.soldier_type.strength, unit.soldier_type.health)))

        if not self.over:
            self.after_id = self.parent.after(self.battle_speed.get(), self.main_phase)
