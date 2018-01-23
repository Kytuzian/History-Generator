import math
import random

from internal import utility as utility
from military.battle import TROOP_RADIUS, CC_RANGE
from military.projectile import Projectile
from research.equipment_list import unarmed


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

        if use_weapon is None:
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
        if self.target is not None: #If we have a target, make sure it still exists.
            if not self.target in self.unit.target.soldiers:
                self.target = None

        if self.ranged and self.target is None:
            self.target = random.choice(self.unit.target.soldiers)
        else:
            self.target = utility.get_nearest_enemy(self, self.unit.target.soldiers)

        if self.target is not None:
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

        if self.in_range() and self.reload >= self.reload_counter:
            if not self.name in stats:
                stats[self.name] = utility.base_soldier_stats()
            weapon = self.get_melee_weapon().name
            if not weapon in stats[self.name]:
                stats[self.name][weapon] = utility.base_weapon_stats()

            attack = self.get_melee_attack(best_material)
            defense = self.target.get_melee_defense(best_enemy_material)

            target_is_shield = self.target.weapons[1].shield
            target_is_ranged = self.target.ranged
            target_off_handed = self.target.weapons[0].name != self.target.weapons[1].name
            target_defense_bonus = (target_off_handed) and (not target_is_ranged) and (not target_is_shield)

            armor_pierce = self.get_melee_weapon().armor_pierce

            # TODO: Add a graphical indication that a unit has a shield.
            is_shield = self.weapons[1].shield
            is_heavy = self.target.armor.heavy
            is_two_handed = self.weapons[0].name == self.weapons[1].name

            if target_defense_bonus:
               defense = int((defense * 3/2) * self.target.weapons[1].defense_skill_multiplier)

            if is_two_handed:
                attack *= 2

            if is_shield:
                attack = int(attack/2)

            if is_heavy:
                if armor_pierce == 1:
                    defense /= 2
                elif armor_pierce == -1:
                    defense *= 2
            else:
                if armor_pierce == 1:
                    defense *= 2
                elif armor_pierce == -1:
                    defense /= 2

            if self.target.mount is not None:
                attack *= int(self.get_melee_weapon().range/5)

            stats[self.name]['attacks'] += 1
            stats[self.name][weapon]['attacks'] += 1

            if random.randint(0, self.discipline) == 0:
                self.fatigue += 1
            if random.randint(0, self.target.discipline) == 0:
                self.target.fatigue += 1

            # Heavy armor makes the unit more tired.
            if is_heavy:
                self.target.fatigue *= 2

            if attack > defense:
                stats['attacks_won'] += 1
                stats[self.name]['attacks_won'] += 1
                stats[self.name][weapon]['attacks_won'] += 1

                self.target.health -= 1

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
                    proj[-1].id = self.canvas.create_oval(self.x, self.y, self.x + self.get_projectile_size(), self.y + self.get_projectile_size(), width=0, fill=color)

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
        self.weapons[0], self.weapons[1] = self.weapons[1], self.weapons[0]

    def get_switch_weapon(self):
        if self.get_melee_weapon() == self.weapons[0]:
            return self.weapons[1]
        else:
            return self.weapons[0]

    def get_projectile_speed(self):
        weapon = self.get_ranged_weapon()

        if weapon is not None:
            return weapon.projectile_speed
        else:
            return 0

    def get_projectile_size(self):
        weapon = self.get_ranged_weapon()

        if weapon is not None:
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

        if use_weapon is None: #Shouldn't actually happen, but just in case.
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
        fatigue_loss = random.randint(0, self.fatigue // 2)
        other_weapon = self.get_switch_weapon()

        if other_weapon is None: #This could happen if ALL of our weapons have broken.
            other_weapon = unarmed()

        other_weapon_attack = other_weapon.get_attack(material)
        other_normal_attack = other_weapon.attack_skill_multiplier * random.randint(0, self.strength)
        result = other_weapon_attack + other_normal_attack - fatigue_loss

        if result > 0:
            return result
        else:
            return random.randint(0, 1)

    def get_melee_attack(self, material):
        fatigue_loss = random.randint(0, self.fatigue // 2)

        #Find our melee weapon
        use_weapon = self.get_melee_weapon()

        if use_weapon is None: #This could happen if ALL of our weapons have broken.
            use_weapon = unarmed()


        weapon_attack = use_weapon.get_attack(material)


        normal_attack = use_weapon.attack_skill_multiplier * random.randint(0, self.strength)



        result = weapon_attack + normal_attack - fatigue_loss

        if self.mount is not None:
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

        if self.mount is not None:
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

        if use_weapon is None: #This could happen if ALL of our weapons have broken.
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
        if self.target is not None:
            tx, ty = self.target.x, self.target.y

            d = utility.distance((tx, ty), (self.x, self.y))

            if self.ranged:
                return d <= self.get_ranged_weapon().range
            else:
                return d <= self.get_melee_weapon().range
        else:
            return False

    def move(self):
        if self.rank_position is not None:
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