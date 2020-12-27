import math

from internal import utility as utility
from military.rank_position import RankPosition
from research.equipment_list import all_ranged_weapons

TROOP_MOVEMENT_SPEED = 1


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
            if weapon.name in list(map(lambda w: w.name, all_ranged_weapons)):
                use_weapon = weapon

        if use_weapon is None:
            self.ammunition = 0
        else:
            self.ammunition = use_weapon.ammunition * len(self.soldiers)

    def setup_ranks(self):
        self.ranks = []

        i = 0
        for rank in range(self.soldier_type.ranks):
            self.ranks.append([])
            for rank_position in range(self.soldier_type.rank_size):
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

        if soldier.targeted is not None:
            soldier.targeted.target = None

        self.soldiers.remove(soldier)

        if soldier.rank_position:
            soldier.rank_position.soldier = None

        if len(self.soldiers) == 0:
            if self.targeted is not None:
                self.targeted.target = None

            self.force.remove(self)

            if self.canvas:
                self.canvas.delete(self.name_id)

    def handle_ranks(self):
        # Fill up earlier positions in the formation
        for rank_i, rank in enumerate(self.ranks):
            for position_i, position in enumerate(rank):
                if not position.has_soldier():
                    next_soldier = self.get_next_soldier(rank_i, position_i)

                    if next_soldier is not None:
                        position.change_soldier(self.get_next_soldier(rank_i, position_i))

        # clear out empty ranks
        for rank_i, rank in enumerate(self.ranks):
            for position_i, position in enumerate(rank):
                if not position.has_soldier():  # Remove the rest of this, because there are no soldiers after this
                    self.ranks[rank_i] = rank[:position_i]
                    self.ranks = self.ranks[:rank_i + 1]  # We don't need any of the rest of the ranks either
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

        if self.soldier_type.mount is not None:
            mount_speed = self.soldier_type.mount.speed

        return int(math.log(self.soldier_type.speed, 2)) * (TROOP_MOVEMENT_SPEED + mount_speed)

    def get_movement_vector(self, vector_format='xy'):
        if self.target is not None and not self.soldier_type.ranged:
            if not self.in_range():
                d = utility.distance((self.x, self.y), (self.target.x, self.target.y))
                dx = self.target.x - self.x
                dy = self.target.y - self.y

                if vector_format == 'xy':
                    return (float(dx) / d * self.get_effective_speed(), float(dy) / d * self.get_effective_speed())
                elif vector_format == 'polar':  # Magnitude and angle
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
        if self.target is not None:
            tx, ty = self.target.get_position()
            self.dx, self.dy = tx - self.x, ty - self.y

            # print(self.x, self.y)
            # If we aren't in range, we need to move closer.
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
