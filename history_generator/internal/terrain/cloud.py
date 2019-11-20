import random

class Cloud:
    def __init__(self, x, y, water):
        self.x = x
        self.y = y
        self.water = water

        self.processed = False

        self.wait = 125 * random.random() ** 5
        self.age = 0

    def add_water(self, amount):
        self.water += amount

    def precipitate(self):
        if self.age > self.wait:
            amount = random.random() * self.water
            self.water -= amount
        else:
            amount = 0
        return amount