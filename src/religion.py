import random
import utility

from Tkinter import *

import events
import event_analysis

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

PRIEST_TOLERANCE_BONUS = 5

INTOLERANT_DOMAINS = ['war', 'fire', 'death', 'lightning', 'thunder',\
                      'wind', 'chaos', 'the underworld']
TOLERANT_DOMAINS = ['peace', 'wisdom', 'children', 'knowledge',\
                    'writing', 'music', 'storytelling', 'friendship'\
                    'the hearth', 'unity']

DOMAINS = ['fire', 'wind', 'water', 'air', 'lightning', 'death',\
           'children', 'fertility', 'harvest', 'wisdom', 'war',\
           'smithing', 'animals', 'earth', 'rivers', 'peace',\
           'knowledge', 'writing', 'music', 'storytelling',\
           'luck', 'thunder', 'friendship', 'wine', 'weaving',\
           'the sun', 'the hearth', 'the moon', 'the sky', 'messengers'\
           'chaos', 'unity', 'the underworld', 'creation']

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
            gained_domain = random.choice(DOMAINS)

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
    def __init__(self, language, name, nation):
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

    def add_god(self, domains=None):
        if domains == None:
            self.gods.append(God(self.language.make_name_word(), self, random.sample(DOMAINS, random.randint(1, 4))))
        else:
            self.gods.append(God(self.language.make_name_word(), self, domains))

    def get_tolerance(self):
        tolerance_value = self.tolerance

        for god in self.gods:
            tolerance_value += god.get_tolerance_score()

        for person in self.nation.notable_people:
            if person.alive and not person == self.nation.ruler:
                if person.role == 'priest':
                    amount = (1 - person.effectiveness) * PRIEST_TOLERANCE_BONUS

                    tolerance_value += amount

        #Can't have a negative tolerance
        return max(1, tolerance_value)

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

        self.gui_window.columnconfigure(1, weight=1)

        self.tolerance_label = Label(self.gui_window, text='Tolerance: {}'.format(self.get_tolerance()))
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
