import random
import time

from math import *

import sys

START_BATTLES_MINIMIZED = False

S_WIDTH = 1000
S_HEIGHT = 1000

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

CELL_SIZE = 6 #cells are squares, this is the side length

#Finds the corresponding keys in a dictionary and applies the function to both, creating a new dictionary
def zip_dict_with(f, a, b):
    res = {}
    for k in a:
        if k in b:
            res[k] = f(a[k], b[k])
    return res

def get_nearest_enemy(unit, check, check_unit = None):
    min_distance = 1000000000

    target = None

    for i in check:
        d = distance_squared((unit.x, unit.y), (i.x, i.y))

        if d < min_distance:
            target = i

            min_distance = d

    return target

def rgb_color(r, g, b):
    return '#{}{}{}'.format(hex(r)[2:].ljust(2, '0'), hex(g)[2:].ljust(2, '0'), hex(b)[2:].ljust(2, '0'))

def show_bar(i, total, start_time=None, width=80, message='', number_limit = False):
    time_message = ''
    if start_time != None:
        end_time = time.time()
        elapsed = end_time - start_time
        if number_limit:
            estimated_remaining = float(i) / elapsed * float(total - i)
        else:
            estimated_remaining = float(i) / elapsed * float(len(total) - i)

        time_message = '{}s remaining. '.format(round(estimated_remaining))

    message += time_message

    if not number_limit:
        bar_chunks = int(float(i) / float(len(total)) * (width - len(message)))
    else:
        bar_chunks = int(float(i) / float(total) * (width - len(message)))

    sys.stdout.write('\r{}'.format(message) + '=' * bar_chunks + ' ' * (width - bar_chunks - len(message)))
    sys.stdout.flush()

def calculate_interception(v_e, v_p, (x_e, y_e), (x_p, y_p), theta_e):
    t1 = -(v_e*x_e*cos(theta_e) - v_e*x_p*cos(theta_e) + v_e*y_e*sin(theta_e) - v_e*y_p*sin(theta_e) + sqrt(-(v_e**2*sin(theta_e)**2 - v_p**2)*x_e**2 + 2*(v_e**2*sin(theta_e)**2 - v_p**2)*x_e*x_p - (v_e**2*sin(theta_e)**2 - v_p**2)*x_p**2 - (v_e**2*cos(theta_e)**2 - v_p**2)*y_e**2 - (v_e**2*cos(theta_e)**2 - v_p**2)*y_p**2 + 2*(v_e**2*x_e*cos(theta_e)*sin(theta_e) - v_e**2*x_p*cos(theta_e)*sin(theta_e))*y_e - 2*(v_e**2*x_e*cos(theta_e)*sin(theta_e) - v_e**2*x_p*cos(theta_e)*sin(theta_e) - (v_e**2*cos(theta_e)**2 - v_p**2)*y_e)*y_p))/((cos(theta_e)**2 + sin(theta_e)**2)*v_e**2 - v_p**2)
    t2 = -(v_e*x_e*cos(theta_e) - v_e*x_p*cos(theta_e) + v_e*y_e*sin(theta_e) - v_e*y_p*sin(theta_e) - sqrt(-(v_e**2*sin(theta_e)**2 - v_p**2)*x_e**2 + 2*(v_e**2*sin(theta_e)**2 - v_p**2)*x_e*x_p - (v_e**2*sin(theta_e)**2 - v_p**2)*x_p**2 - (v_e**2*cos(theta_e)**2 - v_p**2)*y_e**2 - (v_e**2*cos(theta_e)**2 - v_p**2)*y_p**2 + 2*(v_e**2*x_e*cos(theta_e)*sin(theta_e) - v_e**2*x_p*cos(theta_e)*sin(theta_e))*y_e - 2*(v_e**2*x_e*cos(theta_e)*sin(theta_e) - v_e**2*x_p*cos(theta_e)*sin(theta_e) - (v_e**2*cos(theta_e)**2 - v_p**2)*y_e)*y_p))/((cos(theta_e)**2 + sin(theta_e)**2)*v_e**2 - v_p**2)

    if t1 > 0:
        n = x_e-x_p+v_e*t1*cos(theta_e)
        d = v_p * t1
        if n > d:
            n = d - 1 * 10^-10
        theta_p1 = acos(n / d)

        return (t1, theta_p1)
    else:
        n = x_e-x_p+v_e*t2*cos(theta_e)
        d = v_p * t2
        if n > d:
            n = d - 1 * 10^-10
        theta_p1 = acos(n / d)

        return (t2, theta_p2)

def calculate_xy_vector((magnitude, angle)):
    return (magnitude * cos(angle), magnitude * sin(angle))

def calculate_polar_vector((dx, dy)):
    magnitude = sqrt(dx**2 + dy**2)

    return (magnitude, atan2(dy, dx))

#If reverse is false, then it selects heigher weights, if it's true, then it selects lower ones.
def weighted_random_choice(col, weight=None, reverse=True):
    if weight == None:
        weight = lambda i, _: i #Makes it more likely to select early indexes.

    if reverse:
        weight_calculate = lambda i, v: 1.0 / (weight(i, v) + 1.0)
    else:
        weight_calculate = weight

    accum = 0
    total = sum(map(lambda i: weight_calculate(i[0], i[1]), enumerate(col)))
    goal = random.random() * total

    for i, v in enumerate(col):
        weight_value = weight_calculate(i, v)
        # print(weight_value)
        if weight_value > 0: #If its not, we'll get an error for an empty randrange
            accum += weight_value

            if accum > goal:
                return v

    return col[0]

def rough_match(a, b, tolerance):
    return a + tolerance >= b and a - tolerance <= b

def clamp(a, maxv, minv):
    if a > maxv:
        return maxv
    elif a < minv:
        return minv
    else:
        return a

def product(l):
    return reduce(lambda a, b: a * b, l)

def flatten(l):
    result = []

    for sub_l in l:
        result += sub_l

    return result

def mutate(l, amount, base="qwertyuiopasdfghjklzxcvbnm"):
    result = []

    for i in xrange(random.randint(1, len(l) / amount + 1)):
        l.remove(random.choice(l))

    for i in xrange(random.randint(1, len(l) / amount + 1)):
        l.append(random.choice(l) if random.randint(0, 2) == 0 else random.choice(base))

    return l

def distance((x1, y1), (x2, y2)):
    return sqrt((x1-x2)**2 + (y1-y2)**2)

def distance_squared((x1, y1), (x2, y2)):
    return (x1 - x2)**2 + (y1 - y2)**2

#This is faster than just do a distance check because we only have to calculate half of it sometimes.
#Full calculation is slower, but it's faster on average.
def collided((x1, y1, r1), (x2, y2, r2)):
    x_dist = (x1 - x2)**2
    length = (r1 + r2)**2
    if x_dist < length:
        y_dist = (y1 - y2)**2
        if y_dist < length:
            return y_dist + x_dist < length
        else:
            return False
    else:
        return False

def intersect((x, y), check, radius=1, ignore_exact=False):
    for index,((cx, cy), cradius) in enumerate(check):
        if collided((x, y, radius), (cx, cy, cradius)):
            if ignore_exact and x == cx and y == cy:
                return -1
            else:
                return index

    return -1
