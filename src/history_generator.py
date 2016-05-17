from math import *
from Tkinter import *
import tkMessageBox
from time import sleep
import tkFont
import random

import sys

import cProfile

import utility

from nation import *
from city import *
from martial import *
from battle import *
from language import *

import culture
import events
import event_analysis
import terrain

import noise

DEFAULT_SIMULATION_SPEED = 300 #ms

class Main:
    nation_count = 8

    def __init__(self):
        self.events = []

        self.year = 0
        self.month = 1
        self.day = 0
        self.hour = 0
        self.minute = 0

        self.parent = Tk()
        self.parent.title('Year: 0')
        self.parent.geometry("{}x{}+0+0".format(utility.DISPLAY_WIDTH, utility.DISPLAY_HEIGHT))

        self.canvas = Canvas(self.parent, bd=1, relief=RIDGE, width=utility.DISPLAY_WIDTH, height=utility.DISPLAY_HEIGHT - 4, scrollregion=(0, 0, utility.S_WIDTH, utility.S_HEIGHT))
        self.canvas.bind('<Button-1>', self.get_cell_information)
        self.canvas.bind('<MouseWheel>', self.on_vertical)
        self.canvas.bind('<Shift-MouseWheel>', self.on_horizontal)

        self.canvas.grid(row=0, column=3, rowspan=12)#, sticky=W + E + N + S)

        self.after_id = 0

        self.nation_id = 0

        self.battles = []

        self.cells = []

        self.nations = []

        self.is_continuous = False
        self.run_until_battle = False
        self.advancing = False

        self.setup()

    def zoom(self, size):
        utility.CELL_SIZE = int(self.zoom_scale.get())

        if utility.CELL_SIZE < 1:
            utility.CELL_SIZE = 1

        utility.S_WIDTH = utility.CELL_SIZE * len(self.cells)
        utility.S_HEIGHT = utility.CELL_SIZE * len(self.cells[0])

        self.canvas.config(scrollregion=(0, 0, utility.S_WIDTH, utility.S_HEIGHT))

        if utility.S_WIDTH < utility.DISPLAY_WIDTH:
            self.canvas.config(width=utility.S_WIDTH)
        else:
            self.canvas.config(width=utility.DISPLAY_WIDTH)

        if utility.S_HEIGHT < utility.DISPLAY_HEIGHT:
            self.canvas.config(height=utility.S_HEIGHT)
        else:
            self.canvas.config(height=utility.DISPLAY_HEIGHT)

        for x in self.cells:
            for y in x:
                self.canvas.delete(y.id)
                y.make_id()

        for nation in self.nations:
            for city in nation.cities:
                city.remake_display_name()

    def on_vertical(self, event):
        self.canvas.yview_scroll(-event.delta, 'units')

    def on_horizontal(self, event):
        self.canvas.xview_scroll(-event.delta, 'units')

    def setup(self):
        size = utility.S_WIDTH // utility.CELL_SIZE
        data = noise.generate_noise(size, 'Generating terrain: ')
        print('')
        cells_x = utility.S_WIDTH // utility.CELL_SIZE
        cells_y = utility.S_HEIGHT // utility.CELL_SIZE
        for x in xrange(cells_x):
            self.cells.append([])
            for y in xrange(cells_y):
                utility.show_bar(x * cells_y + y, cells_x * cells_y, message='Generating world: ', number_limit=True)
                self.cells[-1].append(terrain.Cell(self, '', x, y, data[x][y], random.random()**6, 0, None))

        self.weather = terrain.Weather(self.cells)
        self.weather.run(10)

        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                cell.terrain.setup()
                cell.reset_color()

        print('')

        self.nations = []
        self.old_nations = {}

        for new_nation in xrange(self.nation_count):
            self.nations.append(Nation(self))

        self.create_gui()

        events.main = self

    def get_next_id(self):
        self.nation_id += 1

        return 'nation {}'.format(self.nation_id)

    def create_gui(self):
        self.parent.columnconfigure(3, weight=1)
        self.parent.rowconfigure(11, weight=1)

        self.continuous = Button(self.parent, text="Run until battle", command=self.toggle_run_until_battle)
        self.continuous.grid(row=0, sticky=W)

        self.minimize_battles = Checkbutton(self.parent, text='Minimize battle windows', command=self.toggle_minimize_battles)
        self.minimize_battles.grid(row=0, column=1, columnspan=2, sticky=W)

        self.religion_history_button = Button(self.parent, text="Religion history", command=self.open_religion_history_window)
        self.religion_history_button.grid(row=2, column=0, sticky=W)

        self.world_history_button = Button(self.parent, text="World history", command=self.open_world_history_window)
        self.world_history_button.grid(row=2, column=1, sticky=W)

        self.zoom_label = Label(self.parent, text='Zoom (Cell Size):')
        self.zoom_label.grid(row=3, column=0, sticky=W)

        self.zoom_scale = Scale(self.parent, from_=1, to_=20, orient=HORIZONTAL)
        self.zoom_scale.grid(row=4, column=0, sticky=W)
        self.zoom_scale.bind('<ButtonRelease-1>', self.zoom)
        self.zoom_scale.set(utility.CELL_SIZE)

        self.advance_button = Button(self.parent, text="Advance Step", command=self.main_loop)
        self.advance_button.grid(row=5, sticky=W)

        self.run_continuously_checkbutton = Checkbutton(self.parent, text='Run continuously', command=self.toggle_continuous)
        self.run_continuously_checkbutton.grid(row=5, column=1, sticky=W)

        self.simulation_speed_label = Label(self.parent, text='Simulation Speed (ms):')
        self.simulation_speed_label.grid(row=6, column=0, sticky=W)

        self.delay = Scale(self.parent, from_=10, to_=1000, orient=HORIZONTAL)
        self.delay.grid(row=7, sticky=W)
        self.delay.set(DEFAULT_SIMULATION_SPEED)

        self.advance_time_button = Button(self.parent, text='Advance By:', command=self.run_to)
        self.advance_time_button.grid(row=8, column=0, sticky=W)

        self.years_input = StringVar()
        self.years_box = Entry(self.parent, textvariable=self.years_input)
        self.years_box.grid(row=9, column=0, sticky=W)
        self.years_input.set('0')

        self.nation_selector = Listbox(self.parent)
        self.nation_selector.grid(row=10, column=0, columnspan=3, sticky=W+E)

        self.nation_selector.bind('<Double-Button-1>', self.select_nation)

        self.refresh_nation_selector()

    def open_religion_history_window(self):
        self.religion_history_window = event_analysis.HistoryWindow('Religion History', ['ReligionGodAdded', 'ReligionGodRemoved', 'ReligionDomainAdded', 'ReligionDomainRemoved'])

    def open_world_history_window(self):
        self.world_history_window = event_analysis.HistoryWindow('World History', ['NationFounded', 'CityFounded', 'CityMerged', 'ReligionGodAdded', 'ReligionGodRemoved', 'ReligionDomainAdded', 'ReligionDomainRemoved', 'DiplomacyTrade', 'DiplomacyWar', 'ArmyDispatched', 'Attack', 'Revolt'])

    def toggle_minimize_battles(self):
        utility.START_BATTLES_MINIMIZED = not utility.START_BATTLES_MINIMIZED

    def select_nation(self, event):
        selected_item = self.nation_selector.get(self.nation_selector.curselection())
        for nation in self.nations:
            if str(nation) == selected_item:
                nation.show_information_gui()

                break

    def get_all_cities(self):
        res = []
        for nation in self.nations:
            res.extend(nation.cities)
        return res

    def available_colors(self):
        #For the deep copy
        available_list = list(NATION_COLORS)

        for nation in self.nations:
            available_list.remove(nation.color)

        return available_list

    def add_nation(self, nation):
        self.nations.append(nation)
        self.events.append(events.EventNationFounded("NationFounded", {"nation_a": self.nations[-1].id}, self.get_current_date()))

    def remove_nation(self, nation):
        #Remove this nation from other treaties.
        for remove_war in nation.at_war:
            remove_war.at_war.remove(nation)
        for remove_trade in nation.trading:
            remove_trade.trading.remove(nation)

        print('{}: {} has been eliminated!'.format(self.get_current_date(), nation.name))

        self.old_nations[nation.id] = nation.name

        self.nations.remove(nation)

    def refresh_nation_selector(self):
        self.nation_selector.delete(0, END)
        for nation in self.nations:
            self.nation_selector.insert(END, nation)

    def get_cell_information(self, event):
        if self.parent.focus_get() != None:
            cell_x, cell_y = event.x // utility.CELL_SIZE, event.y // utility.CELL_SIZE

            self.cells[cell_x][cell_y].show_information_gui()

    def run_to(self):
        self.advancing = True

        try:
            advance_amount = int(self.years_input.get())

            if advance_amount > 0:
                self.end_year = self.year + advance_amount
            else:
                tkMessageBox.showerror('Negative Years', 'Cannot advance a negative amount of time.')
        except ValueError:
            tkMessageBox.showerror('Invalid Year', '{} is not a valid integer'.format(self.years_input.get()))
            return

        self.after_id = self.parent.after(self.delay.get(), self.main_loop)

    def toggle_run_until_battle(self):
        self.run_until_battle = not self.run_until_battle

        if self.run_until_battle and not self.is_continuous: #This mean we weren't just running continuously, so start
            self.after_id = self.parent.after(self.delay.get(), self.main_loop)

    def toggle_continuous(self):
        self.is_continuous = not self.is_continuous

        if self.is_continuous: #This mean we weren't just running continuously, so start
            self.after_id = self.parent.after(self.delay.get(), self.main_loop)

    def change_cell_ownership(self, x, y, city, new_type=None):
        self.cells[x][y].change_owner(city, new_type=new_type)

    def start(self):
        self.parent.mainloop()

    def main_loop(self):
        self.parent.title("Map View: Year {}".format(self.year))

        try:
            if self.month == 12:
                self.year += 1
                self.month = 1

                for i in self.nations:
                    i.history_step()

                    if len(i.cities) == 0 and len(i.moving_armies) == 0 and len(self.battles) == 0:
                        self.remove_nation(i)

            if len(self.battles) == 0 or self.day == 30:
                for i in self.nations:
                    i.grow_population()

                    i.move_armies(utility.flatten([nation.moving_armies for nation in self.nations if nation != i]))

                    for k in i.at_war:
                        if not (k in self.nations):
                            i.at_war.remove(k)

                    if len(i.cities) == 0 and len(i.moving_armies) == 0 and len(self.battles) == 0:
                        self.remove_nation(i)

                # We only want to handle moving the groups after we handle each city.
                # This is because the groups involve caravans, which need to know
                # about a city's production in the last month, so that we can calculate prices
                for i in self.nations:
                    i.group_step()

                #We can only have one nation per color
                if random.randint(0, len(self.nations)**3 + 5) == 0 and len(self.nations) < len(NATION_COLORS):
                    self.add_nation(Nation(self))

                self.diplomacy()

                self.refresh_nation_selector()

                self.write_out_events('event_log.txt')

                self.month += 1

            if len(self.battles) > 0:
                self.run_until_battle = False

            if self.is_continuous or self.run_until_battle:
                self.after_id = self.parent.after(self.delay.get(), self.main_loop)
            elif self.advancing:
                if self.year < self.end_year:
                    self.after_id = self.parent.after(self.delay.get(), self.main_loop)
                else:
                    #We finish advancing next step
                    self.advancing = False
                    self.after_id = self.parent.after(self.delay.get(), self.main_loop)
        except KeyboardInterrupt:
            self.write_out_events('event_log.txt')

    def get_current_date(self):
        return (self.year, self.month, self.day)

    def write_out_events(self, filename):
        with open(filename, 'w' if self.month == 1 and self.year == 1 else 'a') as f:
            for event in self.events:
                # print("Writing event {}".format(event.to_dict()))
                f.write('{}\n'.format(event.to_dict()))

            self.events = []

    def get_nation_by_name(self, name):
        for i in self.nations:
            if i.name == name:
                return i

    def remove_dead_nations_from_trading(self):
        for nation in self.nations:
            for partner in nation.trading:
                if not partner in self.nations:
                    nation.trading.remove(partner)

    def start_war(self, a, b, is_holy_war=False):
        if a != b and not b in a.at_war and not a in b.at_war:
            if not b in a.trading and not a in b.trading:
                a.at_war.append(b)
                b.at_war.append(a)

                distance_to_enemy = utility.distance(a.get_average_city_position(), b.get_average_city_position())

                # print('Declared war on enemy who is: {} away'.format(distance_to_enemy))

                if is_holy_war:
                    print("{}: {} has started a holy war with {} because of religious differences.".format(self.get_current_date, a.name, b.name))
                    self.events.append(events.EventDiplomacyWar('DiplomacyWar', {'nation_a': a.id, 'nation_b': b.id, 'reason': 'religious'}, self.get_current_date()))
                else:
                    print("{}: {} has gone to war with {}!".format(self.get_current_date(), a.name, b.name))
                    self.events.append(events.EventDiplomacyWar('DiplomacyWar', {'nation_a': a.id, 'nation_b': b.id, 'reason': 'economic'}, self.get_current_date()))

    def start_trade_agreement(self, a, b):
        #Some more sanity checks, just in case.
        if not a in b.trading and not b in a.trading and a != b:
            if not a in b.at_war and not b in a.at_war:
                a.trading.append(b)
                b.trading.append(a)

                print("{}: {} has begun to send caravans to and receive them from {}".format(self.get_current_date(), a.name, b.name))

                self.events.append(events.EventDiplomacyTrade('DiplomacyTrade', {'nation_a': a.id, 'nation_b': b.id}, self.get_current_date()))

    def handle_revolt(self, nation):
        #Not for realism, but this just can't happen, because then they'd be sharing colors.
        if len(self.nations) < len(NATION_COLORS):
            #Need more than one city to revolt.
            if len(nation.cities) > 1:
                if random.randint(0, max(1, 50 + nation.morale)) == 0:
                    revolted_cities = []
                    for city in nation.cities:
                        #Not all cities can revolt
                        if random.randint(0, max(1, int(city.morale))) == 0 and len(nation.cities) > 1:
                            revolted_cities.append(city)
                            nation.remove_city(city)

                    #At least one city has to revolt, we already decided a revolt was happening, dammit!
                    if len(revolted_cities) == 0:
                        min_morale = nation.cities[0].morale
                        lowest_morale = nation.cities[0]
                        for city in nation.cities:
                            if city.morale < min_morale:
                                min_morale = city.morale
                                lowest_morale = city
                        revolted_cities.append(lowest_morale)
                        nation.remove_city(lowest_morale)

                    self.nations.append(Nation(self, revolted_cities))

                    #For readability
                    revolted_nation = self.nations[-1]

                    revolted_nation.army_structure = nation.army_structure.zero() #The actual army revolts are just the armies in the revolting cities
                    revolted_nation.language = Language(base_language=nation.language)

                    #Copy weapon choices over
                    #We don't want a shallow copy because they shouldn't share research
                    revolted_nation.sidearm_list = list(nation.sidearm_list)
                    revolted_nation.basic_weapon_list = list(nation.basic_weapon_list)
                    revolted_nation.weapon_list = list(nation.weapon_list)
                    revolted_nation.basic_ranged_weapon_list = list(nation.basic_ranged_weapon_list)
                    revolted_nation.ranged_weapon_list = list(nation.ranged_weapon_list)
                    revolted_nation.armor_list = list(nation.armor_list)
                    revolted_nation.basic_armor_list = list(nation.basic_armor_list)

                    army_revolted = sum([city.army.size() for city in revolted_nation.cities])

                    #The revolting nation increases their morale because they're now free from whatever issues they saw with the old regime
                    revolted_nation.mod_morale(MORALE_INCREMENT * len(revolted_cities) * int(log(army_revolted + 2)))

                    #The old nation increases their morale because the haters are now gone.
                    nation.mod_morale(len(revolted_cities) * MORALE_INCREMENT * int(log(sum([city.army.size() for city in nation.cities]) + 2)))

                    print('{}:'.format(self.get_current_date()))
                    print("There was a revolt in the nation of {}, resulting in the creation of the new nation state of {}.".format(nation.name, revolted_nation.name))
                    print("The following cities joined the revolt, along with {} soldiers: {}".format(army_revolted, self.nations[-1].cities))

                    self.events.append(events.EventRevolt('Revolt', {'nation_a': nation.id, 'nation_b': revolted_nation.id, 'cities': [city.name for city in revolted_nation.cities]}, self.get_current_date()))

                    #We don't have peaceful revolts, naturally a nation would attempt to put down the revolt.
                    self.start_war(nation, revolted_nation)

    def diplomacy(self):
        for i in self.nations:
            self.handle_revolt(i)

            #Let's go to war, but we can only do that if there is a nation other than us
            if random.randint(0, max(15, (len(i.at_war) + 1)**5 + 2*i.get_tolerance())) == 0 and len(self.nations) > 1:
                enemy = utility.weighted_random_choice(self.nations, weight=lambda _, v: utility.distance(i.get_average_city_position(), v.get_average_city_position()), reverse=True)

                #We can't go to war twice, fight with a trading partner, or be war with ourselves
                #Because doing any of those things would be really stupid
                if not enemy in i.at_war and not enemy in i.trading and enemy != i:
                    self.start_war(i, enemy)
            else:
                for enemy in self.nations: #CHECK FOR THE HEATHEN BASTARDS
                    if enemy != i and enemy.religion != i.religion and random.randint(0, 3 * i.get_tolerance()) == 0:
                        self.start_war(i, enemy)

                        break

            #Let's try not warring with them, and trade instead, perhaps?
            if random.randint(0, max(4, int(7**log(max(1, i.get_tolerance()))))) == 0: #Randomly start a new trade agreement. Change it later
                partner = utility.weighted_random_choice(self.nations, weight=lambda _, v: utility.distance(i.get_average_city_position(), v.get_average_city_position()), reverse=True)

                #We can't trade with somebody we're already trading with or at war with, and we can't trade with ourselves
                if not partner in i.trading and not partner in i.at_war and not partner == i:
                    self.start_trade_agreement(i, partner)

            self.remove_dead_nations_from_trading()

            self.handle_army_dispatch(i)

    def handle_army_dispatch(self, nation):
        #Determine if we want to launch an attack with this cities army
        for city in nation.cities:
            #Cool, let's fight them, assuming we have soldiers of course, and there is a them to fight
            if len(nation.at_war) > 0 and city.army.size() > 0:
                enemy = random.choice(nation.at_war)

                if len(enemy.cities) > 0 and enemy in self.nations:
                    attacking_city = utility.weighted_random_choice(enemy.cities, weight=lambda _, v: utility.distance(city.position, v.position), reverse=True)

                    if random.randint(0, max(20, city.army.size() + city.population // 8 - attacking_city.population // 3 - attacking_city.army.size())) > 20 and random.randint(0, len(nation.moving_armies)**3) == 0:
                        fx, fy = city.position

                        dx, dy = attacking_city.position

                        #Conscript some levies to join the army.
                        if city.population // 3 > 1:
                            conscript_max = max(city.population // 4, 3)
                            conscript_min = min(city.population // 8, 2)
                            conscripted = int(random.randint(conscript_min, conscript_max) * nation.get_conscription_bonus())
                        else:
                            conscripted = 0

                        # print('Conscripted {} people (out of {}) into the army.'.format(conscripted, city.population))

                        city.population -= conscripted
                        city.army.add_to(city.army.name, conscripted)

                        nation.moving_armies.append(Group(nation.name, city.army, (fx, fy), (dx, dy), nation.color, lambda s: False, self.do_attack(nation, city, enemy, attacking_city), self.canvas))

                        self.events.append(events.EventArmyDispatched('ArmyDispatched', {'nation_a': nation.id, 'nation_b': enemy.id, 'city_a': city.name, 'city_b': attacking_city.name, 'reason': 'attack', 'army_size': city.army.size()}, self.get_current_date()))

                        city.army = city.army.zero()
                    # elif random.randint(0, city.army.size()) < city.army.size() // 4 and len(nation.cities) > 1: #Reinforce another city
                    #     fx, fy = city.position
                    #
                    #     #We obviously can't reinforce the same city
                    #     reinforcement_cities = filter(lambda check: check != city, nation.cities)
                    #
                    #     #This really should always be true, but, as always, just in case
                    #     if len(reinforcement_cities) > 0:
                    #         #We want to reinforce cities with larger armies more, so we can better amass our forces for attacks
                    #         reinforce_city = utility.weighted_random_choice(reinforcement_cities, lambda _, v: v.army.size())
                    #
                    #         if reinforce_city != city:
                    #             dx, dy = reinforce_city.position
                    #
                    #             nation.moving_armies.append(Group(nation.name, city.army, (fx, fy), (dx, dy), nation.color, lambda s, c: False, self.reinforce(nation, reinforce_city), self.canvas))
                    #
                    #             self.events.append(events.EventArmyDispatched('ArmyDispatched', {'nation_a': nation.id, 'nation_b': nation.id, 'city_a': city.name, 'city_b': reinforce_city.name, 'reason': 'reinforce', 'army_size': city.army.size()}, self.get_current_date()))
                    #
                    #             city.army = city.army.zero()

    def return_levies(self, sender, reinforce_city):
        def do(reinforcing):
            print('{} levied soldiers returned to {}'.format(reinforcing.members.size(), reinforce_city.name))

            sender.moving_armies.remove(reinforcing)
            self.canvas.delete(reinforcing.id)

            if reinforce_city.nation == sender: #If we own it, as we should, just join the army.
                reinforce_city.population += reinforcing.members.size()
            elif reinforce_city.nation in sender.at_war: #If we're at war with the nation that now owns our city, attack it.
                self.attack(sender, reinforcing.members, reinforce_city.nation, None, reinforce_city)
            else: #if a third party is involved, let's just return back home
                return_destination = random.choice(sender.cities)
                sender.moving_armies.append(Group(sender.name, reinforcing.members, reinforce_city.position, return_destination.position, sender.color, lambda s: False, self.reinforce(sender, return_destination), self.canvas))

                self.events.append(events.EventArmyDispatched('ArmyDispatched', {'nation_a': sender.id, 'nation_b': sender.id, 'city_a': reinforce_city.name, 'city_b': return_destination.name, 'reason': 'reinforce', 'army_size': reinforcing.members.size()}, self.get_current_date()))

        return do

    #These functions return other functions so that they can be called from the Group class and still have all the relevant information
    def reinforce(self, sender, reinforce_city):
        def do(reinforcing):
            sender.moving_armies.remove(reinforcing)
            self.canvas.delete(reinforcing.id)

            if reinforce_city.nation == sender: #If we own it, as we should, just join the army.
                reinforce_city.army.add_army(reinforcing.members)
            elif reinforce_city.nation in sender.at_war: #If we're at war with the nation that now owns our city, attack it.
                self.attack(sender, reinforcing.members, reinforce_city.nation, None, reinforce_city)
            else: #if a third party is involved, let's just return back home
                return_destination = random.choice(sender.cities)
                sender.moving_armies.append(Group(sender.name, reinforcing.members, reinforce_city.position, return_destination.position, sender.color, lambda s: False, self.reinforce(sender, return_destination), self.canvas))

                self.events.append(events.EventArmyDispatched('ArmyDispatched', {'nation_a': sender.id, 'nation_b': sender.id, 'city_a': reinforce_city.name, 'city_b': return_destination.name, 'reason': 'reinforce', 'army_size': reinforcing.members.size()}, self.get_current_date()))

        return do

    def do_attack(self, attacker, attacking_city, defender, city):
        def do(attacking):
            attacker.moving_armies.remove(attacking)
            self.canvas.delete(attacking.id)

            self.attack(attacker, attacking.members, defender, attacking_city, city)

        return do

    def attack(self, attacker, attacking_army, defender, attacking_city, city):
        if city in defender.cities:
            #Somebody has to show up to defend the city.
            defender_max = max(city.population // 3, 3)
            defender_min = max(city.population // 6, 2)
            defending_garrison_size = random.randint(defender_min, defender_max)

            defending_army = defender.army_structure.zero().add_to(defender.army_structure.name, defending_garrison_size)

            city.population = max(city.population - defending_garrison_size, 1)

            #The army should also defend
            defending_army.add_army(city.army)

            city.army = city.army.zero()

            print("{}: A battle has begun between {} and {}".format(self.get_current_date(), attacker.name, defender.name))
            print("{} has {} soldiers, and {} has {} soldiers, for a total of {} soldiers.".format(attacker.name, attacking_army.size(), defender.name, defending_army.size(), attacking_army.size() + defending_army.size()))

            if attacking_army.size() == 0:
                attacking_army.add_number(1, attacker)

            battle = Battle(attacker, attacking_army, defender, defending_army, attacking_city, city, self.end_battle)
            battle.setup_soldiers()

            if not battle.check_end_battle():
                battle.main_phase()

                self.battles.append(battle)

                print("Battle started. {} currently running.".format(len(self.battles)))
        elif city in attacker.cities: #if we already own it, just join the army that's already there
            city.army.add_army(attacking_army)
        else: #If somebody other than us or the person we intended to attack owns this city, just go back to reinforce one of our cities.
            if len(attacker.cities) > 0: #It really ought to be, but it could happen that we lose all our cities before we can go back.
                return_destination = random.choice(attacker.cities)
                attacker.moving_armies.append(Group(attacker.name, attacking_army, city.position, return_destination.position, attacker.color, lambda s: False, self.reinforce(attacker, return_destination), self.canvas))

                self.events.append(events.EventArmyDispatched('ArmyDispatched', {'nation_a': attacker.id, 'nation_b': attacker.id, 'city_a': city.name, 'city_b': return_destination.name, 'reason': 'reinforce', 'army_size': attacking_army.size()}, self.get_current_date()))

    def end_battle(self, battle):
        a = battle.a
        b = battle.b

        attack_city = battle.city

        if battle in self.battles:
            self.battles.remove(battle)

        print("Battle ended.")

        #Determine the winner
        if battle.a_army.size() > 0:
            print("{}: {} has triumphed with {} remaining troops!".format(self.get_current_date(), a.name, battle.a_army.size()))

            self.events.append(events.EventAttack('Attack', {'nation_a': a.id, 'nation_b': b.id, 'city_b': attack_city.name, 'success': True, 'remaining_soldiers': battle.a_army.size()}, self.get_current_date()))

            print("They have taken the city of {} from {}.".format(attack_city.name, b.name))

            attack_city.capture(battle.a_army, a, battle.attacking_city)
            a.capture_city(attack_city)
        elif battle.b_army.size() > 0:
            print("{}: {} has triumphed with {} remaining troops!".format(self.get_current_date(), b.name, battle.b_army.size()))

            self.events.append(events.EventAttack('Attack', {'nation_a': a.id, 'nation_b': b.id, 'city_b': attack_city.name, 'success': False, 'remaining_soldiers': battle.b_army.size()}, self.get_current_date()))

            b.mod_morale(MORALE_INCREMENT)
            a.mod_morale(-MORALE_INCREMENT)

            #Add the levy back to the defending city's population, then put the army back as the army.
            attack_city.population += battle.b_army.number
            battle.b_army.number = 0 #Set the first tier soldiers to 0, because they all went back into the city
            attack_city.army = battle.b_army

        self.attack_city = None

        self.after_id = self.parent.after(self.delay.get(), self.main_loop)

    def all_cities(self, ignore_nation=None):
        if len(self.nations) > 0:
            return reduce(lambda a,b: a + b, map(lambda a: a.cities if a != ignore_nation else [], self.nations))
        else:
            return []

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        params = arg.split('=')

        if params[0] == "width":
            utility.S_WIDTH = int(params[1])
        elif params[0] == "height":
            utility.S_HEIGHT = int(params[1])
        elif params[0] == "size":
            utility.CELL_SIZE = int(params[1])

cProfile.run('Main().start()', sort='tottime')
raw_input()
# History = Main()
# History.start()
