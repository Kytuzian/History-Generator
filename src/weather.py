import math

def temperature(elevation, height, world_height):
    r = float(world_height) / 2
    latitude = (float(height) - r) / world_height * 180 / math.pi

    temp = 103 - 1.45*latitude - 0.00227*elevation - 0.0054*latitude**2 - 0.000007*latitude*elevation

    return temp
