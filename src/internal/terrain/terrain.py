import math

import internal.utility as utility

MAX_HEIGHT = 4000

BASE_CELL_FOOD_PRODUCTION = 10
BASE_CELL_MIN_FOOD_PRODUCTION = 1


def to_celsius(t):
    return (t - 32.0) / (9.0 / 5.0)


def to_farenheit(t):
    return (9.0 / 5.0) * t + 32.0


def to_meters(f):
    return 0.3048 * f


def to_feet(m):
    return m / 0.3048


def temperature(elevation, height, world_height):
    r = float(world_height) / 2
    latitude = (float(height) - r) / world_height * 180 / math.pi

    temp = 103 - 1.45 * latitude - 0.00227 * elevation - 0.0054 * latitude ** 2 - 0.000007 * latitude * elevation

    return to_celsius(temp)


class Terrain:
    def __init__(self, height, moisture):
        self.name = ''
        self.color = ''
        self.height = max(0, height)
        self.moisture = moisture

        self.setup()

    def get_info(self):
        res = {}
        res['height'] = self.height
        res['moisture'] = self.moisture
        res['name'] = self.name
        res['color'] = self.color

        return res

    def setup(self):
        if self.height == 0:
            self.name = 'water'
            self.color = utility.rgb_color(0, 0, 255)
        elif self.height < 0.1 and self.moisture < 0.5:
            self.name = 'sand'
            self.color = utility.rgb_color(237, 201, 175)
        elif self.height > 0.5 and self.moisture < 0.5:
            self.name = 'snow'
            self.color = utility.rgb_color(200, 255, 255)
        elif self.moisture > 0.5:
            self.name = 'forest'
            self.color = utility.rgb_color(34, 139, 34)
        else:
            self.name = 'land'
            self.color = utility.rgb_color(0, 255, 0)

    def get_food_production_multiplier(self):
        if self.name == 'water':
            return 1.1
        elif self.name == 'land':
            return 1.0
        elif self.name == 'sand':
            return 0.95
        elif self.name == 'forest':
            return 1.05
        elif self.name == 'snow':
            return 0.75

    def is_settleable(self):
        return not self.is_water()

    def is_water(self):
        return self.name == 'water'
