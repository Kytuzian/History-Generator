from Tkinter import *
from time import sleep

import random
import math

import utility

from research import all_ranged_weapons, unarmed

PROJECTILE_MOVEMENT_SPEED = 6
PROJECTILE_RADIUS = 3

TROOP_MOVEMENT_SPEED = 1
TROOP_RADIUS = 5

#How many steps away the target unit should be before switching to melee.
CC_RANGE = 50

#How often on average to check for a new target for the unit
SWITCH_TARGET_COUNT = 8

#The maximum number of troops on either side of the battle
BATTLE_SIZE = 350

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

        self.reforming = True

        self.id = -1
        self.weapon_id = -1

        self.x = 0
        self.y = 0

        self.canvas = canvas

        self.rank_position = None

    def get_melee_weapon(self):
        if self.unit.soldier_type.originally_ranged:
            return self.weapons[1]
        else:
            return self.weapons[0]

    def get_projectile_speed(self):
        weapon = self.get_ranged_weapon()

        if weapon != None:
            return weapon.projectile_speed
        else:
            return 0

    def get_ranged_weapon(self):
        if self.unit.soldier_type.originally_ranged:
            return self.weapons[0]
        else:
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

                    speed = self.unit.get_effective_speed()

                    if d < speed: #If we're almost there, just jump exactly there
                        self.x += dx
                        self.y += dy
                    else:
                        self.x += dx / d * speed
                        self.y += dy / d * speed

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
        d1 = (len(self.unit.ranks) / 2.0 - self.rank) * (TROOP_RADIUS + 1)
        d2 = -self.position * (TROOP_RADIUS + 1)

        # print(self.rank, len(self.unit.ranks[0]), d1, d2)

        t1 = math.atan2(self.unit.dy, self.unit.dx) + math.pi / 2.0
        t2 = t1 - math.pi / 2.0
        self.x = self.unit.x + math.cos(t1) * d1 + math.cos(t2) * d2
        self.y = self.unit.y + math.sin(t1) * d1 + math.sin(t2) * d2

        # print(self.rank, self.position, self.x, self.y, self.unit.x, self.unit.y)

class Projectile:
    def __init__(self, (dx, dy), strength, target, speed):
        self.dx = dx
        self.dy = dy

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

        self.shoot_angle = 0
        self.shoot_time = 0
        self.shoot_position = (0, 0)

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
        for rank in xrange(self.soldier_type.rank_size):
            self.ranks.append([])
            for rank_position in xrange(self.soldier_type.ranks):
                self.ranks[-1].append(RankPosition(self, rank, rank_position, self.canvas))

                if len(self.soldiers) > i:
                    self.ranks[-1][-1].change_soldier(self.soldiers[i])

                    i += 1
                else:
                    return

    def handle_death(self, soldier):
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
        return int(math.log(self.soldier_type.speed, 2)) * TROOP_MOVEMENT_SPEED

    def get_movement_vector(self, vector_format='xy'):
        if self.target != None and not self.soldier_type.ranged:
            d = utility.distance((self.x, self.y), (self.target.x, self.target.y))
            dx = self.target.x - self.x
            dy = self.target.y - self.y

            if vector_format == 'xy':
                return (float(dx) / d * self.get_effective_speed(), float(dy) / d * self.get_effective_speed())
            elif vector_format == 'polar': #Magnitude and angle
                return (self.get_effective_speed(), math.atan2(dy, dx))
        else:
            return (0, 0)

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

    def in_range(self):
        for soldier in self.soldiers:
            if soldier.in_range():
                return True

        return False

    def move(self):
        if self.target != None:
            #We need to calculate these things because we need them for rank positions (facing the enemy, etc.)
            tx, ty = self.target.get_position()
            x, y = self.get_position()

            self.dx, self.dy = tx - x, ty - y

            #If we aren't in range, we need to move closer.
            if not self.in_range():
                d = utility.distance((tx, ty), (x, y))

                if d != 0:
                    speed = self.get_effective_speed()

                    if d < speed:
                        self.x += self.dx
                        self.y += self.dy
                    else:
                        self.x += self.dx / d * speed
                        self.y += self.dy / d * speed

class Battle:
    def __init__(self, nation_a, a_army, nation_b, b_army, attacking_city, city, battle_over):
        self.a = nation_a
        self.b = nation_b

        self.a_army = a_army
        self.b_army = b_army

        self.parent = Tk()
        self.parent.title("{}({}) vs. {}({})".format(self.a.name, self.a_army.size(), self.b.name, self.b_army.size()))
        self.parent.geometry("1000x600+330+0")

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

        self.a_original_size = self.a_army.size()
        self.b_original_size = self.b_army.size()

        self.attacking_city = attacking_city
        self.city = city

        self.create_gui()

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

       # print("Setting up a max of {} soldiers of {} for this unit type.".format(limit, army.number))

        for soldier in xrange(army.number):
            if soldier % (army.ranks * army.rank_size) == 0:
                force.append(Unit(army.zero(), force, [], self.canvas))

                sx, sy = random.randint(xmin, xmax), random.randint(ymin, ymax)

            force[-1].soldiers.append(Soldier(force[-1], army.name, army.health, army.strength, army.ranged, army.weapons, army.armor, army.discipline, self.canvas))

            x,y = sx + len(force[-1].soldiers[:-1]) % army.rank_size * (TROOP_RADIUS + 1), sy + len(force[-1].soldiers[:-1]) / army.rank_size * (TROOP_RADIUS + 1)

            force[-1].soldiers[-1].id = self.canvas.create_oval(x, y, x + TROOP_RADIUS, y + TROOP_RADIUS, fill=color)

            cx, cy = x + TROOP_RADIUS // 2, y + TROOP_RADIUS // 2

            if not force[-1].soldiers[-1].ranged:
                force[-1].soldiers[-1].weapon_id = self.canvas.create_line(cx, cy, cx + 1, cy + force[-1].soldiers[-1].get_melee_weapon().range)

            limit -= 1
            army.number -= 1

            if limit <= 0:
                break

        for unit in force:
            if unit.name_id == 0: #It was just created, set it up
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
                unit.name_id = self.canvas.create_text(unit.x, unit.y, text=("{} ({}; {}): {}, {}".format(unit.soldier_type.name, ', '.join(map(lambda w: w.name, unit.soldier_type.weapons)), unit.soldier_type.armor.name, unit.soldier_type.strength, unit.soldier_type.health)))

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

            self.canvas.move(p.id, p.dx * p.speed, p.dy * p.speed)

            x,y = self.canvas.coords(p.id)[:2]

            try:
                tx,ty = self.canvas.coords(p.target.id)[:2]

                if p.skip_step <= 0:
                    if p.kill_range > 0:
                        p.kill_range -= 1

                        if utility.collided((x, y, p.speed), (tx, ty, TROOP_RADIUS)):
                            hit = True

                            damage = p.strength

                            #Allow the troop being hit by the projectile to try and defend a little.
                            defense = p.target.get_ranged_defense(owner_nation.tech.get_best_in_category('material'))

                            if random.randint(0, p.target.discipline) == 0:
                                p.target.fatigue += 1

                            #Can't do less than 0 damage
                            total_damage = max(damage - defense, 0)

                            p.target.health -= total_damage

                            if p.target.health <= 0:
                                p.target.unit.handle_death(p.target)
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

            #Targeting stuff
            if current_unit.target != None: #if we have a target make sure it still exists
                if not current_unit.target in enemy_force:
                    current_unit.target = None
                elif len(current_unit.target.soldiers) == 0:
                    current_unit.target = None

            #If we don't have a target, target the closest unit.
            if current_unit.target == None or random.randint(0, SWITCH_TARGET_COUNT) == 0:
                current_unit.target = self.get_nearest_enemy(current_unit, enemy_force)

                if current_unit.target != None:
                    current_unit.target.targeted = current_unit
                else:
                    continue

            current_unit.move()
            current_unit.handle_ranks()

            for soldier in current_unit.soldiers:
                #Targeting stuff
                if current_unit.target == None:
                    continue

                if soldier.target != None: #If we have a target, make sure it still exists.
                    if not soldier.target in current_unit.target.soldiers:
                        soldier.target = None

                if len(current_unit.target.soldiers) == 0:
                    break

                if soldier.ranged:
                    soldier.target = random.choice(current_unit.target.soldiers)
                else:
                    soldier.target = self.get_nearest_enemy(soldier, current_unit.target.soldiers)

                if soldier.target != None:
                    soldier.target.targeted = soldier
                else:
                    continue

                x, y = soldier.x, soldier.y
                tx, ty = soldier.target.x, soldier.target.y

                d = utility.distance((x, y), (tx, ty))

                #Show the weapon
                if d != 0 and not soldier.ranged:
                    cx, cy = x + TROOP_RADIUS // 2, y + TROOP_RADIUS // 2
                    weapon_range = soldier.get_melee_weapon().range

                    if soldier.weapon_id == -1:
                        soldier.weapon_id = self.canvas.create_line(cx, cy, cx + 1, cy + soldier.get_melee_weapon().range)
                    else:
                        self.canvas.coords(soldier.weapon_id, cx, cy, cx + (tx - cx) / d * weapon_range, cy + (ty - cy) / d * weapon_range)
                elif soldier.ranged:
                    if soldier.weapon_id != -1:
                        self.canvas.delete(soldier.weapon_id)
                        soldier.weapon_id = -1

                if soldier.ranged:
                    if d < soldier.target.unit.get_effective_speed() * CC_RANGE:
                        soldier.ranged = False

                    soldier.move()
                    if soldier.in_range() and soldier.shoot > soldier.shoot_counter:
                        if current_unit.ammunition > 0:
                            m, tangle = current_unit.target.get_movement_vector(vector_format='polar')

                            if m > 0:
                                t, angle = utility.calculate_interception(m, soldier.get_projectile_speed(), (tx, ty), (x, y), tangle)

                                tx += math.cos(tangle) * t * m
                                ty += math.sin(tangle) * t * m

                                d = utility.distance((x, y), (tx, ty))

                            damage = soldier.get_ranged_attack(nation.tech.get_best_in_category('material'))
                            proj.append(Projectile(((tx - x) / d, (ty - y) / d), damage, soldier.target, soldier.get_projectile_speed()))

                            proj[-1].id = self.canvas.create_oval(x, y, x + PROJECTILE_RADIUS, y + PROJECTILE_RADIUS, width=0, fill=color)
                            proj[-1].skip_step = d // soldier.get_projectile_speed() // 2
                            proj[-1].kill_range = d // soldier.get_projectile_speed() * 2

                            soldier.shoot = 0

                            current_unit.ammunition -= 1
                        else:
                            for s in current_unit.soldiers:
                                s.ranged = False

                            current_unit.soldier_type.ranged = False
                    else:
                        soldier.shoot += math.sqrt(soldier.discipline) / 2 + random.randint(0, 1) * math.log(soldier.discipline)
                else:
                    #If the target moves out of range, then switch back to ranged.
                    if d > soldier.target.unit.get_effective_speed() * CC_RANGE:
                        if current_unit.soldier_type.ranged:
                            soldier.ranged = True

                    if soldier.in_range():
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
                            soldier.target.unit.handle_death(soldier.target)
                        elif soldier.health <= 0:
                            current_unit.handle_death(soldier)
                    else: #Not in range, so we need to get closer.
                        # self.canvas.move(soldier.id, (tx - x) / d * current_unit.get_effective_speed(), (ty - y) / d * current_unit.get_effective_speed())
                        soldier.move()

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

        total = self.a_original_size + self.b_original_size
        current = self.a_army.size() + self.b_army.size() + a_force_size + b_force_size
        utility.show_bar(current, total, message='Soldiers Left: ', number_limit=True)

        if not self.over:
            self.after_id = self.parent.after(self.battle_speed.get(), self.main_phase)
