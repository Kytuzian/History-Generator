from tkinter import *

import random

from culture import culture
from culture.culture import ART_CATEGORIES
from culture.form import Form
import internal.events as events
import internal.utility as utility
from internal.group.group import Group

AVERAGE_MAX_LIFE_EXPECTANCY = 60

SCIENTIST_RESEARCH_BONUS = 20

BASE_START_ARTISTIC_PERIOD_CHANCE = 720

# This is how many points to increase the weight by for the significance of the gods
# For example, if there is a war god with a significance of 10, then the resulting influence
# will be RELIGION_ROLE_INFLUENCE * 10 = 10 (for now).
RELIGION_ROLE_INFLUENCE = 1
ART_ROLE_INFLUENCE = 2
LENGTH_ROLE_INFLUENCE = 2

PRIEST_TOLERANCE_BONUS = 5

# Chance to relocate every month
RELOCATE_CHANCE = 72
GO_HOME = 10

# The actual art creation chances for a person is their base art_create_chance +/- the art_create_variance
PERSON_ROLES = {'general': {'art_create_chance': 0, 'art_create_variance': 0},
                'priest': {'art_create_chance': 0, 'art_create_variance':0},
                'oracle': {'art_create_chance': 100, 'art_create_variance': 15},
                'artist': {'art_create_chance': 40, 'art_create_variance': 20},
                'writer': {'art_create_chance': 40, 'art_create_variance': 15},
                'composer': {'art_create_chance': 50, 'art_create_variance': 25},
                'philosopher': {'art_create_chance': 30, 'art_create_variance': 20},
                'scientist': {'art_create_chance': 70, 'art_create_variance': 30},
                'revolutionary': {'art_create_chance': 0, 'art_create_variance': 0},
                'hero': {'art_create_chance': 0, 'art_create_variance': 0},
                'administrator': {'art_create_chance': 0, 'art_create_variance': 0},
                'historian': {'art_create_chance': 40, 'art_create_variance': 10},#Kenny Addition

                'conqueror': {'art_create_chance': 0, 'art_create_variance': 0},
                'emperor': {'art_create_chance': 0, 'art_create_variance': 0},
                'lord': {'art_create_chance': 0, 'art_create_variance': 0},
                'duke': {'art_create_chance': 0, 'art_create_variance': 0},
                'bishop': {'art_create_chance': 30, 'art_create_variance': 30},
                'prophet': {'art_create_chance': 50, 'art_create_variance': 50},
                'count': {'art_create_chance': 0, 'art_create_variance': 0},
                'bard': {'art_create_chance': 40, 'art_create_variance': 90},
                'singer': {'art_create_chance': 25, 'art_create_variance': 75},
                'musician': {'art_create_chance': 100, 'art_create_variance': 5},
                'quartermaster': {'art_create_chance': 0, 'art_create_variance': 0},
                'drillmaster': {'art_create_chance': 0, 'art_create_variance': 0},
                'seneschal': {'art_create_chance': 25, 'art_create_variance': 25},
                'professor': {'art_create_chance': 50, 'art_create_variance': 75},
                'master': {'art_create_chance': 75, 'art_create_variance': 50},
                'professional': {'art_create_chance': 15, 'art_create_variance': 100}
                }

PERIOD_FORMS = [['<|The> <titlecase><<color>|<flower>|flower|<adj>|<<place>|<nation_place>|<nation_place>>> <Period|Cycle>']]

NORMAL_FORMS = [['<titlecase><role>']]

class Period:
    def __init__(self, person, role=None):
        self.person = person

        #  Measured in months
        self.length = 0

        self.custom_weights = {}
        self.art = []

        if role is not None:
            self.role = role
        else:
            # Could possibly change roles. This is less likely if the person has spent more time in a particular role, and if they have created more works.
            # If it's our first run, then our role is only determined by our religion, otherwise, religion plays a more minor role as the person becomes more cemented.
            role_weights = person.get_role_weights()
            self.role = utility.weighted_random_choice(list(PERSON_ROLES.keys()), lambda _, role: role_weights[role])

        base_create_chance = PERSON_ROLES[self.role]['art_create_chance']
        base_create_variance = PERSON_ROLES[self.role]['art_create_variance']
        self.art_create_chance = base_create_chance + random.randint(-base_create_variance, base_create_variance)

        custom_tags = {'role': [self.role]}

        if (self.art_create_chance - base_create_variance // 10) > base_create_chance:
            custom_tags['creation_rate'] = ['prolific', 'productive', 'creative']
        elif (self.art_create_chance + base_create_chance // 10) < base_create_chance:
            custom_tags['creation_rate'] = ['quiet', 'lazy', 'unproductive', 'barren']
        else:
            custom_tags['creation_rate'] = ['normal', 'average', 'standard']

        if self.role in ART_CATEGORIES.keys():
            gen = Form(PERIOD_FORMS, custom_tags=custom_tags)
        else:
            gen = Form(NORMAL_FORMS, custom_tags=custom_tags)

        self.name = gen.generate(nation=self.person.nation, creator=self.person)[0]

    def get_info(self):
        # We store the actual art data in the cultures for the various nations
        # We'll retrieve it when we load the game.
        res = {'length': self.length, 'custom_weights': self.custom_weights,
               'art_create_chance': self.art_create_chance, 'role': self.role, 'name': self.name,
               'art': list(map(lambda art: art.name, self.art))}

        return res

    def get_weights(self, l):
        res = {}

        for i in l:
            if i in self.custom_weights:
                res[i] = self.custom_weights[i]
            else:
                res[i] = 1

        return res

    def choice(self, options, amount=1):
        def weight(_, v):
            if v in self.custom_weights:
                return self.custom_weights[v]
            else:
                return 1

        converted = {}
        for i in range(len(options)):
            if isinstance(options[i], list):
                converted[utility.tuplize(options[i])] = options[i]
                options[i] = utility.tuplize(options[i])

        chosen_item = utility.weighted_random_choice(options, weight=weight)

        if chosen_item in self.custom_weights:
            self.custom_weights[chosen_item] += amount
        else:
            self.custom_weights[chosen_item] = 1 + amount

        if chosen_item in converted:
            return converted[chosen_item]
        else:
            return chosen_item

    def choose(self, option, amount=1):
        if isinstance(option, list):
            option = tuple(option)

        if option in self.custom_weights:
            self.custom_weights[option] += amount
        else:
            self.custom_weights[option] = amount

class Person:
    def __init__(self, nation, city, name, religion, role=None):
        self.name = name
        self.nation = nation
        self.home = city
        self.city = city
        self.age = 1

        # Target is the place that we are going to when we relocate
        # Travel is the group that we are traveling in
        self.target = None
        self.travel = None

        #added secularism
        if random.randint(0, 100) > 5:
            self.religion = religion
        else:
            self.religion = None

        # Each person's life is separated into one (or many periods)
        self.periods = []
        self.start_new_period(role=role)

        self.effectiveness = 0.5 + random.random() + random.random()**5

        self.alive = True

        self.nation.parent.event_log.add_event('NotablePersonBirth',
                                               {'nation_a': self.nation.id,
                                                'person_a': self.name,
                                                'person_a_role': self.periods[-1].role},
                                               self.nation.parent.get_current_date())

    def save(self, path):
        res = {'name': self.name, 'home': self.home.name, 'city': self.city.name, 'age': self.age,
               'religion': self.religion.name, 'effectiveness': self.effectiveness, 'alive': self.alive, 'periods': []}

        for period in self.periods:
            res['periods'].append(period.get_info())

        with open(path + self.name + '.txt', 'w') as f:
            f.write(str(res))

    def get_tolerance_score(self):
        if self.periods[-1].role == 'priest':
            return (1 - self.effectiveness) * PRIEST_TOLERANCE_BONUS
        elif self.periods[-1].role == 'bishop':
            return (1 - self.effectiveness) * (PRIEST_TOLERANCE_BONUS * 2)
        elif self.periods[-1].role == 'prophet':
            return (1 - self.effectiveness) * (PRIEST_TOLERANCE_BONUS * 3)
        else:
            return 0

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title('{} ({})'.format(self.name, self.periods[-1].role))
        self.gui_window.geometry("500x750+0+0")

        self.gui_window.columnconfigure(4, weight=1)
        self.gui_window.rowconfigure(4, weight=1)

        self.age_label = Label(self.gui_window, text='Age: {}'.format(self.age))
        self.age_label.grid(row=0, column=0, sticky=W)

        self.period_choice = StringVar()
        self.period_choice.set(self.periods[0].name)

        self.periods_label = Label(self.gui_window, text='Period:')
        self.periods_label.grid(row=1, column=0, sticky=W)

        self.periods_choice = OptionMenu(self.gui_window, self.period_choice, *list(map(lambda period: period.name, self.periods)))
        self.periods_choice.grid(row=2, column=0, columnspan=2, sticky=W)

        self.period_select = Button(self.gui_window, text='Select', command=self.select_period)
        self.period_select.grid(row=2, column=2, sticky=W)

        self.period_length_label = Label(self.gui_window, text='Length:')
        self.period_length_label.grid(row=3, column=0, sticky=W)

        self.period_role_label = Label(self.gui_window, text='Role:')
        self.period_role_label.grid(row=3, column=1, sticky=W)

        self.period_art_display = Listbox(self.gui_window)
        self.period_art_display.grid(row=4, column=0, columnspan=5, sticky=W+E+N+S)
        self.period_art_display.bind('<Double-Button-1>', self.select_art)

        self.select_period(self.periods[-1].name)

    def select_period(self, period_override=None):
        if period_override is None:
            period_name = self.period_choice.get()
        else:
            period_name = period_override

        period_index = 0
        for i, period in enumerate(self.periods):
            if period.name == period_name:
                period_index = i

        self.periods_label['text'] = 'Period: {}'.format(self.periods[period_index].name)
        self.period_length_label['text'] = 'Length: {}'.format(self.periods[period_index].length)
        self.period_role_label['text'] = 'Role: {}'.format(self.periods[period_index].role)

        self.period_art_display.delete(0, END)
        for art in self.periods[period_index].art:
            self.period_art_display.insert(END, '{} ({})'.format(art.name, art.subject))

    def select_art(self, event, period_override=None):
        if period_override is None:
            period_name = self.period_choice.get()
        else:
            period_name = period_override

        period_index = 0
        for i, period in enumerate(self.periods):
            if period.name == period_name:
                period_index = i

        selected_item = self.period_art_display.get(self.period_art_display.curselection())
        for art in self.periods[period_index].art:
            if '{} ({})'.format(art.name, art.subject) == selected_item:
                art.show_information_gui()
                break

    def get_role_weights(self):
        res = {}
        for role in PERSON_ROLES.keys():
            res[role] = 1

        for period in self.periods:
            res[period.role] += period.length * LENGTH_ROLE_INFLUENCE
            res[period.role] += len(period.art) * ART_ROLE_INFLUENCE

        if self.religion is not None:
            religion_weights = self.religion.get_role_weights()
            for (role, weight) in religion_weights.items():
                res[role] += weight * RELIGION_ROLE_INFLUENCE

        return res

    def choice(self, options, amount=1):
        return self.periods[-1].choice(options, amount=amount)

    def choose(self, option, amount=1):
        self.periods[-1].choose(option, amount=amount)

    def get_weights(self, l):
        return self.periods[-1].get_weights(l)

    def start_new_period(self,role=None):
        if len(self.periods) > 0:
            prev_role = self.periods[-1].role
        else:
            prev_role = ''

        self.periods.append(Period(self,role=role))

        self.nation.parent.event_log.add_event('NotablePersonPeriod',
                                               {'nation_a': self.nation.id,
                                                'person_a': self.name,
                                                'person_a_prev_role': prev_role,
                                                'person_a_role': self.periods[-1].role,
                                                'period_name': self.periods[-1].name},
                                               self.nation.parent.get_current_date())

    def get_effectiveness(self):
        return self.effectiveness

    def handle_death(self):
        self.nation.parent.event_log.add_event('NotablePersonDeath',
                                               {'nation_a': self.nation.id,
                                                'person_a': self.name,
                                                'person_a_role': self.periods[-1].role},
                                               self.nation.parent.get_current_date())

    def arrival(self, group):
        self.city = self.target
        self.target = None

    def handle_monthly(self):
        if self.target is not None:
            self.travel.step([])

        if self.alive:
            if self.target is None and random.randint(0, RELOCATE_CHANCE) == 0 and len(self.nation.cities) > 0:
                if self.city != self.home:
                    if random.randint(0, GO_HOME) == 0:
                        self.target = self.home

                if self.target is None:
                    self.target = random.choice(self.nation.cities)

                self.travel = Group(self.nation.parent, self.name, [self], self.city.position, self.target.position, self.nation.color, None, self.arrival)

            self.periods[-1].length += 1

            if not self == self.nation.ruler:
                if self.periods[-1].role == 'scientist':
                    amount = self.effectiveness**2 * SCIENTIST_RESEARCH_BONUS
                    if self.nation.current_research is not None:
                        self.nation.current_research.do_research(amount)
                elif self.periods[-1].role == 'revolutionary':
                    self.nation.mod_morale(-self.effectiveness**2)
            if self.periods[-1].role in ART_CATEGORIES:
                # Let's make some art
                if random.randint(0, self.periods[-1].art_create_chance) == 0:
                    new_art = culture.create_art(self.nation, self)

                    if new_art is not None:
                        self.nation.culture.add_art(new_art)
                        self.periods[-1].art.append(new_art)

                        self.nation.parent.event_log.add_event('ArtCreated',
                                                               {'nation_a': self.nation.id,
                                                                'person_a': self.name,
                                                                'person_a_role': self.periods[-1].role,
                                                                'art': str(new_art)},
                                                               self.nation.parent.get_current_date())

                # Let's start a new artistic period in our lives (maybe)
                if random.randint(0, BASE_START_ARTISTIC_PERIOD_CHANCE - self.periods[-1].length) == 0:
                    self.start_new_period()

    def history_step(self):
        self.age += 1

        if random.randint(0, AVERAGE_MAX_LIFE_EXPECTANCY) == 0: #The person died
            self.alive = False

    def __repr__(self):
        return "{}({}): {}".format(self.name, self.age, self.periods[-1].role)
