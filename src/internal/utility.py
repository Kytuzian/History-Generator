import random
import shlex
import struct
import subprocess
import time

import tkFont

from math import *

import sys
import platform

import os

START_BATTLES_MINIMIZED = False

S_WIDTH = 1000
S_HEIGHT = 1000

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

CELL_SIZE = 6  # cells are squares, this is the side length

SCROLL_SPEED = CELL_SIZE


def listbox_capacity(listbox):
    font = tkFont.Font(listbox, listbox['font'])

    return listbox.winfo_height() / font.metrics()['ascent']


def count(l):
    res = {}
    for i in l:
        if i in res:
            res[i] += 1
        else:
            res[i] = 1

    return res


def tuplize(l):
    res = l

    for i in xrange(len(res)):
        if isinstance(res[i], list):
            res[i] = tuplize(res[i])

    return tuple(res)


def get_time_span_length(start_date, end_date):
    year_dif, month_dif, day_dif = end_date[0] - start_date[0], end_date[1] - start_date[1], end_date[2] - start_date[2]

    if day_dif < 0:
        month_dif -= 1
        day_dif += 30

    if month_dif < 0:
        year_dif -= 1
        month_dif += 12

    return year_dif, month_dif, day_dif


def get_container(s, start, end, start_pos):
    level = 1

    i = start_pos
    while i < len(s):
        if s[i] == start:
            level += 1
        elif s[i] == end:
            level -= 1
            if level == 0:
                break

        i += 1

    return s[start_pos:i]


def find_container_of(s, start, end, char):
    # Start here, and go back until we find the starting bracket
    level = 0

    start_pos = 0
    while start_pos < len(s):
        if s[start_pos] == start:
            level += 1
        elif s[start_pos] == end:
            level -= 1
        elif s[start_pos] == char and level == 1:
            break
        start_pos += 1

    if start_pos >= len(s) - 1:
        raise Exception('\'{}\' not found in {}.'.format(char, s))
    while start_pos > 0:
        if s[start_pos] == end:
            level += 1
        elif s[start_pos] == start:
            level -= 1
            if level == 0:
                break

        start_pos -= 1

    level = 1
    end_pos = start_pos + 1
    while end_pos < len(s):
        if s[end_pos] == start:
            level += 1
        elif s[end_pos] == end:
            level -= 1
            if level == 0:
                break

        end_pos += 1

    return start_pos, end_pos


# So that if an inner section is detected, its entire contents are ignored
# For example, separate_container('<test|test1>|test2', '<', '>', '|') will return ['<test|test1>', 'test2']
def separate_container(s, start, end, char):
    result = []
    level = 0

    i = 0
    while len(s) > 0 and i < len(s):
        if s[i] == char and level == 0:
            result.append(s[:i])
            s = s[i + 1:]
            i = 0
        else:
            if s[i] == start:
                level += 1
            elif s[i] == end:
                level -= 1
            i += 1

    if len(s) > 0:
        result.append(s)

    return result


def titlecase(s):
    new_words = []
    for word in s.split():
        if not word in ['of', 'by', 'a', 'the']:
            word = word[0].upper() + word[1:]

        new_words.append(word)

    # First word is always capitalized
    if len(new_words) > 0 and len(new_words[0]) > 0:
        new_words[0] = new_words[0][0].upper() + new_words[0][1:]

    return ' '.join(new_words)


def capitalize_first_letter(s):
    return s[0].upper() + s[1:]


def displayify_text(s):
    words = s.split('_')
    words = map(capitalize_first_letter, words)
    return ' '.join(words)


def base_war_stats():
    base = {}

    base['troops_lost'] = 0
    base['troops_killed'] = 0

    return base


def base_stats():
    base = {}

    base['troops'] = 0
    base['troops_lost'] = 0
    base['troops_killed'] = 0
    base['projectiles_launched'] = 0
    base['projectiles_hit'] = 0
    base['attacks_won'] = 0

    return base


def base_soldier_stats():
    base = {}

    base['attacks'] = 0
    base['attacks_won'] = 0
    base['kills'] = 0
    base['deaths'] = 0
    base['projectiles_launched'] = 0
    base['projectiles_hit'] = 0

    return base


def base_weapon_stats():
    base = {}

    base['attacks'] = 0
    base['attacks_won'] = 0
    base['kills'] = 0

    return base


def show_dict(d, depth=1, recurse=True, gen=None):
    for stat, v in sorted(d.items()):
        if isinstance(v, dict):
            if recurse:
                if gen != None:
                    gen.write_to_gen_log('{}{}:'.format('\t' * depth, displayify_text(stat)))
                else:
                    print('{}{}:'.format('\t' * depth, displayify_text(stat)))
                show_dict(v, depth=depth + 1, recurse=recurse, gen=gen)
        else:
            if gen != None:
                gen.write_to_gen_log('{}{}: {}'.format('\t' * depth, displayify_text(stat), v))
            else:
                print('{}{}: {}'.format('\t' * depth, displayify_text(stat), v))


def fst(t):
    return t[0]


def snd(t):
    return t[1]


# Finds the corresponding keys in a dictionary and applies the function to both, creating a new dictionary
# f_single is used if the key appears in only one of the dictionaries
def zip_dict_with(f, a, b, f_single=None):
    res = {}
    for k in a:
        if k in b:
            res[k] = f(a[k], b[k])
        else:
            if f_single != None:
                res[k] = f_single(a[k])

    if f_single != None:
        for k in b:
            if not k in res:
                res[k] = f_single(b[k])

    return res


def get_nearest_enemy(unit, check, check_unit=None):
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


# From https://gist.github.com/jtriley/1108174
def get_terminal_size():
    """ getTerminalSize()
     - get width and height of console
     - works on linux,os x,windows,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        tuple_xy = (80, 25)  # default value
    return tuple_xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass


def _get_terminal_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass


def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])


terminal_width = -1


def show_bar(i, total, start_time=None, width=80, message='', number_limit=False):
    global terminal_width
    if terminal_width == -1:
        terminal_width, _ = get_terminal_size()
        terminal_width -= 1

    if terminal_width != -1:
        width = terminal_width

    if isinstance(total, int) or isinstance(total, float):
        number_limit = True

    # Because we start counting at 0
    i += 1

    # Just to make sure we don't get a ridiculously long bar
    i = min(total, i)

    time_message = ''
    if start_time != None:
        elapsed = time.time() - start_time
        if number_limit:
            estimated_remaining = elapsed / float(i) * float(total - i)
        else:
            estimated_remaining = elapsed / float(i) * float(len(total) - i)

        time_message = '{} seconds. '.format(round(estimated_remaining))

    message += time_message

    # The 2 is because of the []
    if not number_limit:
        bar_chunks = int(float(i) / float(len(total)) * (width - len(message) - 2))
    else:
        bar_chunks = int(float(i) / float(total) * (width - len(message) - 2))

    sys.stdout.write(
        '\r{}'.format(message) + '[{}{}]'.format('=' * bar_chunks, ' ' * (width - bar_chunks - len(message) - 2)))
    sys.stdout.flush()


def calculate_interception(v_e, v_p, (x_e, y_e), (x_p, y_p), theta_e):
    t1 = -(v_e * x_e * cos(theta_e) - v_e * x_p * cos(theta_e) + v_e * y_e * sin(theta_e) - v_e * y_p * sin(
        theta_e) + sqrt(-(v_e ** 2 * sin(theta_e) ** 2 - v_p ** 2) * x_e ** 2 + 2 * (
                v_e ** 2 * sin(theta_e) ** 2 - v_p ** 2) * x_e * x_p - (
                                    v_e ** 2 * sin(theta_e) ** 2 - v_p ** 2) * x_p ** 2 - (
                                    v_e ** 2 * cos(theta_e) ** 2 - v_p ** 2) * y_e ** 2 - (
                                    v_e ** 2 * cos(theta_e) ** 2 - v_p ** 2) * y_p ** 2 + 2 * (
                                    v_e ** 2 * x_e * cos(theta_e) * sin(theta_e) - v_e ** 2 * x_p * cos(theta_e) * sin(
                                theta_e)) * y_e - 2 * (
                                    v_e ** 2 * x_e * cos(theta_e) * sin(theta_e) - v_e ** 2 * x_p * cos(theta_e) * sin(
                                theta_e) - (v_e ** 2 * cos(theta_e) ** 2 - v_p ** 2) * y_e) * y_p)) / (
                     (cos(theta_e) ** 2 + sin(theta_e) ** 2) * v_e ** 2 - v_p ** 2)
    t2 = -(v_e * x_e * cos(theta_e) - v_e * x_p * cos(theta_e) + v_e * y_e * sin(theta_e) - v_e * y_p * sin(
        theta_e) - sqrt(-(v_e ** 2 * sin(theta_e) ** 2 - v_p ** 2) * x_e ** 2 + 2 * (
                v_e ** 2 * sin(theta_e) ** 2 - v_p ** 2) * x_e * x_p - (
                                    v_e ** 2 * sin(theta_e) ** 2 - v_p ** 2) * x_p ** 2 - (
                                    v_e ** 2 * cos(theta_e) ** 2 - v_p ** 2) * y_e ** 2 - (
                                    v_e ** 2 * cos(theta_e) ** 2 - v_p ** 2) * y_p ** 2 + 2 * (
                                    v_e ** 2 * x_e * cos(theta_e) * sin(theta_e) - v_e ** 2 * x_p * cos(theta_e) * sin(
                                theta_e)) * y_e - 2 * (
                                    v_e ** 2 * x_e * cos(theta_e) * sin(theta_e) - v_e ** 2 * x_p * cos(theta_e) * sin(
                                theta_e) - (v_e ** 2 * cos(theta_e) ** 2 - v_p ** 2) * y_e) * y_p)) / (
                     (cos(theta_e) ** 2 + sin(theta_e) ** 2) * v_e ** 2 - v_p ** 2)

    if t1 > 0:
        n = x_e - x_p + v_e * t1 * cos(theta_e)
        d = v_p * t1
        if n > d:
            n = d - 1 * 10 ^ -10
        theta_p1 = acos(n / d)

        return (t1, theta_p1)
    else:
        n = x_e - x_p + v_e * t2 * cos(theta_e)
        d = v_p * t2
        if n > d:
            n = d - 1 * 10 ^ -10
        theta_p2 = acos(n / d)

        return (t2, theta_p2)


def calculate_xy_vector((magnitude, angle)):
    return (magnitude * cos(angle), magnitude * sin(angle))


def calculate_polar_vector((dx, dy)):
    magnitude = sqrt(dx ** 2 + dy ** 2)

    return (magnitude, atan2(dy, dx))


def count_freq(l):
    res = {}
    for i in l:
        if not i in res:
            res[i] = 1
        else:
            res[i] += 1
    return res


# Adapted from:
# http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
def weighted_random_choice(choices, weight=None):
    if weight == None:
        weight = lambda i, _: len(choices) - i  # Makes it more likely to select early indexes.

    total = sum(weight(i, v) for i, v in enumerate(choices))
    r = random.uniform(0, total)
    accum = 0

    for i, v in enumerate(choices):
        w = weight(i, v)
        if accum + w >= r:
            return v
        accum += w
    return choices[0]


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
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def distance_squared((x1, y1), (x2, y2)):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


# This is faster than just do a distance check because we only have to calculate half of it sometimes.
# Full calculation is slower, but it's faster on average.
def collided((x1, y1, r1), (x2, y2, r2)):
    x_dist = (x1 - x2) ** 2
    length = (r1 + r2) ** 2
    if x_dist < length:
        y_dist = (y1 - y2) ** 2
        if y_dist < length:
            return y_dist + x_dist < length
        else:
            return False
    else:
        return False


def intersect((x, y), check, radius=1, ignore_exact=False):
    for index, ((cx, cy), cradius) in enumerate(check):
        if collided((x, y, radius), (cx, cy, cradius)):
            if ignore_exact and x == cx and y == cy:
                return -1
            else:
                return index

    return -1
