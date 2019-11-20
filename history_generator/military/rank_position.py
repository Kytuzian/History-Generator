import math

from military.soldier import TROOP_RADIUS


class RankPosition:
    def __init__(self, unit, rank, position, canvas):
        self.unit = unit
        self.rank = rank
        self.position = position

        self.canvas = canvas

        self.x, self.y = 0, 0

        self.soldier = None

    def change_soldier(self, soldier):
        if soldier.rank_position is not None:
            soldier.rank_position.soldier = None

        soldier.rank_position = self
        self.soldier = soldier

    def has_soldier(self):
        return self.soldier is not None

    def calculate_position(self):
        d1 = ((len(self.unit.ranks[0]) - 1) / 2.0 - self.position) * (TROOP_RADIUS + 1)
        d2 = -self.rank * (TROOP_RADIUS + 1)

        t1 = math.atan2(self.unit.dy, self.unit.dx) + math.pi / 2.0
        t2 = t1 - math.pi / 2.0
        self.x = self.unit.x + math.cos(t1) * d1 + math.cos(t2) * d2
        self.y = self.unit.y + math.sin(t1) * d1 + math.sin(t2) * d2