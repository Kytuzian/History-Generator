import civil.city as city
import civil.people as people

import culture.culture as culture
import culture.language as language

import internal.group as group
import internal.utility as utility
import internal.gui as gui
import internal.events as events
import internal.event_analysis as event_analysis
import research.equipment_list

from military.troop import Troop

import research.tech as research

import math
import random

from Tkinter import *

OFFICE_MORALE_BONUS = 4

NATION_COLORS = ['dark orange', 'cadet blue', 'gold', 'deep sky blue',
                 'firebrick', 'maroon', 'sienna', 'dark slate blue',
                 'deep pink', 'dark orchid', 'slate gray', 'violet',
                 'navy', 'magenta', 'sandy brown', 'saddle brown',
                 'orchid', 'violet red', 'medium slate blue', 'purple', 'blue violet',
                 'dark sea green', 'hot pink', 'orange', 'indian red',
                 'red', 'brown', 'salmon', 'steel blue', 'royal blue', 'medium purple',
                 'dark slate gray', 'dark olive green', 'cyan', 'chocolate', 'orange red',
                 'tomato', 'gray', 'cornflower blue', 'goldenrod',
                 'midnight blue', 'rosy brown', 'plum', 'sky blue',
                 'dark violet', 'dark khaki', 'olive drab', 'medium turquoise',
                 'slate blue', 'powder blue', 'aquamarine']

OFFICE_MODIFIERS = ['tax_rate', 'army_spending', 'morale']
OFFICE_MODIFIER_MAX = 2

GOVERNMENT_TYPES = ["Principality", "Commonwealth", "Kingdom", "Hegemony", "Khanate",
                    "Socialist State", "Sultanate", "Republic", "Democracy", "Theocracy",
                    "Confederacy", "Oligarchy", "Aristocracy", "Meritocracy", "States",  # Kenny - Additions from here
                    "Empire", "Tsardom", "Caliphate", "Emirate", "Tribes", "Clan",
                    "Duchy", "Autocracy"

                    ]
INIT_CITY_COUNT = 1

CITY_FOUND_COST = 100000
SOLDIER_RECRUIT_COST = 500
SOLDIER_UPKEEP = 50

PEOPLE_LIMIT = 20

REARM_CHANCE = 5

TAX_MULTIPLIER = 2

# in order to prevent extremeley long late game names
NAME_SWITCH_THRESHOLD = 70

NOTABLE_PERSON_BIRTH_CHANCE = 150

PRIEST_TOLERANCE_BONUS = 5

GOVERNMENT_TYPE_BONUSES = {"Principality": {'food': 1, 'morale': 0.75, 'efficiency': 1, 'tolerance': 1,
                                            'conscription': 1.5},
                           "Kingdom": {'food': 1, 'morale': 0.75, 'efficiency': 1, 'tolerance': 1, 'conscription': 1.5},
                           "Sultanate": {'food': 1, 'morale': 0.75, 'efficiency': 1, 'tolerance': 1,
                                         'conscription': 1.5},
                           "Khanate": {'food': 1, 'morale': 0.75, 'efficiency': 1, 'tolerance': 1, 'conscription': 1.5},
                           "Socialist State": {'food': 2, 'morale': 0.5, 'efficiency': 1, 'tolerance': 1,
                                               'conscription': 1},
                           "States": {'food': 1, 'morale': 1, 'efficiency': 1, 'tolerance': 1, 'conscription': 1},
                           "Commonwealth": {'food': 1, 'morale': 1, 'efficiency': 1, 'tolerance': 1, 'conscription': 1},
                           "Democracy": {'food': 1, 'morale': 2, 'efficiency': 0.75, 'tolerance': 1, 'conscription': 1},
                           "Republic": {'food': 1, 'morale': 1.5, 'efficiency': 1, 'tolerance': 1, 'conscription': 1},
                           "Theocracy": {'food': 1, 'morale': 1.5, 'efficiency': 1, 'tolerance': 0.5,
                                         'conscription': 1},
                           "Confederacy": {'food': 1, 'morale': 1.5, 'efficiency': 0.75, 'tolerance': 1,
                                           'conscription': 1},
                           "Meritocracy": {'food': 1, 'morale': 0.75, 'efficiency': 2, 'tolerance': 1,
                                           'conscription': 1},
                           "Aristocracy": {'food': 1, 'morale': 1, 'efficiency': 0.75, 'tolerance': 1,
                                           'conscription': 1.5},
                           "Oligarchy": {'food': 1, 'morale': 1, 'efficiency': 0.75, 'tolerance': 1,
                                         'conscription': 1.5},
                           "Hegemony": {'food': 1, 'morale': 0.5, 'efficiency': 1, 'tolerance': 1, 'conscription': 2},
                           "Empire": {'food': 0.5, 'morale': 0.25, 'efficiency': 1.5, 'tolerance': 0.5,
                                      'conscription': 3},
                           "Tsardom": {'food': 1, 'morale': 0.35, 'efficiency': 0.75, 'tolerance': 1,
                                       'conscription': 2.5},
                           "Caliphate": {'food': 0.75, 'morale': 1.5, 'efficiency': 1, 'tolerance': 0.25,
                                         'conscription': 2},
                           "Emirate": {'food': 1.5, 'morale': 0.75, 'efficiency': 1, 'tolerance': 0.25,
                                       'conscription': 2},
                           "Tribes": {'food': 1.5, 'morale': 1, 'efficiency': 0.1, 'tolerance': 0.5,
                                      'conscription': 1.5},
                           "Clan": {'food': 0.75, 'morale': 1, 'efficiency': 0.75, 'tolerance': 0.5, 'conscription': 2},
                           "Duchy": {'food': 1.75, 'morale': 1.5, 'efficiency': 0.75, 'tolerance': 1,
                                     'conscription': 1.25},
                           "Autocracy": {'food': 0.25, 'morale': 1, 'efficiency': 1.5, 'tolerance': 0.25,
                                         'conscription': 4}}


class Nation:
    def __init__(self, parent, cities=None):
        self.displaying = ''
        self.language = language.Language()  # Create a new, random language

        self.age = 0

        self.parent = parent

        # Take a color that hasn't already been used.
        self.color = random.choice(parent.available_colors())

        CELLS_WIDTH = utility.S_WIDTH // utility.CELL_SIZE
        CELLS_HEIGHT = utility.S_WIDTH // utility.CELL_SIZE
        x = random.randint(int(CELLS_WIDTH * 0.1), int(CELLS_WIDTH * 0.9))
        y = random.randint(int(CELLS_HEIGHT * 0.1), int(CELLS_HEIGHT * 0.9))

        if cities is not None:
            self.cities = cities

            for city in self.cities:
                city.nation = self

                for cell in city.cells:
                    cell.update_self()
        else:
            self.cities = []

        self.money = 0

        self.id = parent.get_next_id('nation')

        self.notable_people = []
        self.culture = culture.Culture(self)

        self.ruler = None
        self.main_religion = None

        self.at_war = []
        self.allied = []
        self.trading = []
        self.relations = {}

        self.troop_tree = []

        self.treaties = []

        self.caravans = []

        self.moving_armies = []

        self.sidearm_list = random.sample(research.equipment_list.sidearm_list, 3)
        self.basic_weapon_list = random.sample(research.equipment_list.basic_weapon_list, 2)
        self.weapon_list = random.sample(research.equipment_list.weapon_list, 4)
        self.basic_ranged_weapon_list = random.sample(research.equipment_list.basic_ranged_weapon_list, 1)
        self.ranged_weapon_list = random.sample(research.equipment_list.ranged_weapon_list, 2)

        self.armor_list = random.sample(research.equipment_list.armor_list, 2)
        self.basic_armor_list = random.sample(research.equipment_list.basic_armor_list, 2)

        self.mount_list = random.sample(research.equipment_list.mount_list, 2)
        self.basic_mount_list = random.sample(research.equipment_list.basic_mount_list, 2)
        self.mount_none = research.equipment_list.mount_none

        self.army_structure = Troop.init_troop(self.language.make_word(self.language.name_length, True), self)

        self.tech = research.base_tech_tree()
        self.current_research = None

        self.tax_rate = random.random() * TAX_MULTIPLIER

        self.morale = 0

        self.army_spending = random.random() * 0.6 + 0.2
        self.elite = random.randint(3, 6)

        if len(self.cities) > 0:
            if random.randint(0, 2) == 0:
                place_name = self.cities[0].name
            else:
                place_name = self.language.make_name_word()
        else:
            place_name = self.language.make_name_word()

        self.name = language.NationName(random.sample(language.MODIFIERS, max(0, random.randint(0, 8) - 5)),
                                        random.choice(GOVERNMENT_TYPES), [place_name])
        # self.continent =

        # Otherwise we were initialized with some cities and such stuff
        if len(self.cities) == 0:
            for i in xrange(INIT_CITY_COUNT):
                self.create_city(self.name.places[0])

    # doesn't work at the moment
    def update_tree(self, troop):
        for t in self.troop_tree:
            if t.name == troop.name:
                self.troop_tree.remove(t)

        self.troop_tree.append(troop)

    def show_troop_tree_gui(self):
        self.gui_window = Tk()
        self.gui_window.title(self.name.short_name() + ' Troop Tree')
        self.gui_window.geometry("600x625+0+0")
        self.gui_window.config(background='white')

        self.gui_window.columnconfigure(5, weight=1)

        self.start_label = gui.Label(self.gui_window, text=self.name.short_name() + ' Troop Tree')
        self.start_label.grid(row=0, sticky=W)

        self.troops_display = Listbox(self.gui_window)
        self.troops_display.grid(row=1, sticky=N + S + E + W, columnspan=6)

        self.troops_display.delete(0, END)

        for troop in self.troop_tree:
            self.troops_display.insert(END, '-----------')
            name_text = 'Tier {} Troop: {} '.format(troop.tier, troop.name)

            # for i in xrange(troop.elite):
            #     name_text += '*'

            self.troops_display.insert(END, name_text)
            self.troops_display.insert(END, 'Stats: Health - {}, Strength - {}, Speed - {}, Discipline - {}'.format(
                troop.health, troop.strength, troop.speed, troop.discipline))
            self.troops_display.insert(END, 'Weapons: {} | {}, Armor: {}, Mount: {}'.format(troop.weapons[0].name,
                                                                                            troop.weapons[1].name,
                                                                                            troop.armor.name,
                                                                                            troop.mount.name))

            upgradeText = 'Upgrades: '

            for (i, upgrade) in enumerate(troop.upgrades):
                # print "upgrade"+ upgrade.name
                upgradeText += "Tier " + str(upgrade.tier) + ": " + upgrade.name + " | "

            self.troops_display.insert(END, upgradeText)

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title(self.name.short_name())
        self.gui_window.geometry("500x400+0+0")
        self.gui_window.config(background='white')

        self.gui_window.columnconfigure(5, weight=1)

        self.full_name = gui.Label(self.gui_window, text='Full name: {}'.format(self.name))
        self.full_name.grid(row=0, columnspan=6, sticky=W)

        self.age_label = gui.Label(self.gui_window, text='Age: {}'.format(self.age))
        self.age_label.grid(row=1, sticky=W)

        self.ruler_label = gui.Label(self.gui_window, text='Ruler: {}'.format(self.ruler))
        self.ruler_label.grid(row=2, columnspan=6, sticky=W)

        self.money_label = gui.Label(self.gui_window, text='Money: {}'.format(int(self.money)))
        self.money_label.grid(row=3, columnspan=2, sticky=W)

        self.morale_label = gui.Label(self.gui_window, text='Morale: {}'.format(self.morale))
        self.morale_label.grid(row=4, columnspan=2, sticky=W)

        self.religion_label = Label(self.gui_window, text='Main Religion: ')
        self.religion_label.grid(row=5, sticky=W)

        if self.main_religion is not None:
            self.religion_button = Button(self.gui_window, text=self.main_religion.name,
                                          command=self.main_religion.show_information_gui)
            self.religion_button.grid(row=5, column=1, sticky=W)
        else:
            self.religion_label = Label(self.gui_window, text='Religion: Secular')

        self.army_structure_button = gui.Button(self.gui_window, text='Army',
                                                command=self.army_structure.show_information_gui)
        self.army_structure_button.grid(row=6, column=0, sticky=W)

        self.culture_button = gui.Button(self.gui_window, text='Culture', command=self.culture.show_information_gui)
        self.culture_button.grid(row=6, column=1, sticky=W)

        self.army_structure_button = gui.Button(self.gui_window, text='Troop Tree', command=self.show_troop_tree_gui)
        self.army_structure_button.grid(row=6, column=2, sticky=W)

        self.display_selector_label = gui.Label(self.gui_window, text='Display:')
        self.display_selector_label.grid(row=7, sticky=W)

        self.event_display_button = gui.Button(self.gui_window, text='Events', command=self.display_events)
        self.event_display_button.grid(row=8, column=0, sticky=W)

        self.people_display_button = gui.Button(self.gui_window, text='People', command=self.display_people)
        self.people_display_button.grid(row=8, column=1, sticky=W)

        self.city_display_button = gui.Button(self.gui_window, text='Cities', command=self.display_cities)
        self.city_display_button.grid(row=8, column=2, sticky=W)

        self.trade_display_button = gui.Button(self.gui_window, text='Trade', command=self.display_trade)
        self.trade_display_button.grid(row=8, column=3, sticky=W)

        self.war_display_button = gui.Button(self.gui_window, text='War', command=self.display_war)
        self.war_display_button.grid(row=8, column=4, sticky=W)

        self.listbox_display = Listbox(self.gui_window)
        self.listbox_display.grid(row=9, sticky=E + W, columnspan=6)

        self.listbox_display.bind('<Double-Button-1>', self.selected)

    def save(self, path):
        self.parent.db.save_nation(self)
        self.parent.db.save_name(self.name)
        return

    def selected(self, event):
        if self.displaying == 'city':  # We can't select any other options
            selected_item = self.listbox_display.get(self.listbox_display.curselection())

            for city in self.cities:
                if str(city) == selected_item:
                    city.show_information_gui()

                    break
        elif self.displaying == 'people':
            selected_item = self.listbox_display.get(self.listbox_display.curselection())

            for person in self.notable_people:
                if str(person) == selected_item:
                    person.show_information_gui()

                    break
        elif self.displaying == 'trade' or self.displaying == 'war':
            selected_item = self.listbox_display.get(self.listbox_display.curselection())

            for nation in self.parent.nations:
                if str(nation) == selected_item:
                    nation.show_information_gui()

                    break

    def display_events(self):
        all_events = event_analysis.find_nation_mentions(self.id)
        all_events = all_events.search('name',
                                       r'NationFounded|TechResearch|CityFounded|CityMerged|Attack|DiplomacyWar|DiplomacyTrade|Revolt')
        all_events = sorted(all_events.event_list, key=lambda event: event.date)

        self.listbox_display.delete(0, END)
        for event in all_events:
            self.listbox_display.insert(END, event.text_version())

        self.displaying = 'event'

    def display_people(self):
        self.listbox_display.delete(0, END)
        for person in self.notable_people:
            if person.alive:  # Don't show all the dead people we keep stored away...
                self.listbox_display.insert(END, person)

        self.displaying = 'people'

    def display_war(self):
        self.listbox_display.delete(0, END)
        for warring in self.at_war:
            self.listbox_display.insert(END, warring)

        self.displaying = 'war'

    def display_trade(self):
        self.listbox_display.delete(0, END)
        for trade in self.trading:
            self.listbox_display.insert(END, trade)

        self.displaying = 'trade'

    def display_cities(self):
        self.listbox_display.delete(0, END)
        for city in self.cities:
            self.listbox_display.insert(END, city)

        self.displaying = 'city'

    def start_army_moves(self):
        for army in self.moving_armies:
            army.start_move()

    def do_army_moves(self):
        done = True
        for army in self.moving_armies:
            if not army.do_move():
                done = False

        return done

    def end_army_moves(self):
        for army in self.moving_armies:
            army.end_move()

    def total_army(self):
        for i in self.cities:
            if not i.army:
                i.army = self.army_structure.zero()

        return sum([city.army.size() for city in self.cities])

    def add_person(self, role=None):
        if len(self.cities) > 0:
            start_city = random.choice(self.cities)
            religion = start_city.get_random_religion()
            new_person = people.Person(self, start_city, self.language.generate_name(), religion, role=role)
            self.notable_people.append(new_person)

            return new_person

    def remove_population(self, amount):
        per_city = amount / len(self.cities)

        for city in self.cities:
            city.population -= per_city
            city.population = max(city.population, 1)

    def add_population(self, amount):
        per_city = amount / len(self.cities)

        for city in self.cities:
            city.population += per_city

    def get_tax_rate(self):
        multiplier = 1.0
        for person in self.notable_people:
            if person.periods[-1].role == 'administrator':
                multiplier *= person.effectiveness
        return self.tax_rate * multiplier

    def get_army_spending(self):
        return self.army_spending

    def get_population(self):
        return sum([i.population for i in self.cities])

    def get_improvements(self):
        return sum([i.improvements for i in self.cities])

    def get_average_city_position(self):
        if len(self.cities) == 0:
            return (random.randint(0, utility.S_WIDTH // utility.CELL_SIZE),
                    random.randint(0, utility.S_HEIGHT // utility.CELL_SIZE))

        x = 0
        y = 0

        for i in self.cities:
            cx, cy = i.position
            x += cx
            y += cy

        return (int(x / len(self.cities)), int(y / len(self.cities)))

    def get_unit(self, name):
        for i in self.army_structure:
            if i.name == name:
                return i

    def group_step(self):
        for city in self.cities:
            for caravan in city.caravans:
                caravan.step(None)

        for army in self.moving_armies:
            army.step(None)  # run the calculations but don't actually move yet

    def handle_people_monthly(self):
        if self.ruler is None or not self.ruler.alive:
            self.ruler = self.add_person()

        if random.randint(0, NOTABLE_PERSON_BIRTH_CHANCE) == 0:
            self.add_person()

        if self.ruler is not None:
            self.mod_morale(self.ruler.effectiveness ** 2)
            self.main_religion = self.ruler.religion

        for person in self.notable_people:
            person.handle_monthly()

    def grow_population(self):
        for city in self.cities:
            if not city.destroy:  # Don't simulate cities that are marked for destruction
                city.history_step()

        # Destroy cities if they been set to be destroyed.
        for city in self.cities:
            if city.destroy:
                city.destroy_self()  # This method removes the city from the city list, so we don't need to do it again

        # calculate net city morale, then use that to modify our own morale.
        total = 0
        for city in self.cities:
            total += city.morale
        if total != 0:
            if total < 0:
                self.mod_morale(-math.log(-total, 2))
            else:
                self.mod_morale(math.log(total, 2))

        self.handle_people_monthly()

    def move_armies(self, armies):
        for moving_army in self.moving_armies:
            moving_army.step(armies)

    def capture_city(self, other):
        self.chance_add_new_name(other.name)

    def chance_add_new_name(self, new_name):
        # Because we can't a place name twice
        if not new_name in self.name.places:
            roll = random.randint(0, self.get_tolerance())
            if roll > NAME_SWITCH_THRESHOLD:
                self.name.add_place(new_name)

    def get_city_candidate_cells(self):
        candidates = []

        for x in self.parent.cells:
            for y in x:
                if y.owner is None and y.terrain.is_settleable():
                    candidates.append(y)

        return candidates

    def create_city(self, name=''):
        if name == '':
            name = self.language.make_name_word()

        x, y = self.get_average_city_position()
        candidates = self.get_city_candidate_cells()
        candidate = utility.weighted_random_choice(candidates, lambda _, cell: 1.0 / (
                    utility.distance_squared((cell.x, cell.y), (x, y)) + 1.0))
        self.cities.append(city.City(self, name, candidate, self.parent))

        self.chance_add_new_name(self.cities[-1].name)

        self.parent.write_to_gen_log(
            "{}: A new city was founded in the nation of {}, called {}".format(self.parent.get_current_date(),
                                                                               self.name, self.cities[-1].name))
        self.parent.events.append(
            events.EventCityFounded('CityFounded', {'nation_a': self.id, 'city_a': self.cities[-1].name},
                                    self.parent.get_current_date()))

        self.cities[-1].army = self.army_structure.copy().zero()

        self.money -= CITY_FOUND_COST

        self.mod_morale(city.MORALE_INCREMENT)

        if self.parent.cells[self.cities[-1].position[0]][self.cities[-1].position[1]].owner is None:
            self.parent.change_cell_ownership(self.cities[-1].position[0], self.cities[-1].position[1], self.cities[-1],
                                              new_type='city')

        religion_populations = self.get_nation_religion_populations()

        if len(religion_populations) > 0:
            religion, _ = utility.weighted_random_choice(religion_populations, lambda i, (_, adherents): adherents)
            religion.adherents[self.cities[-1].name] = self.cities[-1].population

    def add_city(self, city):
        self.cities.append(city)

        city.nation = self

    def remove_city(self, city):
        self.cities.remove(city)

    def get_capital(self):
        for city in self.cities:
            if city.is_capital:
                return city

        return None

    def has_capital(self):
        for city in self.cities:
            if city.is_capital:
                return True
        return False

    def get_nation_religion_populations(self):
        res = {}
        for religion in self.parent.religions:
            for city_name in religion.adherents:
                if city_name in map(lambda i: i.name, self.cities):
                    if not religion in res:
                        res[religion] = religion.adherents[city_name]
                    else:
                        res[religion] += religion.adherents[city_name]

        return res.items()

    # Tolerance is a weighted average of the tolerances of the religions that make up this nation.
    def get_tolerance(self):
        val = 0
        religion_populations = self.get_nation_religion_populations()
        final = {}
        total = self.get_population()

        if total > 0:
            for (religion, adherents) in religion_populations:
                final[religion] = float(adherents) / total

        for (religion, p) in final.iteritems():
            val += religion.get_tolerance() * p

        for person in self.notable_people:
            if person.alive and not person == self.ruler:
                if person.periods[-1].role == 'priest':
                    # Priests can either make the nation more or less tolerant, depending
                    amount = (1 - person.effectiveness) * PRIEST_TOLERANCE_BONUS

                    val += amount

                if person.periods[-1].role == 'bishop':
                    # Priests can either make the nation more or less tolerant, depending
                    amount = (1 - person.effectiveness) * (PRIEST_TOLERANCE_BONUS * 2)

                    val += amount

                if person.periods[-1].role == 'prophet':
                    # Priests can either make the nation more or less tolerant, depending
                    amount = (1 - person.effectiveness) * (PRIEST_TOLERANCE_BONUS * 3)

                    val += amount

        val = int(self.get_tolerance_bonus() * val)
        return max(1, val)

    def get_tolerance_bonus(self):
        return GOVERNMENT_TYPE_BONUSES[self.name.government_type]['tolerance']

    def get_resource_bonus(self, resource):
        if resource in GOVERNMENT_TYPE_BONUSES[self.name.government_type]:
            return GOVERNMENT_TYPE_BONUSES[self.name.government_type][resource]
        else:
            return 1.0

    def get_efficiency_bonus(self):
        return GOVERNMENT_TYPE_BONUSES[self.name.government_type]['efficiency']

    def get_morale_bonus(self):
        return GOVERNMENT_TYPE_BONUSES[self.name.government_type]['morale']

    def get_conscription_bonus(self):
        return GOVERNMENT_TYPE_BONUSES[self.name.government_type]['conscription']

    def get_soldier_cost(self, troop):
        amount = SOLDIER_RECRUIT_COST

        for weapon in troop.weapons:
            amount += weapon.cost

        amount += troop.armor.cost

        amount += troop.mount.cost

        # print('{} ({},{},{}) costs {}'.format(troop.name, troop.tier, troop.weapons, troop.armor, amount))

        return amount

    def get_soldier_upkeep(self, troop):
        return SOLDIER_UPKEEP

    def mod_morale(self, amount):
        if amount > 0:
            amount = amount * self.get_morale_bonus()
        else:
            amount = amount / self.get_morale_bonus()

        self.morale = int(self.morale + amount * self.get_morale_bonus())

    def handle_rearming(self):
        if random.randint(0, 100) < REARM_CHANCE:
            units = self.army_structure.make_upgrade_list()

            rearm_unit = random.choice(units)
            rearm_unit.do_rearm(self)

            weapon_string = ', '.join(map(lambda w: w.name, rearm_unit.weapons))
            e = events.EventRearmUnit('RearmUnit',
                                      {'nation_a': self.id, 'unit_a': rearm_unit.name, 'weapons': weapon_string,
                                       'armor': rearm_unit.armor.name}, self.parent.get_current_date())
            self.parent.events.append(e)

            self.parent.write_to_gen_log(self.parent.events[-1].text_version())

            for city in self.cities:
                city.rearm_army(rearm_unit)

    def handle_people(self):
        for person in self.notable_people:
            was_alive = person.alive
            person.history_step()

            # Only do it once.
            if not person.alive and was_alive:
                person.handle_death()

    def history_step(self):
        self.name.history_step(self)

        # we lost our capital somehow
        if not self.has_capital():
            # choose a new capital from our cities, weighted by population
            if len(self.cities) > 0:  # Just to be sure
                new_capital = utility.weighted_random_choice(self.cities, weight=lambda i, v: v.population)

                new_capital.make_capital()
        else:
            self.mod_morale(city.CAPITAL_CITY_MORALE_BONUS)

        self.handle_treaties()

        for curCity in self.cities:
            # It's more likely to found a new city when this city is near population capacity
            # Because as there's no more space, people want to go to a new city
            try:
                found_city_chance = max(1, int(
                    len(self.cities) ** 4 * math.math.log(curCity.population_capacity - curCity.population)))
            except:  # Log is negative
                found_city_chance = max(1, len(self.cities) ** 4)
            if random.randint(0, found_city_chance) == 0 and self.money > CITY_FOUND_COST:
                self.create_city()

            if self.current_research is None or self.current_research.is_unlocked():
                if self.current_research is not None and self.current_research.is_unlocked():
                    self.parent.events.append(events.EventTechResearch('TechResearch', {'nation_a': self.id,
                                                                                        'tech_a': self.current_research.name},
                                                                       self.parent.get_current_date()))

                    self.parent.write_to_gen_log(self.parent.events[-1].text_version())
                available = self.tech.get_available_research()

                if len(available) > 0:
                    self.current_research = random.choice(available)
                else:  # There's nothing left to research
                    self.current_research = None
            else:
                self.current_research.do_research(random.randint(1, int(math.log(curCity.population + 1) ** 2 + 1)))

                for cell in curCity.cells:
                    for building in cell.buildings:
                        research_rate = building.get_research_rate()

                        if research_rate > 0:
                            self.current_research.do_research(random.randint(1, research_rate))

        self.handle_rearming()
        self.handle_people()

        self.age += 1

        # More cities means less happiness
        self.mod_morale(-(len(self.cities) ** 2 + 1))

    def handle_revolt(self):
        # Not for realism, but this really shouldn't happen, because then they'd be sharing colors.
        if len(self.parent.available_colors()) > 0:
            # Need more than one city to revolt.
            if len(self.cities) > 1:
                if random.randint(0, max(1, 50 + self.morale)) == 0:
                    revolted_cities = []
                    for city in self.cities:
                        # Not all cities can revolt
                        if random.randint(0, max(1, int(city.morale))) == 0 and len(self.cities) > 1:
                            revolted_cities.append(city)
                            self.remove_city(city)

                    # At least one city has to revolt, we already decided a revolt was happening, dammit!
                    if len(revolted_cities) == 0:
                        min_morale = self.cities[0].morale
                        lowest_morale = self.cities[0]
                        for city in self.cities:
                            if city.morale < min_morale:
                                min_morale = city.morale
                                lowest_morale = city
                        revolted_cities.append(lowest_morale)
                        self.remove_city(lowest_morale)

                    self.parent.add_nation(Nation(self.parent, revolted_cities))

                    # For readability
                    revolted_nation = self.parent.nations[-1]

                    # The actual army revolts are just the armies in the revolting cities
                    revolted_nation.army_structure = self.army_structure.reset()
                    revolted_nation.language = language.Language(base_language=self.language)

                    # Copy weapon choices over
                    # We don't want a shallow copy because they shouldn't share research
                    revolted_nation.sidearm_list = list(self.sidearm_list)
                    revolted_nation.basic_weapon_list = list(self.basic_weapon_list)
                    revolted_nation.weapon_list = list(self.weapon_list)
                    revolted_nation.basic_ranged_weapon_list = list(self.basic_ranged_weapon_list)
                    revolted_nation.ranged_weapon_list = list(self.ranged_weapon_list)
                    revolted_nation.armor_list = list(self.armor_list)
                    revolted_nation.basic_armor_list = list(self.basic_armor_list)

                    army_revolted = sum([city.army.size() for city in revolted_nation.cities])

                    # The revolting nation increases their morale because they're now free from whatever issues they saw with the old regime
                    revolted_nation.mod_morale(
                        city.MORALE_INCREMENT * len(revolted_cities) * int(math.log(army_revolted + 2)))

                    # The old nation increases their morale because the haters are now gone.
                    self.mod_morale(len(revolted_cities) * city.MORALE_INCREMENT * int(
                        math.log(sum([city.army.size() for city in self.cities]) + 2)))

                    self.parent.write_to_gen_log('{}:'.format(self.parent.get_current_date()))
                    self.parent.write_to_gen_log(
                        "There was a revolt in the nation of {}, resulting in the creation of the new nation state of {}.".format(
                            self.name, revolted_nation.name))
                    self.parent.write_to_gen_log(
                        "The following cities joined the revolt, along with {} soldiers: {}".format(army_revolted,
                                                                                                    revolted_nation.cities))

                    self.parent.events.append(events.EventRevolt('Revolt',
                                                                 {'nation_a': self.id, 'nation_b': revolted_nation.id,
                                                                  'cities': [city.name for city in
                                                                             revolted_nation.cities]},
                                                                 self.parent.get_current_date()))

                    # We don't have peaceful revolts, naturally a nation would attempt to put down the revolt.
                    self.parent.start_war(self, revolted_nation)

    def handle_army_dispatch(self):
        # Determine if we want to launch an attack with this city's army
        for city in self.cities:
            if len(self.at_war) > 0 and city.army.size() > 0:
                enemy = random.choice(self.at_war)

                # Make sure our enemy actually still exists.
                if len(enemy.cities) > 0 and enemy in self.parent.nations:
                    attacking_city = utility.weighted_random_choice(enemy.cities,
                                                                    weight=lambda _, v: 1.0 / utility.distance(
                                                                        city.position, v.position))

                    if random.randint(0, max(20,
                                             city.army.size() + city.population // 8 - attacking_city.population // 3 - attacking_city.army.size())) > 20:
                        if random.randint(0, len(self.moving_armies) ** 3) == 0:
                            fx, fy = city.position

                            dx, dy = attacking_city.position

                            # Conscript some levies to join the army.
                            if city.population // 3 > 1:
                                conscript_max = max(city.population // 4, 3)
                                conscript_min = min(city.population // 8, 2)
                                conscripted = int(
                                    random.randint(conscript_min, conscript_max) * self.get_conscription_bonus())
                            else:
                                conscripted = 0

                            city.population -= conscripted
                            city.army.add_to(city.army.name, conscripted)

                            action = self.parent.do_attack(self, city, enemy, attacking_city)

                            self.moving_armies.append(
                                group.Group(self.parent, self.id, city.army, (fx, fy), (dx, dy), self.color, lambda s: False,
                                            action, self.parent.canvas, is_army=True, has_boat=(city.resources['boats'] > 0)))

                            self.parent.events.append(events.EventArmyDispatched('ArmyDispatched', {'nation_a': self.id,
                                                                                                    'nation_b': enemy.id,
                                                                                                    'city_a': city.name,
                                                                                                    'city_b': attacking_city.name,
                                                                                                    'reason': 'attack',
                                                                                                    'army_size': city.army.size()},
                                                                                 self.parent.get_current_date()))

                            city.army = city.army.zero()

    def handle_treaties(self):
        for treaty in self.treaties:
            treaty.history_step(self, self.parent.get_current_date())

    def get_current_treaties_with(self, nation):
        current_treaties = filter(lambda treaty: treaty.is_current, self.treaties)

        return filter(lambda treaty: treaty.nation_a == nation or treaty.nation_b == nation, current_treaties)

    def get_treaty_with(self, nation, treaty_type):
        # First check for current treaties
        for treaty in self.treaties:
            if treaty.is_current:
                if treaty.nation_a == nation or treaty.nation_b == nation:
                    if treaty.treaty_type == treaty_type:
                        return treaty

        # Now for not current ones
        for treaty in self.treaties:
            if treaty.nation_a == nation or treaty.nation_b == nation:
                if treaty.treaty_type == treaty_type:
                    return treaty

        return None

    def handle_relations(self):
        for nation in self.parent.nations:
            if nation != self:
                if nation in self.trading:
                    trade_treaty = self.get_treaty_with(nation, 'trade')

                    if trade_treaty is not None:
                        self.relations[nation.id] += trade_treaty[self.id]['caravans_received'] / trade_treaty.length(
                            self.parent.get_current_date())

                if nation in self.at_war:
                    war_treaty = self.get_treaty_with(nation, 'war')

                    if war_treaty is not None:
                        # This way, if we lose more troops than them, our relations will go down even more, even though they go down by default just for being at war

                        relative_troops_lost = min(-1, war_treaty[nation.id]['troops_lost'] - war_treaty[self.id][
                            'troops_lost'])

                        self.relations[nation.id] += relative_troops_lost / war_treaty.length(
                            self.parent.get_current_date())

                max_relation_change = int(math.log(self.get_tolerance() + nation.get_tolerance() + 1))

                self.relations[nation.id] += random.randint(-max_relation_change // 2, max_relation_change // 2)

                self.relations[nation.id] = min(100, max(-100, self.relations[nation.id]))

                # Relations are the same both ways.
                nation.relations[self.id] = self.relations[nation.id]

        # print('{}\'s Relations:'.format(self.name))
        # for nation in self.relations:
        #     print('\t{}: {}'.format(events.get_nation_name(nation), self.relations[nation]))

    def handle_diplomacy(self):
        # We can only start warring/trading if there are nations other than us.
        if len(self.parent.nations) > 1:
            distance_sorted_nations = sorted(self.parent.nations,
                                             key=lambda nation: utility.distance(self.get_average_city_position(),
                                                                                 nation.get_average_city_position()))

            # Check for war/trade
            for other in distance_sorted_nations:
                # We can't start trading with an enemy we're at war with or vice versa.
                # And we certainly can't start fighting/trading with ourselves.
                if other != self and not other in self.at_war and not other in self.trading:
                    normal_war_chance = int(
                        max(24, len(self.at_war) + 2 * self.get_tolerance() + 3 * self.relations[other.id]))
                    holy_war_chance = int(
                        max(12, len(self.at_war) + self.get_tolerance() + 3 * self.relations[other.id]))

                    effective_money = max(self.money ** 2, 1)  # The less money we have, the more we want to trade.
                    trade_chance = int(
                        max(24, math.log(effective_money) + self.get_tolerance() - 3 * self.relations[other.id]))

                    # print('War chance with {} ({}) is {}'.format(other.name.short_name(), self.relations[other.id], normal_war_chance))
                    # print('Holy war chance with {} ({}) is {}'.format(other.name.short_name(), self.relations[other.id], holy_war_chance))
                    # print('Trade chance with {} ({}) is {}'.format(other.name.short_name(), self.relations[other.id], trade_chance))

                    if random.randint(0, normal_war_chance) == 0:
                        # print('Declaring war on nation with which out relations are {}'.format(self.relations[other.id]))
                        self.parent.start_war(self, other)
                        break
                    # elif other.religion != self.religion and random.randint(0, holy_war_chance) == 0:
                    #     # print('Declaring a holy war on nation with which out relations are {}'.format(self.relations[other.id]))
                    #     self.parent.start_war(self, other, is_holy_war=True)
                    #     break
                    elif random.randint(0, trade_chance) == 0:
                        # print('Starting trade with a nation with which out relations are {}'.format(self.relations[other.id]))
                        self.parent.start_trade_agreement(self, other)
                        break

        self.remove_dead_nations()
        self.handle_army_dispatch()
        self.handle_revolt()
        self.handle_relations()

    def remove_dead_nations(self):
        for nation in self.trading:
            if not nation in self.parent.nations:
                for treaty in self.get_current_treaties_with(nation):
                    treaty.end(self.parent.get_current_date())

                self.relations.pop(nation.id)

    def __repr__(self):
        return '{} ({}): ${}; Pop: {}'.format(self.name.short_name(), self.color, int(self.money),
                                              sum([i.population for i in self.cities]))
