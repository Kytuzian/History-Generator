from Tkinter import *

import random
import sys

import internal.utility as utility

from military.soldier import Soldier, TROOP_RADIUS
from military.unit import Unit

PROJECTILE_MOVEMENT_SPEED = 6
PROJECTILE_RADIUS = 3

# How often on average to check for a new target for the unit
SWITCH_TARGET_COUNT = 8

# The maximum number of troops on either side of the battle
BATTLE_SIZE = 350

# 1 unit of ranged from one unit of melee
TROOP_RATIO = 1


class Battle:
    def __init__(self, nation_a, a_army, nation_b, b_army, attacking_city, city, battle_over, use_graphics=True,
                 fast_battles=False):
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
                self.parent.title(
                    "{}({}) vs. {}({})".format(self.a.name, self.a_army.size(), self.b.name, self.b_army.size()))
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
        self.battle_speed_label.place(x=10, y=10)

    def setup_army(self, army, force, color, (xmin, xmax), (ymin, ymax), limit):
        sx, sy = 0, 0

        # print("Setting up a max of {} soldiers of {} for this unit type.".format(limit, army.number))

        new_units = []
        for soldier in xrange(army.number):
            if soldier % (army.ranks * army.rank_size) == 0:
                force.append(Unit(army.zero(), force, [], self.canvas))
                new_units.append(force[-1])

                sx, sy = random.randint(xmin, xmax), random.randint(ymin, ymax)

            force[-1].soldiers.append(
                Soldier(force[-1], army.name, army.health, army.strength, army.ranged, army.weapons, army.armor,
                        army.discipline, self.canvas, army.mount, army.quality))

            x, y = sx + len(force[-1].soldiers[:-1]) % army.rank_size * (TROOP_RADIUS + 1), sy + len(
                force[-1].soldiers[:-1]) / army.rank_size * (TROOP_RADIUS + 1)

            force[-1].soldiers[-1].x = x
            force[-1].soldiers[-1].y = y
            if self.use_graphics:
                force[-1].soldiers[-1].id = self.canvas.create_oval(x, y, x + TROOP_RADIUS, y + TROOP_RADIUS,
                                                                    fill=color)

                cx, cy = x + TROOP_RADIUS // 2, y + TROOP_RADIUS // 2

                if not force[-1].soldiers[-1].ranged:
                    force[-1].soldiers[-1].weapon_id = self.canvas.create_line(cx, cy, cx + 1, cy + force[-1].soldiers[
                        -1].get_melee_weapon().range)

            limit -= 1
            army.number -= 1

            if limit <= 0:
                break

        for unit in new_units:
            # So they start out facing the right direction
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
                # print unit.soldier_type.name+" "+str(unit.soldier_type.quality)
                if unit.soldier_type.mount.name == 'None':
                    unit.name_id = self.canvas.create_text(unit.x, unit.y, text=(
                        "{} ({}; {}): {}, {}".format(unit.soldier_type.name,
                                                     ', '.join(map(lambda w: w.name, unit.soldier_type.weapons)),
                                                     unit.soldier_type.armor.name, unit.soldier_type.strength,
                                                     unit.soldier_type.health)))
                else:
                    unit.name_id = self.canvas.create_text(unit.x, unit.y, text=(
                        "{} ({}; {}): {}, {}, {}".format(unit.soldier_type.name,
                                                         ', '.join(map(lambda w: w.name, unit.soldier_type.weapons)),
                                                         unit.soldier_type.armor.name, unit.soldier_type.strength,
                                                         unit.soldier_type.health, unit.soldier_type.mount.name)))

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

                            # Allow the troop being hit by the projectile to try and defend a little.
                            defense = p.target.get_ranged_defense(owner_nation.tech.get_best_in_category('material'))
                            is_shield = p.target.weapons[1].shield
                            armor_pierce = p.launcher.get_ranged_weapon().armor_pierce
                            siege_weapon = p.launcher.get_ranged_weapon().siege_weapon
                            is_heavy = p.target.armor.heavy

                            if is_shield:
                                damage = int(damage / 2)
                            # print p.launcher.name + "'s ranged attack was deflected by "+p.target.name+"'s shield: "+str(damage)
                            elif not is_heavy:
                                damage *= 2
                                # print p.launcher.name + "'s ranged attack was left unprotected by "+p.target.name+"'s lack of a shield: "+str(damage)

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
                                    # print p.launcher.name + "'s ranged attack impacted "+p.target.name+"'s light armor: "+str(damage)

                            if random.randint(0, p.target.discipline) == 0:
                                p.target.fatigue += 1

                            # Can't do less than 0 damage
                            total_damage = max(damage - defense, 0)

                            original_health = p.target.health

                            p.target.health -= total_damage

                            if p.target.health <= 0:
                                overkill = 1
                                if siege_weapon:
                                    overkill += p.target.health * -1 / original_health
                                stats['troops_killed'] += overkill
                                stats[p.launcher.name]['kills'] += overkill
                                stats[p.launcher.name][weapon]['kills'] += overkill

                                if not p.target.name in enemy_stats:
                                    enemy_stats[p.target.name] = utility.base_soldier_stats()
                                enemy_stats[p.target.name]['deaths'] += overkill
                                enemy_stats['troops_lost'] += overkill
                                p.target.unit.handle_death(p.target)

                                num = 1
                                while num < overkill:
                                    if num < len(p.target.soldiers):
                                        p.target.unit.handle_death(p.target.soldiers[num])
                                    num += 1
                else:
                    p.skip_step -= 1

                if hit or x < 0 or x > 1000 or y < 0 or y > 600:
                    if self.use_graphics:
                        self.canvas.delete(p.id)

                    proj.remove(p)
            except:  # Remove this if we don't have a target
                if self.use_graphics:
                    self.canvas.delete(p.id)

                proj.remove(p)

    def check_end_battle(self):
        # if there are no units left, end the battle
        if (self.size(self.force_a) <= 0 and self.a_army.size() <= 0) or (
                self.size(self.force_b) <= 0 and self.b_army.size() <= 0):
            # Zero the army just in case anything got messed up
            if self.size(self.force_a) <= 0:  # A is always the attackers
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

            if len(current_unit.soldiers) == 0:  # No soldiers, remove this and untarget
                if current_unit.targeted is not None:
                    current_unit.targeted.target = None

                force.remove(current_unit)

                continue

            if self.use_graphics:
                self.canvas.coords(current_unit.name_id, current_unit.x, current_unit.y - 20)

            # Targeting stuff
            if current_unit.target is not None:  # if we have a target make sure it still exists
                if not current_unit.target in enemy_force:
                    current_unit.target = None
                elif len(current_unit.target.soldiers) == 0:
                    current_unit.target = None

            # If we don't have a target, target the closest unit.
            if current_unit.target is None or random.randint(0, SWITCH_TARGET_COUNT) == 0:
                current_unit.target = utility.get_nearest_enemy(current_unit, enemy_force)

                if current_unit.target is not None:
                    current_unit.target.targeted = current_unit
                else:
                    continue

            current_unit.move()
            current_unit.handle_ranks()

            for soldier in current_unit.soldiers:
                # Targeting stuff
                if current_unit.target is None:
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
            normal_defense = troop.armor.defense_skill_multiplier * use_weapon.defense_skill_multiplier * random.randint(
                0, troop.strength)

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

            sys.stdout.write("\rBattle for {}: {}(Soldiers: {}) vs. {}(Soldiers: {})".format(self.city.name,
                                                                                             self.a.name.short_name(),
                                                                                             self.a_army.size(),
                                                                                             self.b.name.short_name(),
                                                                                             self.b_army.size()))
            sys.stdout.flush()

            if a_unit is None or b_unit is None:
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

            self.handle_units(self.force_a, self.a, self.proj_a, self.force_b, self.b, self.a.color, self.a_stats,
                              self.b_stats)
            if self.over:
                return

            self.handle_units(self.force_b, self.b, self.proj_b, self.force_a, self.a, self.b.color, self.b_stats,
                              self.a_stats)
            if self.over:
                return

            a_force_size = self.size(self.force_a)
            b_force_size = self.size(self.force_b)

            # print(a_force_size, b_force_size)

            # Add more troops if possible
            if a_force_size < 10 or a_force_size < self.a_amount // 2:
                self.setup_army(self.a_army, self.force_a, self.a.color, (350, 650), (50, 100),
                                max(10, self.a_amount - a_force_size))
            if b_force_size < 10 or b_force_size < self.b_amount // 2:
                self.setup_army(self.b_army, self.force_b, self.b.color, (350, 650), (500, 550),
                                max(10, self.b_amount - b_force_size))

            if self.a_army.size() > 0 and a_force_size == 0:
                self.setup_army(self.a_army, self.force_a, self.a.color, (350, 650), (50, 100), self.a_amount)

            if self.b_army.size() > 0 and b_force_size == 0:
                self.setup_army(self.b_army, self.force_b, self.b.color, (350, 650), (500, 550), self.b_amount)

            a_cur = self.a_army.size() + a_force_size
            b_cur = self.b_army.size() + b_force_size

            sys.stdout.write(
                "\rBattle of {}: {}(Soldiers: {}) vs. {}(Soldiers: {})".format(self.city.name, self.a.name.short_name(),
                                                                               a_cur, self.b.name.short_name(), b_cur))
            sys.stdout.flush()

            if not self.over:
                if self.use_graphics:
                    self.parent.title(
                        "Battle of {}: {}(Reinforcements: {}) vs. {}(Reinforcements: {})".format(self.city.name,
                                                                                                 self.a.name.short_name(),
                                                                                                 self.a_army.size(),
                                                                                                 self.b.name.short_name(),
                                                                                                 self.b_army.size()))

                    self.after_id = self.parent.after(self.battle_speed.get(), self.main_phase)

                    break

