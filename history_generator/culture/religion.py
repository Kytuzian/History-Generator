import random

from tkinter import *

import internal.events as events
import internal.event_analysis as event_analysis
import internal.gui as gui
import civil.people as people
from culture.god import God, DOMAINS

# In percent
MONOTHEISM_CHANCE = 20

# In percent
LOSE_GOD_CHANCE = 1
GAIN_GOD_CHANCE = 8

MAX_BASE_TOLERANCE = 100


class Religion:
    def __init__(self, parent, language, name):
        self.parent = parent
        self.name = name
        self.language = language

        self.polytheistic = random.randint(0, 100) > MONOTHEISM_CHANCE

        self.gods = []
        if self.polytheistic:
            for new_god in range(random.randint(1, 10)):
                self.add_god()
        else:
            self.add_god(['everything'])

        # Lower tolerance means more tolerant
        self.tolerance = random.randint(1, MAX_BASE_TOLERANCE)

        self.age = 0

        # Adherents are organized by city name
        self.adherents = {}

    def add_god(self, domains=None):
        if domains is None:
            self.gods.append(
                God(self.language.make_name_word(), self, random.sample(DOMAINS.keys(), random.randint(1, 4))))
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
            # print role
            role_weights[role] = 0

        # print role_weights['professor']

        for god in self.gods:
            for domain in god.domains:
                for (role, weight) in DOMAINS[domain].items():
                    role_weights[role] += god.importance * weight

        return role_weights

    def history_step(self, parent):
        self.age += 1

        # Obviously the number of gods in a monotheistic religion can't change.
        if self.polytheistic:
            for god in self.gods:
                if random.randint(0, 100) < LOSE_GOD_CHANCE:
                    parent.event_log.add_event('ReligionGodRemoved',
                                               {'god_a': god.name, 'religion_a': self.name},
                                               parent.get_current_date())

                    self.gods.remove(god)
                else:
                    god.history_step(parent)

            if random.randint(0, 100) < GAIN_GOD_CHANCE:
                self.add_god()

                parent.event_log.add_event('ReligionGodAdded',
                                           {'god_a': self.gods[-1].name,'religion_a': self.name},
                                           parent.get_current_date())

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

        all_events = event_analysis.find_religion_mentions(self.parent.event_log, self.name)
        all_events = sorted(all_events.event_list, key=lambda event: event.date)

        self.event_log_display = Listbox(self.gui_window)

        for event in all_events:
            self.event_log_display.insert(END, event.text_version())

        self.event_log_display.grid(row=2, columnspan=2, sticky=W + E)
