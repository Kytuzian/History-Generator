import random
import utility

from Tkinter import *

import internal.events as events
import internal.event_analysis as event_analysis
import internal.gui as gui
import civil.people as people

#In percent
MONOTHEISM_CHANCE = 20

IMPORTANCE_CHANGE_CHANCE = 30 #In percent
IMPORTANCE_CHANGE_AMOUNT = 2

#In percent
LOSE_GOD_CHANCE = 1
GAIN_GOD_CHANCE = 8

#in percent
DOMAIN_GAIN_CHANCE = 1
DOMAIN_LOSE_CHANCE = 1

MAX_DOMAIN_COUNT = 5

MAX_IMPORTANCE = 10
TOLERANCE_MULTIPLIER = 1

MAX_BASE_TOLERANCE = 100

INTOLERANT_DOMAINS = ['war', 'fire', 'death', 'lightning', 'thunder',
                      'wind', 'chaos', 'the underworld', #Kenny - Addition
                      'blight', 'disease', 'conquest', 'sacrifice',
                      'lust', 'revenge', 'gluttony', 'envy', 'wrath',
                      'xenophobia', 'zeal', 'apathy'
                      ]
TOLERANT_DOMAINS = ['peace', 'wisdom', 'children', 'knowledge',
                    'writing', 'music', 'storytelling', 'friendship',
                    'the hearth', 'unity', #Kenny - Addition
                    'piety', 'charity', 'books', 'writing',
                    'tales', 'mastery', 'observations', 'understanding',
                    'morale', 'fervor', 'keen', 'passion'
                    ]

DOMAINS = {'fire': {'general': 0.5},
           'wind': {'artist': 1},
           'water': {'artist': 1},
           'air': {'artist': 1},
           'lightning': {'artist': 1},
           'death': {'general': 0.5},
           'children': {},
           'fertility': {},
           'harvest': {'administrator': 1},
           'wisdom': {'oracle': 1, 'scientist': 1, 'historian': 1, 'philosopher': 1},
           'war': {'general': 1},
           'smithing': {},
           'animals': {'artist': 1},
           'earth': {'artist': 1},
           'rivers': {'artist': 1},
           'peace': {'administrator': 1},
           'knowledge': {'historian': 1, 'scientist': 1},
           'writing': {'writer': 1, 'historian': 1, 'philosopher': 1},
           'music': {'composer': 1},
           'storytelling': {'writer': 1, 'oracle': 1, 'hero': 1},
           'luck': {},
           'thunder': {'artist': 1},
           'friendship': {},
           'wine': {},
           'weaving': {'seneschal':1},
           'the sun': {},
           'the hearth': {},
           'the moon': {},
           'the sky': {},
           'messenger': {},
           'chaos': {'revolutionary': 1},
           'unity': {'drillmaster':1, 'quartermaster':1},
           'the underworld': {'conqueror':1},
           'creation': {'emperor':1},
           'everything': {}, # For monotheistic religions

           'blight': {'revolutionary': 0.5},
           'disease': {},
           'conquest': {'scientist': 0.5, 'general':0.5},
           'sacrifice': {'oracle': 0.5},
           'lust': {'artist': 0.5},
           'revenge': {'hero': 0.5, 'revolutionary':0.5},
           'gluttony': {'composer': 1, 'artist':1, 'writer':1},
           'envy': {'historian': 0.5, 'oracle': 1},
           'wrath': {'revolutionary': 0.5, 'hero':1},
           'xenophobia': {'hero': 1, 'general':1},
           'zeal': {'revolutionary': 0.5, 'hero':0.5, 'general':0.5},
           'apathy': {'philosopher':0.5, 'scientist':0.5},

           'piety': {'oracle':1, 'prophet':0.5, 'priest':1, 'bishop':0.75},
           'charity': {'hero':1, 'professor':1},
           'books': {'writer':1, 'bard':1},
           'mastery': {'master':1, 'professional':1},
           'observations': {'philosopher':0.5, 'scientist':0.5, 'professor':0.5},
           'understanding': {'philosopher':1, 'professor':1},
           'morale': {'singer':1, 'lord':1},
           'fervor': {'revolutionary':0.5, 'scientist':0.5},
           'keen': {'general':0.5, 'administrator':0.5},
           'passion': {'hero':1, 'administrator':1}
           }

class God:
    def __init__(self, name, religion, domains):
        self.name = name
        self.is_male = random.choice([False, True])
        self.religion = religion
        self.domains = domains

        self.age = 0

        self.importance = random.randint(0, MAX_IMPORTANCE)

    def history_step(self, parent):
        self.age += 1

        if random.randint(0, 100) < IMPORTANCE_CHANGE_CHANCE:
            self.importance += random.randint(-IMPORTANCE_CHANGE_AMOUNT, IMPORTANCE_CHANGE_AMOUNT)

            self.importance = utility.clamp(self.importance, MAX_IMPORTANCE, 0)

        #We can't lose our last domain of course
        if len(self.domains) > 1 and random.randint(0, 100) < DOMAIN_LOSE_CHANCE:
            lost_domain = random.choice(self.domains)

            self.domains.remove(lost_domain)

            parent.events.append(events.EventReligionDomainRemoved('ReligionDomainRemoved', {'god_a': self.name, 'religion_a': self.religion.name, 'domain_a': lost_domain}, parent.get_current_date()))
            # print(parent.events[-1].text_version())

        if len(self.domains) <= MAX_DOMAIN_COUNT and random.randint(0, 100) < DOMAIN_GAIN_CHANCE:
            gained_domain = random.choice(DOMAINS.keys())

            if not gained_domain in self.domains:
                self.domains.append(gained_domain)

                parent.events.append(events.EventReligionDomainAdded('ReligionDomainAdded', {'god_a': self.name, 'religion_a': self.religion.name, 'domain_a': gained_domain}, parent.get_current_date()))
                # print(parent.events[-1].text_version())

    def get_tolerance_score(self):
        score = 0

        for i, domain in enumerate(self.domains):
            #Some domains are neutral, like smithing and animals
            if domain in TOLERANT_DOMAINS:
                score += TOLERANCE_MULTIPLIER * self.importance
            elif domain in INTOLERANT_DOMAINS:
                score -= TOLERANCE_MULTIPLIER * self.importance

        return score

    def get_gender(self):
        if self.is_male:
            return 'god'
        else:
            return 'goddess'

    def __repr__(self):
        if len(self.domains) > 2:
            return "{} ({}): {} of {}".format(self.name, self.importance, self.get_gender(), (", ".join(self.domains[:-1]) + ', and {}'.format(self.domains[-1])))
        elif len(self.domains) == 2:
            return '{} ({}): {} of {} and {}'.format(self.name, self.importance, self.get_gender(), self.domains[0], self.domains[1])
        elif len(self.domains) == 1:
            return '{} ({}): {} of {}'.format(self.name, self.importance, self.get_gender(), self.domains[0])

class Religion:
    def __init__(self, language, name):
        self.name = name

        self.language = language

        self.polytheistic = random.randint(0, 100) > MONOTHEISM_CHANCE

        self.gods = []
        if self.polytheistic:
            for new_god in xrange(random.randint(1, 10)):
                self.add_god()
        else:
            self.add_god(['everything'])

        #Lower tolerance means more tolerant
        self.tolerance = random.randint(1, MAX_BASE_TOLERANCE)

        self.age = 0

        # Adherents are organized by city name
        self.adherents = {}

    def add_god(self, domains=None):
        if domains is None:
            self.gods.append(God(self.language.make_name_word(), self, random.sample(DOMAINS.keys(), random.randint(1, 4))))
        else:
            self.gods.append(God(self.language.make_name_word(), self, domains))

    def get_tolerance(self):
        tolerance_value = self.tolerance

        for god in self.gods:
            tolerance_value += god.get_tolerance_score()

        # Can't have a negative or zero tolerance
        return max(1, tolerance_value)

    def get_role_weights(self):
        role_weights = {}
        for role in people.PERSON_ROLES:
            #print role
            role_weights[role] = 0

        #print role_weights['professor']

        for god in self.gods:
            for domain in god.domains:
                for (role, weight) in DOMAINS[domain].iteritems():
                    role_weights[role] += god.importance * weight

        return role_weights

    def history_step(self, parent):
        self.age += 1

        #Obviously the number of gods in a monotheistic religion can't change.
        if self.polytheistic:
            for god in self.gods:
                if random.randint(0, 100) < LOSE_GOD_CHANCE:
                    parent.events.append(events.EventReligionGodRemoved('ReligionGodRemoved', {'god_a': god.name, 'religion_a': self.name}, parent.get_current_date()))
                    # print(parent.events[-1].text_version())

                    self.gods.remove(god)
                else:
                    god.history_step(parent)

            if random.randint(0, 100) < GAIN_GOD_CHANCE:
                self.add_god()

                parent.events.append(events.EventReligionGodAdded('ReligionGodAdded', {'god_a': self.gods[-1].name, 'religion_a': self.name}, parent.get_current_date()))
                # print(parent.events[-1].text_version())

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title(self.name)
        self.gui_window.geometry("500x400+0+0")
        self.gui_window.config(background='white')

        self.gui_window.columnconfigure(1, weight=1)

        self.tolerance_label = gui.Label(self.gui_window, text='Tolerance: {}'.format(self.get_tolerance()))
        self.tolerance_label.grid(row=0, sticky=W)

        self.gods_display = Listbox(self.gui_window)

        for god in self.gods:
            self.gods_display.insert(END, god)

        self.gods_display.grid(row=1, columnspan=2, sticky=W + E)

        all_events = event_analysis.find_religion_mentions(self.name)
        all_events = sorted(all_events.event_list, key=lambda event: event.date)

        self.event_log_display = Listbox(self.gui_window)

        for event in all_events:
            self.event_log_display.insert(END, event.text_version())

        self.event_log_display.grid(row=2, columnspan=2, sticky=W + E)

