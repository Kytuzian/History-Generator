from Tkinter import *

import math
import random
import sys
from time import sleep

import utility

from research import all_ranged_weapons, unarmed

PROJECTILE_MOVEMENT_SPEED = 6
PROJECTILE_RADIUS = 3

TROOP_MOVEMENT_SPEED = 1
TROOP_RADIUS = 5
#ADd routing units + equipment slots
#How many steps away the target unit should be before switching to melee.
CC_RANGE = 50

#How often on average to check for a new target for the unit
SWITCH_TARGET_COUNT = 8

#The maximum number of troops on either side of the battle
BATTLE_SIZE = 350


#battle porportions
#troop quality

#Kenny Additions
# 1 unit of ranged from one unit of melee
TROOP_RATIO = 1

class Soldier:
    def __init__(self, unit, name, health, strength, ranged, weapons, armor, discipline, canvas, mount, quality):
        self.unit = unit

        self.name = name
        self.health = health
        self.strength = strength

        self.ranged = ranged

        self.weapons = weapons
        self.armor = armor
        self.mount = mount
        self.quality = quality

        if self.ranged:
            use_weapon = self.get_ranged_weapon()
        else:
            use_weapon = self.get_melee_weapon()

        if use_weapon == None:
            self.reload = 0
            self.reload_counter = 0
        else:
            # print('Reload time: {}'.format(use_weapon.reload_time))
            self.reload = 0
            self.reload_counter = use_weapon.reload_time

        self.discipline = discipline

        self.fatigue = 2

        self.target = None
        self.targeted = None

        self.reforming = True

        self.id = -1
        self.weapon_id = -1

        self.x = 0
        self.y = 0

        self.canvas = canvas

        self.rank_position = None

    def step(self, proj, best_material, best_enemy_material, stats, enemy_stats):
        if self.target != None: #If we have a target, make sure it still exists.
            if not self.target in self.unit.target.soldiers:
                self.target = None

        if self.ranged and self.target == None:
            self.target = random.choice(self.unit.target.soldiers)
        else:
            self.target = utility.get_nearest_enemy(self, self.unit.target.soldiers)

        if self.target != None:
            self.target.targeted = self
        else:
            return

        tx, ty = self.target.x, self.target.y

        d = utility.distance((self.x, self.y), (tx, ty))

        if self.reload < self.reload_counter:
            if not self.ranged or self.in_range(): # Melee units always reload, because their first attack is like a "charge"
                self.reload += self.discipline + random.randint(0,1)

        #Show the weapon if we are currently in melee mode
        if self.canvas:
            if d != 0 and not self.ranged:
                cx, cy = self.x + TROOP_RADIUS // 2, self.y + TROOP_RADIUS // 2
                weapon_range = self.get_melee_weapon().range

                if self.weapon_id == -1:
                    self.weapon_id = self.canvas.create_line(cx, cy, cx, cy + weapon_range)
                else:
                    self.canvas.coords(self.weapon_id, cx, cy, cx + (tx - cx) / d * weapon_range, cy + (ty - cy) / d * weapon_range)
            elif self.ranged:
                if self.weapon_id != -1:
                    self.canvas.delete(self.weapon_id)
                    self.weapon_id = -1

        if self.ranged:
            self.handle_ranged(d, proj, best_material, stats, enemy_stats)
        else:
            self.handle_melee(d, best_material, best_enemy_material, stats, enemy_stats)

    def handle_melee(self, d, best_material, best_enemy_material, stats, enemy_stats):
        #If the target moves out of range, then switch back to ranged.
        if d > self.target.unit.get_effective_speed() * CC_RANGE:
            if self.unit.soldier_type.ranged:
                self.ranged = True
                return

        # print(self.reload, self.reload_counter)

        if self.in_range() and self.reload >= self.reload_counter:
            if not self.name in stats:
                stats[self.name] = utility.base_soldier_stats()
            weapon = self.get_melee_weapon().name
            if not weapon in stats[self.name]:
                stats[self.name][weapon] = utility.base_weapon_stats()

            attack = self.get_melee_attack(best_material)
            defense = self.target.get_melee_defense(best_enemy_material)
            #other_attack = self.get_sidearm_attack(best_material)

            target_is_shield = self.target.weapons[1].shield
            target_is_ranged = self.target.ranged
            target_off_handed = self.target.weapons[0].name != self.target.weapons[1].name
            target_defense_bonus = (target_off_handed) and (not target_is_ranged) and (not target_is_shield)

            armor_pierce = self.get_melee_weapon().armor_pierce
            is_shield = self.weapons[1].shield
            is_heavy = self.target.armor.heavy                     
            is_two_handed = self.weapons[0].name == self.weapons[1].name 

            # if not is_shield and not is_two_handed:
            #     
            #     other_armor_pierce = self.get_switch_weapon().armor_pierce

            #     temp_defense = 0
            #     temp_defense_other = 0

            #     if is_heavy:
            #         if other_armor_pierce:
            #             temp_defense_other = defense/2
            #         else:
            #             temp_defense_other = defense*2
            #         if armor_pierce:
            #             temp_defense = defense/2
            #         else:
            #             temp_defense = defense * 2
            #     else:
            #         if other_armor_pierce:
            #             temp_defense_other = defense*2
            #         else:
            #             temp_defense_other = defense/2
            #         if armor_pierce:
            #             temp_defense = defense*2
            #         else:
            #             temp_defense = defense / 2

                # if (other_attack - temp_defense_other) > (attack - temp_defense):
                #     self.switch_weapons() 

            

            if target_defense_bonus:
               defense = int(defense * 3/2)

            if is_two_handed:
                attack *= 2

            if is_shield:
                attack = int(attack/2)
               # print self.name + " does "+ str(attack) +" damage because of their shield!"

            if is_heavy:
                if armor_pierce == 1:
                    defense /= 2
                #    print self.name + " pierced through " +self.target.name +"'s armor: " + str(defense)
                elif armor_pierce == -1:
                    defense *= 2
                 #   print self.name + " attack glanced off " +self.target.name +"'s armor: " + str(defense)
            else:
                if armor_pierce == 1:
                    defense *= 2
                  #  print self.name + " attack was cushioned by " +self.target.name +"'s armor: " + str(defense)
                elif armor_pierce == -1:
                    defense /= 2
                   # print self.name + " attack sliced through " +self.target.name +"'s armor: " + str(defense)

            if self.target.mount != None:
                attack *= int(self.get_melee_weapon().range/5)

            stats[self.name]['attacks'] += 1
            stats[self.name][weapon]['attacks'] += 1

            if random.randint(0, self.discipline) == 0:
                self.fatigue += 1
            if random.randint(0, self.target.discipline) == 0:
                self.target.fatigue += 1

            if is_heavy:
                print self.target.name + "'s heavy armor is tiring the unit"
                self.target.fatigue *= 2

            if attack > defense:
                stats['attacks_won'] += 1
                stats[self.name]['attacks_won'] += 1
                stats[self.name][weapon]['attacks_won'] += 1

                self.target.health -= 1
            # elif defense > attack and d < self.target.get_melee_weapon().range:
            #     self.health -= 1

            if self.target.health <= 0:
                stats['troops_killed'] += 1
                stats[self.name]['kills'] += 1
                stats[self.name][weapon]['kills'] += 1

                enemy_stats['troops_lost'] += 1

                if not self.target.name in enemy_stats:
                    enemy_stats[self.target.name] = utility.base_soldier_stats()
                enemy_stats[self.target.name]['deaths'] += 1

                self.target.unit.handle_death(self.target)
            elif self.health <= 0:
                stats['troops_lost'] += 1
                stats[self.name]['deaths'] += 1

                enemy_stats['troops_killed'] += 1
                enemy_stats[self.target.name]['kills'] += 1
                enemy_stats[self.target.name][self.target.get_melee_weapon().name]['kills'] += 1

                self.unit.handle_death(self)

            self.reload = 0
        else: #Not in range, so we need to get closer.
            self.move()

    def handle_ranged(self, d, proj, best_material, stats, enemy_stats):
        if d < self.target.unit.get_effective_speed() * CC_RANGE:
            self.ranged = False
            return

        self.move()
        if self.in_range() and self.reload >= self.reload_counter:
            if self.unit.ammunition > 0:
                weapon = self.get_ranged_weapon().name
                if not self.name in stats:
                    stats[self.name] = utility.base_soldier_stats()
                if not weapon in stats[self.name]:
                    stats[self.name][weapon] = utility.base_weapon_stats()

                stats['projectiles_launched'] += 1
                stats[self.name]['projectiles_launched'] += 1
                stats[self.name][weapon]['attacks'] += 1

                m, tangle = self.unit.target.get_movement_vector(vector_format='polar')

                tx, ty = self.target.x, self.target.y

                if m > 0:
                    t, angle = utility.calculate_interception(m, self.get_projectile_speed(), (tx, ty), (self.x, self.y), tangle)

                    tx += math.cos(tangle) * t * m
                    ty += math.sin(tangle) * t * m

                    d = utility.distance((self.x, self.y), (tx, ty))

                damage = self.get_ranged_attack(best_material)
                proj.append(Projectile((self.x, self.y), ((tx - self.x) / d, (ty - self.y) / d), self, damage, self.target, self.get_projectile_speed()))

                if self.canvas:
                    color = self.canvas.itemcget(self.id, 'fill')
                    proj[-1].id = self.canvas.create_oval(self.x, self.y, self.x + 2, self.y + self.get_projectile_size(), width=0, fill=color)

                proj[-1].skip_step = d // self.get_projectile_speed() // 2
                proj[-1].kill_range = d // self.get_projectile_speed() * 2

                self.reload = 0

                self.unit.ammunition -= 1
            else:
                for s in self.unit.soldiers:
                    s.ranged = False

                self.unit.soldier_type.ranged = False

    def get_melee_weapon(self):
        if self.unit.soldier_type.originally_ranged:
            return self.weapons[1]
        else:
            return self.weapons[0]

    def switch_weapons(self):
        temp = self.weapons[0] 
        self.weapons[0] = self.weapons[1]
        self.weapons[1] = temp

    def get_switch_weapon(self):
        if self.get_melee_weapon() == self.weapons[0]:
            return self.weapons[1]
        else:
            return self.weapons[0]

    def get_projectile_speed(self):
        weapon = self.get_ranged_weapon()

        if weapon != None:
            return weapon.projectile_speed
        else:
            return 0

    def get_projectile_size(self):
        weapon = self.get_ranged_weapon()

        if weapon != None:
            return weapon.projectile_size
        else:
            return 0

    def get_ranged_weapon(self):
        if self.unit.soldier_type.originally_ranged:
            return self.weapons[0]
        else:
            return None

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

    def get_sidearm_attack(self, material):
        other_weapon = self.get_switch_weapons()

        if other_weapon == None: #This could happen if ALL of our weapons have broken.
            other_weapon = unarmed()

        other_weapon_attack = other_weapon.get_attack(material)
        other_normal_attack = other_weapon.attack_skill_multiplier * random.randint(0, self.strength)
        other_result = other_weapon_attack + other_normal_attack - fatigue_loss

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
        
        if self.mount != None:
            result += int((self.mount.attack + self.mount.attack_skill_multiplier * random.randint(0, self.strength)) * (1/4))

        # print('{} from weapon ({}), {} from strength, {} lost from fatigue = {}'.format(weapon_attack, use_weapon.name, normal_attack, fatigue_loss, result))

        if result > 0:
            return result
        else:
            return random.randint(0, 1)

    def get_ranged_defense(self, material):
        fatigue_loss = random.randint(0, self.fatigue // 2)
        armor_defense = self.armor.get_defense(material)
        skill_defense = self.armor.defense_skill_multiplier * random.randint(0, self.strength)
        is_shield = self.weapons[1].shield

        if self.mount != None:
            mount_defense = int(self.mount.defense * (1/4))

            if self.mount.heavy:
                mount_defense *= 2
                fatigue_loss *= 2

            armor_defense += mount_defense

            mount_defense_skill = int(self.mount.defense_skill_multiplier * random.randint(0, self.strength) * (1/4))

            skill_defense += mount_defense_skill



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

    def in_range(self):
        if self.target != None:
            tx, ty = self.target.x, self.target.y

            d = utility.distance((tx, ty), (self.x, self.y))

            if self.ranged:
                return d <= self.get_ranged_weapon().range
            else:
                return d <= self.get_melee_weapon().range
        else:
            return False

    def move(self):
        if self.rank_position != None:
            self.rank_position.calculate_position()

            tx, ty = self.rank_position.x, self.rank_position.y

            if not utility.rough_match(self.x, tx, 0.5) or not utility.rough_match(self.y, ty, 0.5):
                if self.reforming:
                    self.x = tx
                    self.y = ty

                    self.reforming = False
                else:
                    dx, dy = tx - self.x, ty - self.y
                    d = utility.distance((tx, ty), (self.x, self.y))

                    speed = self.unit.get_effective_speed() + 0.5

                    if d < speed: #If we're almost there, just jump exactly there
                        self.x += dx
                        self.y += dy
                    else:
                        self.x += dx / d * speed
                        self.y += dy / d * speed

                if self.canvas:
                    self.canvas.coords(self.id, self.x, self.y, self.x + TROOP_RADIUS, self.y + TROOP_RADIUS)

class RankPosition:
    def __init__(self, unit, rank, position, canvas):
        self.unit = unit
        self.rank = rank
        self.position = position

        self.canvas = canvas

        self.x, self.y = 0, 0

        self.soldier = None

    def change_soldier(self, soldier):
        if soldier.rank_position != None:
            soldier.rank_position.soldier = None

        soldier.rank_position = self
        self.soldier = soldier

    def has_soldier(self):
        return self.soldier != None

    def calculate_position(self):
        d1 = ((len(self.unit.ranks[0]) - 1) / 2.0 - self.position) * (TROOP_RADIUS + 1)
        d2 = -self.rank * (TROOP_RADIUS + 1)

        t1 = math.atan2(self.unit.dy, self.unit.dx) + math.pi / 2.0
        t2 = t1 - math.pi / 2.0
        self.x = self.unit.x + math.cos(t1) * d1 + math.cos(t2) * d2
        self.y = self.unit.y + math.sin(t1) * d1 + math.sin(t2) * d2

class Projectile:
    def __init__(self, (x, y), (dx, dy), launcher, strength, target, speed):
        self.x = x
        self.y = y

        self.dx = dx
        self.dy = dy

        self.launcher = launcher

        self.skip_step = 0
        self.kill_range = 1000

        self.strength = strength / 2

        if self.strength <= 0:
            self.strength = 1

        self.id = -1

        self.target = target

        self.speed = speed

class Unit:
    def __init__(self, soldier_type, force, soldiers, canvas):
        self.soldier_type = soldier_type

        self.force = force

        self.soldiers = soldiers
        self.ranks = []

        self.target = None
        self.targeted = None

        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0

        self.name_id = 0

        self.canvas = canvas

    def setup_ammunition(self):
        use_weapon = None
        for weapon in self.soldier_type.weapons:
            if weapon.name in map(lambda w: w.name, all_ranged_weapons):
                use_weapon = weapon

        if use_weapon == None:
            self.ammunition = 0
        else:
            self.ammunition = use_weapon.ammunition * len(self.soldiers)

    def setup_ranks(self):
        self.ranks = []

        i = 0
        for rank in xrange(self.soldier_type.ranks):
            self.ranks.append([])
            for rank_position in xrange(self.soldier_type.rank_size):
                self.ranks[-1].append(RankPosition(self, rank, rank_position, self.canvas))

                if len(self.soldiers) > i:
                    self.ranks[-1][-1].change_soldier(self.soldiers[i])

                    i += 1
                else:
                    return

    def handle_death(self, soldier):
        if self.canvas:
            self.canvas.delete(soldier.id)
            self.canvas.delete(soldier.weapon_id)

        if soldier.targeted != None:
            soldier.targeted.target = None

        self.soldiers.remove(soldier)

        if soldier.rank_position:
            soldier.rank_position.soldier = None

        if len(self.soldiers) == 0:
            if self.targeted != None:
                self.targeted.target = None

            self.force.remove(self)

            if self.canvas:
                self.canvas.delete(self.name_id)

    def handle_ranks(self):
        #Fill up earlier positions in the formation
        for rank_i, rank in enumerate(self.ranks):
            for position_i, position in enumerate(rank):
                if not position.has_soldier():
                    next_soldier = self.get_next_soldier(rank_i, position_i)

                    if next_soldier != None:
                        position.change_soldier(self.get_next_soldier(rank_i, position_i))

        #clear out empty ranks
        for rank_i, rank in enumerate(self.ranks):
            for position_i, position in enumerate(rank):
                if not position.has_soldier(): #Remove the rest of this, because there are no soldiers after this
                    self.ranks[rank_i] = rank[:position_i]
                    self.ranks = self.ranks[:rank_i + 1] #We don't need any of the rest of the ranks either
                    return

    def get_next_soldier(self, ri, pi):
        for rank_i, rank in enumerate(self.ranks):
            if rank_i >= ri:
                for position_i, position in enumerate(rank):
                    if rank_i == ri:
                        if position_i > pi:
                            if position.has_soldier():
                                return position.soldier
                    else:
                        if position.has_soldier():
                            return position.soldier

    def get_effective_speed(self):
        mount_speed = 0

        if self.soldier_type.mount != None:
            mount_speed = self.soldier_type.mount.speed

        return int(math.log(self.soldier_type.speed, 2)) * (TROOP_MOVEMENT_SPEED + mount_speed)
 
    def get_movement_vector(self, vector_format='xy'):
        if self.target != None and not self.soldier_type.ranged:
            if not self.in_range():
                d = utility.distance((self.x, self.y), (self.target.x, self.target.y))
                dx = self.target.x - self.x
                dy = self.target.y - self.y

                if vector_format == 'xy':
                    return (float(dx) / d * self.get_effective_speed(), float(dy) / d * self.get_effective_speed())
                elif vector_format == 'polar': #Magnitude and angle
                    return (self.get_effective_speed(), math.atan2(dy, dx))
            else:
                return (0, 0)
        else:
            return (0, 0)

    def get_position(self):
        return (self.x, self.y)

    def calculate_position(self):
        total_x = 0
        total_y = 0

        for soldier in self.soldiers:
            total_x += soldier.x
            total_y += soldier.y

        if len(self.soldiers) > 0:
            self.x = total_x // len(self.soldiers)
            self.y = total_y // len(self.soldiers)

        return (self.x, self.y)

    def in_range(self):
        for soldier in self.soldiers:
            if soldier.in_range():
                return True

        return False

    def move(self):
        if self.target != None:
            tx, ty = self.target.get_position()
            self.dx, self.dy = tx - self.x, ty - self.y

            # print(self.x, self.y)
            #If we aren't in range, we need to move closer.
            if not self.in_range():
                d = utility.distance((tx, ty), (self.x, self.y))

                if d != 0:
                    speed = self.get_effective_speed()

                    if d < speed:
                        self.x += self.dx
                        self.y += self.dy
                    else:
                        self.x += self.dx / d * speed
                        self.y += self.dy / d * speed
                    # print(self.dx, self.dy, d, self.x, self.y)

class Battle:
    def __init__(self, nation_a, a_army, nation_b, b_army, attacking_city, city, battle_over, use_graphics=True, fast_battles=False):
        self.a = nation_a
        self.b = nation_b

        self.a_army = a_army
        self.b_army = b_army

        self.a_stats = utility.base_stats()
        self.b_stats = utility.base_stats()

        self.a_stats['troops'] = a_army.size()
        self.b_stats['troops'] = b_army.size()
        self.delay = 1

        self.force_a = []
        self.force_b = []

        self.proj_a = []
        self.proj_b = []

        self.battle_over = battle_over
        self.over = False

        self.a_amount = 0
        self.b_amount = 0

        self.a_original_size = self.a_army.size()
        self.b_original_size = self.b_army.size()

        self.attacking_city = attacking_city
        self.city = city
        
        self.fast_battles = fast_battles
        if self.fast_battles:
            self.use_graphics = False
        else:
            self.use_graphics = use_graphics
            if use_graphics:
                self.parent = Tk()
                self.parent.title("{}({}) vs. {}({})".format(self.a.name, self.a_army.size(), self.b.name, self.b_army.size()))
                self.parent.geometry("1000x600+330+0")

                if utility.START_BATTLES_MINIMIZED:
                    self.parent.wm_state('iconic')

                self.canvas = Canvas(self.parent, width=1000, height=600)
                self.canvas.pack()

                self.create_gui()
            else:
                self.parent = None
                self.canvas = None

    def create_gui(self):
        self.battle_speed = Scale(self.parent, from_=1, to=200, orient=HORIZONTAL)
        self.battle_speed.set(30)
        self.battle_speed.pack()
        self.battle_speed.place(x=10, y=30)

        self.battle_speed_label = Label(self.parent, text='Battle Speed (ms):')
        self.battle_speed_label.pack()
        self.battle_speed_label.place(x=10, y = 10)

    def setup_army(self, army, force, color, (xmin, xmax), (ymin, ymax), limit):
        sx, sy = 0, 0

        #print("Setting up a max of {} soldiers of {} for this unit type.".format(limit, army.number))

        new_units = []
        for soldier in xrange(army.number):
            if soldier % (army.ranks * army.rank_size) == 0:
                force.append(Unit(army.zero(), force, [], self.canvas))
                new_units.append(force[-1])

                sx, sy = random.randint(xmin, xmax), random.randint(ymin, ymax)

            force[-1].soldiers.append(Soldier(force[-1], army.name, army.health, army.strength, army.ranged, army.weapons, army.armor, army.discipline, self.canvas, army.mount, army.quality))

            x,y = sx + len(force[-1].soldiers[:-1]) % army.rank_size * (TROOP_RADIUS + 1), sy + len(force[-1].soldiers[:-1]) / army.rank_size * (TROOP_RADIUS + 1)

            force[-1].soldiers[-1].x = x
            force[-1].soldiers[-1].y = y
            if self.use_graphics:
                force[-1].soldiers[-1].id = self.canvas.create_oval(x, y, x + TROOP_RADIUS, y + TROOP_RADIUS, fill=color)

                cx, cy = x + TROOP_RADIUS // 2, y + TROOP_RADIUS // 2

                if not force[-1].soldiers[-1].ranged:
                    force[-1].soldiers[-1].weapon_id = self.canvas.create_line(cx, cy, cx + 1, cy + force[-1].soldiers[-1].get_melee_weapon().range)

            limit -= 1
            army.number -= 1

            if limit <= 0:
                break

        for unit in new_units:
            #So they start out facing the right direction
            if army == self.a_army:
                unit.dy = -1
                unit.dx = 0
            elif army == self.b_army:
                unit.dy = 1
                unit.dx = 0

            unit.calculate_position()
            for soldier in unit.soldiers:
                soldier.move()

            unit.setup_ranks()
            unit.setup_ammunition()
            if self.use_graphics:
                #print unit.soldier_type.name+" "+str(unit.soldier_type.quality)
                if unit.soldier_type.mount.name == 'None':
                    unit.name_id = self.canvas.create_text(unit.x, unit.y, text=("{} ({}; {}): {}, {}".format(unit.soldier_type.name, ', '.join(map(lambda w: w.name, unit.soldier_type.weapons)), unit.soldier_type.armor.name, unit.soldier_type.strength, unit.soldier_type.health)))
                else:
                    unit.name_id = self.canvas.create_text(unit.x, unit.y, text=("{} ({}; {}): {}, {}, {}".format(unit.soldier_type.name, ', '.join(map(lambda w: w.name, unit.soldier_type.weapons)), unit.soldier_type.armor.name, unit.soldier_type.strength, unit.soldier_type.health, unit.soldier_type.mount.name)))

        if limit <= 0:
            return

        if len(army.upgrades) > 0:
            for i in army.upgrades:
                self.setup_army(i, force, color, (xmin, xmax), (ymin, ymax), limit)

    def setup_soldiers(self):
        if self.fast_battles:
            return
        else:
            if self.a_army.size() > self.b_army.size():
                self.a_amount = BATTLE_SIZE
                self.b_amount = int(BATTLE_SIZE * (float(self.b_army.size() + 1) / float(self.a_army.size() + 1)))
            else:
                self.a_amount = int(BATTLE_SIZE * (float(self.a_army.size() + 1) / float(self.b_army.size() + 1)))
                self.b_amount = BATTLE_SIZE

            self.setup_army(self.a_army, self.force_a, self.a.color, (100, 900), (50, 300), self.a_amount)
            self.setup_army(self.b_army, self.force_b, self.b.color, (100, 900), (300, 550), self.b_amount)

    def handle_projectiles(self, owner_nation, proj, enemy, enemy_force, stats, enemy_stats):
        i = 0
        for p in proj:
            hit = False

            if self.use_graphics:
                self.canvas.move(p.id, p.dx * p.speed, p.dy * p.speed)

            p.x += p.dx * p.speed
            p.y += p.dy * p.speed

            x, y = p.x, p.y
            try:
                tx, ty = p.target.x, p.target.y

                if p.skip_step <= 0:
                    if p.kill_range > 0:
                        p.kill_range -= 1

                        if utility.collided((x, y, p.speed), (tx, ty, TROOP_RADIUS)):
                            hit = True

                            stats['projectiles_hit'] += 1
                            weapon = p.launcher.get_ranged_weapon().name
                            if not p.launcher.name in stats:
                                stats[p.launcher.name] = utility.base_soldier_stats()
                            if not weapon in stats[p.launcher.name]:
                                stats[p.launcher.name][weapon] = utility.base_weapon_stats()
                            stats[p.launcher.name]['projectiles_hit'] += 1
                            stats[p.launcher.name][weapon]['attacks_won'] += 1

                            damage = p.strength

                            #Allow the troop being hit by the projectile to try and defend a little.
                            defense = p.target.get_ranged_defense(owner_nation.tech.get_best_in_category('material'))
                            is_shield = p.target.weapons[1].shield 
                            armor_pierce = p.launcher.get_ranged_weapon().armor_pierce
                            siege_weapon = p.launcher.get_ranged_weapon().siege_weapon
                            is_heavy = p.target.armor.heavy                     

                            if is_shield:
                                damage = int(damage/2)
                               # print p.launcher.name + "'s ranged attack was deflected by "+p.target.name+"'s shield: "+str(damage)
                            elif not is_heavy:
                                damage *= 2
                                #print p.launcher.name + "'s ranged attack was left unprotected by "+p.target.name+"'s lack of a shield: "+str(damage)

                            if is_heavy:
                                if armor_pierce == 1:
                                    defense /= 2
                                 #   print p.launcher.name + "'s ranged attack pierced  "+p.target.name+"'s heavy armor:  "+str(damage)
                                elif armor_pierce == -1:
                                    defense *= 2
                                  #  print p.launcher.name + "'s ranged attack glanced off of "+p.target.name+"'s hevy armor: "+str(damage)
                            else:
                                if armor_pierce == 1:
                                    defense *= 2
                                   # print p.launcher.name + "'s ranged attack was cushioned by "+p.target.name+"'s light armor: "+str(damage)
                                elif armor_pierce == -1:
                                    defense /= 2
                                    #print p.launcher.name + "'s ranged attack impacted "+p.target.name+"'s light armor: "+str(damage)

                            if random.randint(0, p.target.discipline) == 0:
                                p.target.fatigue += 1

                            #Can't do less than 0 damage
                            total_damage = max(damage - defense, 0)

                            original_health = p.target.health

                            p.target.health -= total_damage

                            if p.target.health <= 0:
                                overkill = 1
                                if siege_weapon:
                                    overkill += p.target.health*-1/original_health
                                stats['troops_killed'] += overkill
                                stats[p.launcher.name]['kills'] += overkill
                                stats[p.launcher.name][weapon]['kills'] += overkill

                                if not p.target.name in enemy_stats:
                                    enemy_stats[p.target.name] = utility.base_soldier_stats()
                                enemy_stats[p.target.name]['deaths'] += overkill
                                enemy_stats['troops_lost'] += overkill
                                p.target.unit.handle_death(p.target)

                                num = 1
                                while(num < overkill):
                                    if num < len(p.target.soldiers):
                                        p.target.unit.handle_death(p.target.soldiers[num])
                                    num += 1
                else:
                    p.skip_step -= 1

                if hit or x < 0 or x > 1000 or y < 0 or y > 600:
                    if self.use_graphics:
                        self.canvas.delete(p.id)

                    proj.remove(p)
            except: #Remove this if we don't have a target
                if self.use_graphics:
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

            if self.use_graphics:
                self.parent.destroy()

            self.over = True
            self.battle_over(self)

            return True
        else:
            return False

    def handle_units(self, force, nation, proj, enemy_force, enemy_nation, color, stats, enemy_stats):
        best_material = nation.tech.get_best_in_category('material')
        best_enemy_material = enemy_nation.tech.get_best_in_category('material')
        for current_unit in force:
            if self.check_end_battle():
                return True

            if len(current_unit.soldiers) == 0: #No soldiers, remove this and untarget
                if current_unit.targeted != None:
                    current_unit.targeted.target = None

                force.remove(current_unit)

                continue

            if self.use_graphics:
                self.canvas.coords(current_unit.name_id, current_unit.x, current_unit.y - 20)

            #Targeting stuff
            if current_unit.target != None: #if we have a target make sure it still exists
                if not current_unit.target in enemy_force:
                    current_unit.target = None
                elif len(current_unit.target.soldiers) == 0:
                    current_unit.target = None

            #If we don't have a target, target the closest unit.
            if current_unit.target == None or random.randint(0, SWITCH_TARGET_COUNT) == 0:
                current_unit.target = utility.get_nearest_enemy(current_unit, enemy_force)

                if current_unit.target != None:
                    current_unit.target.targeted = current_unit
                else:
                    continue

            current_unit.move()
            current_unit.handle_ranks()

            for soldier in current_unit.soldiers:
                #Targeting stuff
                if current_unit.target == None:
                    break
                if len(current_unit.target.soldiers) == 0:
                    break

                soldier.step(proj, best_material, best_enemy_material, stats, enemy_stats)

        return False

    def size(self, force):
        total = 0

        for i in force:
            total += len(i.soldiers)

        return total
    
    def main_phase(self):
        if self.fast_battles:
            self.fast_battle_main()
        else:
            self.standard_battle_main()

    def fast_battle_main(self):
        def get_next_soldier(army):
            for troop in army.make_upgrade_list():
                if troop.number > 0:
                    return troop

            return None

        def get_ranged_damage(troop, material):
            use_weapon = troop.weapons[0]
            weapon_attack = use_weapon.get_attack(material)
            normal_attack = use_weapon.attack_skill_multiplier * random.randint(0, troop.strength)

            result = weapon_attack + normal_attack

            if result > 0:
                return result
            else:
                return random.randint(0, 1)
        
        def get_melee_attack(troop, material):
            if troop.ranged:
                use_weapon = troop.weapons[1]
            else:
                use_weapon = troop.weapons[0]

            weapon_attack = use_weapon.get_attack(material)
            normal_attack = use_weapon.attack_skill_multiplier * random.randint(0, troop.strength)

            result = weapon_attack + normal_attack

            if result > 0:
                return result
            else:
                return random.randint(0, 1)

        def get_ranged_defense(troop, material):
            armor_defense = troop.armor.get_defense(material)
            skill_defense = troop.armor.defense_skill_multiplier * random.randint(0, troop.strength)

            return max(0, armor_defense + skill_defense)

        def get_melee_defense(troop, material):
            if troop.ranged:
                use_weapon = troop.weapons[1]
            else:
                use_weapon = troop.weapons[0]

            weapon_defense = use_weapon.get_defense(material)
            armor_defense = troop.armor.get_defense(material)
            normal_defense = troop.armor.defense_skill_multiplier * use_weapon.defense_skill_multiplier * random.randint(0, troop.strength)

            result = weapon_defense + armor_defense + normal_defense

            if result > 0:
                return result
            else:
                return random.randint(0, 1)

        a_material = self.a.tech.get_best_in_category('material')
        b_material = self.b.tech.get_best_in_category('material')

        while self.a_army.size() > 0 and self.b_army.size() > 0:
            a_unit = get_next_soldier(self.a_army)
            b_unit = get_next_soldier(self.b_army)

            a_health = a_unit.health
            b_health = b_unit.health

            if not a_unit.name in self.a_stats:
                self.a_stats[a_unit.name] = utility.base_soldier_stats()
                self.a_stats[a_unit.name][a_unit.weapons[0].name] = utility.base_weapon_stats()
                self.a_stats[a_unit.name][a_unit.weapons[1].name] = utility.base_weapon_stats()

            if not b_unit.name in self.b_stats:
                self.b_stats[b_unit.name] = utility.base_soldier_stats()
                self.b_stats[b_unit.name][b_unit.weapons[0].name] = utility.base_weapon_stats()
                self.b_stats[b_unit.name][b_unit.weapons[1].name] = utility.base_weapon_stats()
            
            sys.stdout.write("\rBattle for {}: {}(Soldiers: {}) vs. {}(Soldiers: {})".format(self.city.name, self.a.name.short_name(), self.a_army.size(), self.b.name.short_name(), self.b_army.size()))
            sys.stdout.flush()

            if a_unit == None or b_unit == None:
                raise Exception('Couldn\'t find any units!')

            if a_unit.ranged:
                damage = get_ranged_damage(a_unit, a_material)
                defense = get_ranged_defense(b_unit, b_material)
                
                self.a_stats['projectiles_launched'] += 1
                self.a_stats[a_unit.name]['projectiles_launched'] += 1
                self.a_stats[a_unit.name][a_unit.weapons[0].name]['attacks'] += 1

                if defense < damage:
                    b_health -= damage - defense
                    
                    self.a_stats['projectiles_hit'] += 1
                    self.a_stats[a_unit.name]['projectiles_hit'] += 1
                    self.a_stats[a_unit.name][a_unit.weapons[0].name]['attacks_won'] += 1

                    if b_health <= 0:
                        self.a_stats[a_unit.name][a_unit.weapons[0].name]['kills'] += 1

            if b_unit.ranged:
                damage = get_ranged_damage(b_unit, b_material)
                defense = get_ranged_defense(a_unit, a_material)
                
                self.b_stats['projectiles_launched'] += 1
                self.b_stats[b_unit.name]['projectiles_launched'] += 1
                self.b_stats[b_unit.name][b_unit.weapons[0].name]['attacks'] += 1

                if defense < damage:
                    a_health -= damage - defense
                    
                    self.b_stats['projectiles_hit'] += 1
                    self.b_stats[b_unit.name]['projectiles_hit'] += 1
                    self.b_stats[b_unit.name][b_unit.weapons[0].name]['attacks_won'] += 1

                    if a_health <= 0:
                        self.b_stats[b_unit.name][b_unit.weapons[0].name]['kills'] += 1

            while a_health > 0 and b_health > 0:
                a_attack = get_melee_attack(a_unit, a_material)
                b_defense = get_melee_defense(b_unit, b_material)                
                self.a_stats[a_unit.name]['attacks'] += 1
                if a_unit.ranged:
                    a_melee = a_unit.weapons[1]
                else:
                    a_melee = a_unit.weapons[0]
                self.a_stats[a_unit.name][a_melee.name]['attacks'] += 1

                if a_attack > b_defense:
                    self.a_stats[a_unit.name]['attacks_won'] += 1
                    self.a_stats['attacks_won'] += 1
                    self.a_stats[a_unit.name][a_melee.name]['attacks_won'] += 1
                    
                    b_health -= 1

                    if b_health <= 0:
                        self.a_stats[a_unit.name][a_melee.name]['kills'] += 1
                        break

                b_attack = get_melee_attack(b_unit, b_material)
                a_defense = get_melee_defense(a_unit, a_material)
                self.b_stats[b_unit.name]['attacks'] += 1

                if b_unit.ranged:
                    b_melee = b_unit.weapons[1]
                else:
                    b_melee = b_unit.weapons[0]

                self.b_stats[b_unit.name][b_melee.name]['attacks'] += 1

                if b_attack > a_defense:
                    self.b_stats[b_unit.name]['attacks_won'] += 1
                    self.b_stats['attacks_won'] += 1
                    self.b_stats[b_unit.name][b_melee.name]['attacks_won'] += 1
                
                    a_health -= 1

                    if a_health <= 0:
                        self.b_stats[b_unit.name][b_melee.name]['kills'] += 1
                        break

            if a_health <= 0:
                a_unit.number -= 1

                self.a_stats['troops_lost'] += 1
                self.b_stats['troops_killed'] += 1
                self.a_stats[a_unit.name]['deaths'] += 1
                self.b_stats[b_unit.name]['kills'] += 1
            elif b_health <= 0:
                b_unit.number -= 1

                self.b_stats['troops_lost'] += 1
                self.a_stats['troops_killed'] += 1
                self.b_stats[b_unit.name]['deaths'] += 1
                self.a_stats[a_unit.name]['kills'] += 1

        self.battle_over(self)

    def standard_battle_main(self):
        while not self.check_end_battle():
            self.handle_projectiles(self.a, self.proj_a, self.b, self.force_b, self.a_stats, self.b_stats)
            self.handle_projectiles(self.b, self.proj_b, self.a, self.force_a, self.b_stats, self.a_stats)

            self.handle_units(self.force_a, self.a, self.proj_a, self.force_b, self.b, self.a.color, self.a_stats, self.b_stats)
            if self.over:
                return

            self.handle_units(self.force_b, self.b, self.proj_b, self.force_a, self.a, self.b.color, self.b_stats, self.a_stats)
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

            a_cur = self.a_army.size() + a_force_size
            b_cur = self.b_army.size() + b_force_size

            sys.stdout.write("\rBattle of {}: {}(Soldiers: {}) vs. {}(Soldiers: {})".format(self.city.name, self.a.name.short_name(), a_cur, self.b.name.short_name(), b_cur))
            sys.stdout.flush()

            if not self.over:
                if self.use_graphics:
                    self.parent.title("Battle of {}: {}(Reinforcements: {}) vs. {}(Reinforcements: {})".format(self.city.name, self.a.name.short_name(), self.a_army.size(), self.b.name.short_name(), self.b_army.size()))

                    self.after_id = self.parent.after(self.battle_speed.get(), self.main_phase)

                    break
