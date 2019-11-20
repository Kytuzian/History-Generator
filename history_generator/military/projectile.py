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