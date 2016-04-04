import utility

from city import *
from martial import *
from language import *
from group import *
from religion import *
from research import *

import events
import event_analysis

import random

from math import *

from Tkinter import *

OFFICE_MORALE_BONUS = 4

NATION_COLORS = ['dark orange', 'cadet blue', 'sea green', 'gold', 'deep sky blue',\
                 'firebrick', 'dark salmon', 'maroon', 'sienna', 'dark slate blue',\
                 'deep pink', 'dark orchid', 'slate gray', 'violet',\
                 'navy', 'magenta', 'sandy brown', 'saddle brown', \
                 'orchid', 'blue', 'violet red',\
                 'medium slate blue', 'purple', 'blue violet',\
                 'dark sea green', 'hot pink', 'orange', 'indian red', \
                 'red', 'brown', 'dim gray', 'salmon',\
                 'steel blue', 'royal blue', 'medium purple', \
                 'dark slate gray', 'dark olive green', 'cyan', 'chocolate', 'orange red', \
                 'tomato', 'gray', 'cornflower blue', 'goldenrod', \
                 'midnight blue', 'rosy brown', 'plum', 'sky blue',\
                 'dark violet', 'dark khaki', 'olive drab', 'medium turquoise',\
                 'slate blue', 'powder blue', 'aquamarine']

OFFICE_MODIFIERS = ['tax_rate', 'army_spending', 'morale']
OFFICE_MODIFIER_MAX = 2

MODIFIERS = ["Grand", "Federated", "Democratic", "People's", "Free", "Illustrious", "Glorious", "United"]
GOVERNMENT_TYPES = ["Principality", "Commonwealth", "Kingdom", "Hegemony", "Khanate", "Socialist State", "Sultanate", "Republic", "Democracy", "Theocracy", "Confederacy", "Oligarchy", "Aristocracy", "Meritocracy", "States"]
INIT_CITY_COUNT = 1

CITY_FOUND_COST = 100000
SOLDIER_RECRUIT_COST = 2000
SOLDIER_UPKEEP = 200

REARM_CHANCE = 5

TAX_MULTIPLIER = 1

AVERAGE_MAX_LIFE_EXPECTANCY = 60

NAME_SWITCH_THRESHOLD = 30

#Years
MIN_TERM_LENGTH = 5
MAX_TERM_LENGTH = 20

#Chances (1 in x)
LOSE_PLACE_CITY_NAME = 8 #Only applies if the nation no longer owns the city.
LOSE_NAME_MODIFIER = 30 #Per modifier
GAIN_NAME_MODIFIER = 30 #Per history step

GOVERNMENT_TYPE_BONUSES = {}
GOVERNMENT_TYPE_BONUSES["Principality"] = {'food': 1, 'morale': 0.75, 'efficiency': 1, 'tolerance': 1, 'conscription': 1.5}
GOVERNMENT_TYPE_BONUSES["Kingdom"] = {'food': 1, 'morale': 0.75, 'efficiency': 1, 'tolerance': 1, 'conscription': 1.5}
GOVERNMENT_TYPE_BONUSES["Sultanate"] = {'food': 1, 'morale': 0.75, 'efficiency': 1, 'tolerance': 1, 'conscription': 1.5}
GOVERNMENT_TYPE_BONUSES["Khanate"] = {'food': 1, 'morale': 0.75, 'efficiency': 1, 'tolerance': 1, 'conscription': 1.5}
GOVERNMENT_TYPE_BONUSES["Socialist State"] = {'food': 2, 'morale': 0.5, 'efficiency': 1, 'tolerance': 1, 'conscription': 1}
GOVERNMENT_TYPE_BONUSES["States"] = {'food': 1, 'morale': 1, 'efficiency': 1, 'tolerance': 1, 'conscription': 1}
GOVERNMENT_TYPE_BONUSES["Commonwealth"] = {'food': 1, 'morale': 1, 'efficiency': 1, 'tolerance': 1, 'conscription': 1}
GOVERNMENT_TYPE_BONUSES["Democracy"] = {'food': 1, 'morale': 2, 'efficiency': 0.75, 'tolerance': 1, 'conscription': 1}
GOVERNMENT_TYPE_BONUSES["Republic"] = {'food': 1, 'morale': 1.5, 'efficiency': 1, 'tolerance': 1, 'conscription': 1}
GOVERNMENT_TYPE_BONUSES["Theocracy"] = {'food': 1, 'morale': 1.5, 'efficiency': 1, 'tolerance': 0.5, 'conscription': 1}
GOVERNMENT_TYPE_BONUSES["Confederacy"] = {'food': 1, 'morale': 1.5, 'efficiency': 0.75, 'tolerance': 1, 'conscription': 1}
GOVERNMENT_TYPE_BONUSES["Meritocracy"] = {'food': 1, 'morale': 0.75, 'efficiency': 2, 'tolerance': 1, 'conscription': 1}
GOVERNMENT_TYPE_BONUSES["Aristocracy"] = {'food': 1, 'morale': 1, 'efficiency': 0.75, 'tolerance': 1, 'conscription': 1.5}
GOVERNMENT_TYPE_BONUSES["Oligarchy"] = {'food': 1, 'morale': 1, 'efficiency': 0.75, 'tolerance': 1, 'conscription': 1.5}
GOVERNMENT_TYPE_BONUSES["Hegemony"] = {'food': 1, 'morale': 0.5, 'efficiency': 1, 'tolerance': 1, 'conscription': 2}

class Person:
    def __init__(self, name):
        self.name = name

        self.age = 1

        self.effectiveness = random.random() * 2

        self.alive = True

        self.offices = []

    def get_effectiveness(self):
        return self.effectiveness

    def add_office(self, office):
        self.offices.append(office)

    def remove_office(self, office):
        self.offices.remove(office)

    def handle_death(self):
        for office in self.offices:
            office.handle_death(self)

    def history_step(self):
        self.age += 1

        if random.randint(0, AVERAGE_MAX_LIFE_EXPECTANCY) == 0: #The person died
            self.alive = False

    def __repr__(self):
        return "{}({})".format(self.name, self.age)

class Office:
    def __init__(self, nation):
        self.nation = nation
        self.language = self.nation.language
        self.name = self.language.make_word(self.language.name_length, True)

        self.holder = Person(self.language.generate_name())

        self.modifiers = {}

        for modifier in OFFICE_MODIFIERS:
            self.modifiers[modifier] = random.random() * OFFICE_MODIFIER_MAX

        self.term_length = random.randint(MIN_TERM_LENGTH, MAX_TERM_LENGTH)
        self.current_term = 0

        self.age = 0

    def get_modifier(self, modifier):
        return self.modifiers[modifier] * self.holder.get_effectiveness() * self.nation.get_efficiency_bonus()

    def fill_office(self):
        self.current_term = 0

        self.holder = self.nation.get_qualified_person(self)
        self.holder.add_office(self)

    def handle_death(self, person):
        self.fill_office()

    def history_step(self, parent):
        self.age += 1

        self.current_term += 1
        if self.current_term == self.term_length:
            self.fill_office()

    def __repr__(self):
        return "{}: {}: [{}]".format(self.name, self.holder, self.modifiers)

class NationName:
    def __init__(self, modifiers, government_type, places):
        self.modifiers = modifiers
        self.government_type = government_type
        self.places = places

    def history_step(self, parent):
        parent_cities_names = map(lambda city: city.name, parent.cities)

        for place in self.places:
            #We can't get rid of the last one.
            if not place in parent_cities_names and len(self.places) > 1:
                if random.randint(0, LOSE_PLACE_CITY_NAME) == 0:
                    self.remove_place(place)

        for modifier in self.modifiers:
            if random.randint(0, LOSE_NAME_MODIFIER) == 0:
                self.remove_modifier(modifier)

        if random.randint(0, GAIN_NAME_MODIFIER) == 0:
            self.add_modifier(random.choice(MODIFIERS))

    def add_modifier(self, modifier_name):
        self.modifiers.append(modifier_name)

    def remove_modifier(self, modifier_name):
        self.modifiers.remove(modifier_name)

    def add_place(self, place_name):
        self.places.append(place_name)

    def remove_place(self, place_name):
        self.places.remove(place_name)

    def short_name(self):
        return self.places[0]

    def get_name(self):
        modifier_part = ' '.join(self.modifiers)

        if len(self.places) > 2:
            place_part = '{}, and {}'.format(', '.join(self.places[:-1]), self.places[-1])
        elif len(self.places) == 2:
            place_part = '{} and {}'.format(self.places[0], self.places[1])
        else:
            place_part = self.places[0]

        if len(self.modifiers) > 0:
            return 'The {} {} of {}'.format(modifier_part, self.government_type, place_part)
        else:
            return 'The {} of {}'.format(self.government_type, place_part)

    def __repr__(self):
        return self.get_name()

class Nation:
    def __init__(self, parent, cities=None):
        self.language = Language() #Create a new, random language

        self.age = 0

        self.parent = parent

        #Take a color that hasn't already been used.
        self.color = random.choice(parent.available_colors())

        CELLS_WIDTH = utility.S_WIDTH // utility.CELL_SIZE
        CELLS_HEIGHT = utility.S_WIDTH // utility.CELL_SIZE
        x = random.randint(int(CELLS_WIDTH * 0.1), int(CELLS_WIDTH * 0.9))
        y = random.randint(int(CELLS_HEIGHT * 0.1), int(CELLS_HEIGHT * 0.9))

        if cities != None:
            self.cities = cities

            for city in self.cities:
                city.nation = self
        else:
            self.cities = []

        self.money = 0

        self.id = parent.get_next_id()

        self.offices = [Office(self) for i in xrange(2)]

        self.people = []

        self.at_war = []
        self.allied = []
        self.trading = []

        self.caravans = []

        self.moving_armies = []

        self.sidearm_list = random.sample(sidearm_list, 3)
        self.basic_weapon_list = random.sample(basic_weapon_list, 2)
        self.weapon_list = random.sample(weapon_list, 4)
        self.basic_ranged_weapon_list = random.sample(basic_ranged_weapon_list, 1)
        self.ranged_weapon_list = random.sample(ranged_weapon_list, 2)

        self.armor_list = random.sample(armor_list, 2)
        self.basic_armor_list = random.sample(basic_armor_list, 2)

        self.army_structure = Troop.init_troop(self.language.make_word(self.language.name_length, True), self)

        self.tech = base_tech_tree()
        self.current_research = None

        self.tax_rate = random.random() * TAX_MULTIPLIER

        self.morale = MORALE_INCREMENT * 4

        self.army_spending = random.random()

        self.elite = random.randint(2, 10)

        self.religion = Religion(self.language, self.language.make_name_word())

        if len(self.cities) > 0:
            place_name = self.cities[0].name
        else:
            place_name = self.language.make_name_word()

        self.name = NationName(random.sample(MODIFIERS, max(0, random.randint(0, 8) - 5)), random.choice(GOVERNMENT_TYPES), [place_name])

        #Otherwise we were initialized with some cities and such stuff
        if len(self.cities) == 0:
            for i in xrange(INIT_CITY_COUNT):
                self.create_city(self.name.places[0])

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title(self.name.short_name())
        self.gui_window.geometry("500x375+0+0")

        self.gui_window.columnconfigure(5, weight=1)

        self.full_name = Label(self.gui_window, text='Full name: {}'.format(self.name))
        self.full_name.grid(row=0, columnspan=6, sticky=W)

        self.age_label = Label(self.gui_window, text='Age: {}'.format(self.age))
        self.age_label.grid(row=1, sticky=W)

        self.money_label = Label(self.gui_window, text='Money: {}'.format(int(self.money)))
        self.money_label.grid(row=2, sticky=W)

        self.morale_label = Label(self.gui_window, text='Morale: {}'.format(self.morale))
        self.morale_label.grid(row=3, sticky=W)

        self.religion_label = Label(self.gui_window, text='Religion: ')
        self.religion_label.grid(row=4, sticky=W)

        self.religion_button = Button(self.gui_window, text=self.religion.name, command=self.religion.show_information_gui)
        self.religion_button.grid(row=4, column=1, sticky=W)

        self.army_structure_button = Button(self.gui_window, text='Army', command=self.army_structure.show_information_gui)
        self.army_structure_button.grid(row=5, sticky=W)

        self.display_selector_label = Label(self.gui_window, text='Display:')
        self.display_selector_label.grid(row=6, sticky=W)

        self.event_display_button = Button(self.gui_window, text='Events', command=self.display_events)
        self.event_display_button.grid(row=7, column=0, sticky=W)

        self.office_display_button = Button(self.gui_window, text='Offices', command=self.display_offices)
        self.office_display_button.grid(row=7, column=1, sticky=W)

        self.city_display_button = Button(self.gui_window, text='Cities', command=self.display_cities)
        self.city_display_button.grid(row=7, column=2, sticky=W)

        self.trade_display_button = Button(self.gui_window, text='Trade', command=self.display_trade)
        self.trade_display_button.grid(row=7, column=3, sticky=W)

        self.war_display_button = Button(self.gui_window, text='War', command=self.display_war)
        self.war_display_button.grid(row=7, column=4, sticky=W)

        self.listbox_display = Listbox(self.gui_window)
        self.listbox_display.grid(row=8, sticky=E + W, columnspan=6)

        self.listbox_display.bind('<Double-Button-1>', self.selected)

        self.displaying = ''

    def selected(self, event):
        if self.displaying == 'city': #We can't select any other options
            selected_item = self.listbox_display.get(self.listbox_display.curselection())

            for city in self.cities:
                if str(city) == selected_item:
                    city.show_information_gui()

                    break
        elif self.displaying == 'trade' or self.displaying == 'war':
            selected_item = self.listbox_display.get(self.listbox_display.curselection())

            for nation in self.parent.nations:
                if str(nation) == selected_item:
                    nation.show_information_gui()

                    break

    def display_events(self):
        all_events = event_analysis.find_nation_mentions(self.id)
        all_events = all_events.search('name', r'NationFounded|TechResearch|CityFounded|CityMerged|Attack|DiplomacyWar|DiplomacyTrade|Revolt')
        all_events = sorted(all_events.event_list, key=lambda event: event.date)

        self.listbox_display.delete(0, END)
        for event in all_events:
            self.listbox_display.insert(END, event.text_version())

        self.displaying = 'event'

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

    def display_offices(self):
        self.listbox_display.delete(0, END)
        for office in self.offices:
            self.listbox_display.insert(END, office)

        self.displaying = 'office'

    def display_cities(self):
        self.listbox_display.delete(0, END)
        for city in self.cities:
            self.listbox_display.insert(END, city)

        self.displaying = 'city'

    def total_army(self):
        for i in self.cities:
            if not i.army:
                i.army = self.army_structure.zero()

        return sum([city.army.size() for city in self.cities])

    def get_qualified_person(self, office):
        self.add_person() #So the first office isn't always filled by the same person.
        qualified_people = []

        for person in self.people:
            #Right now the only necessary qualification is that the same person can't hold the same office twice at the same time
            if not office in person.offices:
                qualified_people.append(person)

        if len(qualified_people) == 0:
            return self.add_person()
        else:
            return random.choice(qualified_people)

    def add_person(self):
        new_person = Person(self.language.make_name_word())
        self.people.append(new_person)

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
        # print(self.tax_rate, utility.product([office.get_modifier('tax_rate') for office in self.offices]))
        return self.tax_rate * utility.product([office.get_modifier('tax_rate') for office in self.offices])

    def get_army_spending(self):
        return min(1, self.army_spending * utility.product([office.get_modifier('army_spending') for office in self.offices]))

    def get_population(self):
        return sum([i.population for i in self.cities])

    def get_improvements(self):
        return sum([i.improvements for i in self.cities])

    def get_average_city_position(self):
        if len(self.cities) == 0:
            return (random.randint(0, utility.S_WIDTH // utility.CELL_SIZE), random.randint(0, utility.S_HEIGHT // utility.CELL_SIZE))

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

    def receive_caravan(self, nation):
        def f(caravan):
            nation.caravans.remove(caravan)

            #More money if we traded with somebody else
            if nation != self:
                nation.money += 2000

                self.money += 2000
            else:
                self.money += 1000

        return f

    def group_step(self):
        for caravan in self.caravans:
            caravan.step(self.caravans)

    def grow_population(self):
        for city in self.cities:
            if not city.destroy: #Don't simulate cities that are marked for destruction
                city.history_step()

                if random.randint(0, 20) == 0: #Send a caravan
                    cx, cy = city.position

                    if random.randint(0, 2) < 2: #Send to one of our cities
                        trade_city = random.choice(self.cities)
                        dx, dy = trade_city.position #Send it to a random city

                        self.caravans.append(Group("caravan", [], (cx, cy), (dx, dy), self.color, lambda s, g: False, self.receive_caravan(self), self.parent.canvas))
                    elif len(self.trading) > 0: #We have trading partners to trade with
                        partner = random.choice(self.trading)

                        if len(partner.cities) > 0:
                            trade_city = random.choice(partner.cities)
                            dx, dy = trade_city.position #Send it to a random city

                            self.caravans.append(Group("caravan", [], (cx, cy), (dx, dy), self.color, lambda s, g: False, partner.receive_caravan(self), self.parent.canvas))

        #Destroy cities if they been set to be destroyed.
        for city in self.cities:
            if city.destroy:
                city.destroy_self() #This method removes the city from the city list, so we don't need to do it again

    def move_armies(self, armies):
        for moving_army in self.moving_armies:
            moving_army.step(armies)

    def capture_city(self, other):
        self.chance_add_new_name(other.name)

    def chance_add_new_name(self, new_name):
        #Because we can't a place name twice
        if not new_name in self.name.places:
            roll = random.randint(0, self.get_tolerance())
            if roll > NAME_SWITCH_THRESHOLD:
                self.name.add_place(new_name)

    def get_city_candidate_cells(self):
        candidates = []

        for x in self.parent.cells:
            for y in x:
                if y.owner == None and y.terrain.is_settleable():
                    candidates.append(y)

        return candidates

    def create_city(self, name=''):
        if name == '':
            name = self.language.make_name_word()

        x, y = self.get_average_city_position()
        candidates = self.get_city_candidate_cells()
        candidate = utility.weighted_random_choice(candidates, lambda _,cell: utility.distance_squared((cell.x, cell.y), (x, y)))
        self.cities.append(City(self, name, candidate, self.parent))

        self.chance_add_new_name(self.cities[-1].name)

        print("{}: A new city was founded in the nation of {}, called {}".format(self.parent.get_current_date(), self.name, self.cities[-1].name))
        self.parent.events.append(events.EventCityFounded('CityFounded', {'nation_a': self.id, 'city_a': self.cities[-1].name}, self.parent.get_current_date()))

        self.cities[-1].army = self.army_structure.copy().zero()

        self.money -= CITY_FOUND_COST

        self.mod_morale(MORALE_INCREMENT)

        if self.parent.cells[self.cities[-1].position[0]][self.cities[-1].position[1]].owner == None:
            self.parent.change_cell_ownership(self.cities[-1].position[0], self.cities[-1].position[1], self.cities[-1], new_type='city')

    def add_city(self, city):
        self.cities.append(city)

        city.nation = self

    def remove_city(self, city):
        self.cities.remove(city)

    def has_capital(self):
        for city in self.cities:
            if city.is_capital:
                return True
        return False

    def get_tolerance(self):
        return int(self.religion.get_tolerance() * self.get_tolerance_bonus())

    def get_tolerance_bonus(self):
        return GOVERNMENT_TYPE_BONUSES[self.name.government_type]['tolerance']

    def get_resource_bonus(self, resource):
        if resource == 'food':
            mult_mod = 1.0
            add_mod = 0.0
            res = self.tech.get_tech('Improved Agriculture')
            if res != None:
                mult_mod *= res.effect_strength
            return GOVERNMENT_TYPE_BONUSES[self.name.government_type]['food'] * mult_mod + add_mod
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

            weapon_string = ','.join(map(lambda w: w.name, rearm_unit.weapons))
            e = events.EventRearmUnit('RearmUnit', {'nation_a': self.id, 'unit_a': rearm_unit.name, 'weapons': weapon_string, 'armor': rearm_unit.armor.name}, self.parent.get_current_date())
            self.parent.events.append(e)

            print(self.parent.events[-1].text_version())

            for city in self.cities:
                city.rearm_army(rearm_unit)

    def history_step(self):
        self.name.history_step(self)

        for person in self.people:
            person.history_step()

            if not person.alive:
                person.handle_death()

        #Remove old, redundant offices
        for office in self.offices:
            office.history_step(self)

            if random.randint(0, office.age) > 10:
                self.offices.remove(office)

            if random.randint(0, len(self.offices)**3) == 0:
                self.offices.append(Office(self))

        #we lost our capital somehow
        if not self.has_capital():
            #choose a new capital from our cities, utility.weighted by population
            if len(self.cities) > 0: #Just to be sure
                new_capital = utility.weighted_random_choice(self.cities, weight=lambda i, v: v.population, reverse=False)

                new_capital.make_capital()
        else:
            self.mod_morale(CAPITAL_CITY_MORALE_BONUS)

        for city in self.cities:
            #It's more likely to found a new city when this city is near population capacity
            #Because as there's no more space, people want to go to a new city
            try:
                found_city_chance = max(1, int(len(self.cities)**4 * math.log(city.population_capacity - city.population)))
            except: #Log is negative
                found_city_chance = max(1, len(self.cities)**4)
            if random.randint(0, found_city_chance) == 0 and self.money > CITY_FOUND_COST:
                self.create_city()

            if self.current_research == None or self.current_research.is_unlocked():
                if self.current_research != None and self.current_research.is_unlocked():
                    self.parent.events.append(events.EventTechResearch('TechResearch', {'nation_a': self.id, 'tech_a': self.current_research.name}, self.parent.get_current_date()))

                    print(self.parent.events[-1].text_version())
                available = self.tech.get_available_research()

                if len(available) > 0:
                    self.current_research = random.choice(available)
                else: #There's nothing left to research
                    self.current_research = None
            else:
                self.current_research.do_research(random.randint(1, int(log(city.population + 1)**2 + 1)))

                for cell in city.cells:
                    for building in cell.buildings:
                        research_rate = building.get_research_rate()

                        if research_rate > 0:
                            self.current_research.do_research(random.randint(1, research_rate))

        self.religion.history_step(self.parent)
        self.handle_rearming()

        self.age += 1

        for office in self.offices:
            self.mod_morale(int(office.get_modifier('morale') * OFFICE_MORALE_BONUS))

        #More cities means less happiness
        self.mod_morale(-(len(self.cities) + 1))

    def __repr__(self):
        return '{} ({}): ${}; Pop: {}'.format(self.name.short_name(), self.color, int(self.money), sum([i.population for i in self.cities]))
