from Tkinter import *
import tkMessageBox
import random

import sys

import civil.battle_history as battle_history
import civil.treaty as treaty
import internal.terrain.cell
import internal.terrain.weather
import internal.utility as utility

import civil.city as city
import civil.nation as nation

import culture.religion as religion

import internal.events as events
import internal.event_analysis as event_analysis
import internal.terrain.noise as noise
import internal.db as db
import internal.gui as gui

import military.battle as battle
from internal.event_log import EventLog
from internal.group.group import Group
from internal.progress_bar import map_task, sequence_tasks, call_task, ProgressBar

DEFAULT_SIMULATION_SPEED = 300  # ms


class Main:
    nation_count = 8

    def __init__(self):
        events.main = self

        self.old_nations = {}

        self.year = 1
        self.month = 1
        self.day = 1
        self.hour = 0
        self.minute = 0

        self.parent = Tk()
        self.parent.title('Year: 0')
        self.parent.geometry("{}x{}+0+0".format(utility.DISPLAY_WIDTH, utility.DISPLAY_HEIGHT))
        self.parent.config(background='white')

        self.after_id = 0
        self.advance_num = 0

        self.ids = {}

        self.battles = []

        self.battle_history = []
        self.treaties = []

        self.cells = []

        self.nations = []
        self.coninents = []
        self.religions = []

        self.is_continuous = False
        self.run_until_battle = False
        self.advancing = False
        self.graphical_battles = True
        self.fast_battles = False

        self.world_name = ''

        self.db = None  # The DB connection. Will be created after setup so we can give it a real name.

        # Set up the GUI

        self.event_log_box = Listbox(self.parent, height=10)
        self.event_log = EventLog(self, self.db, self.event_log_box)

        self.parent.columnconfigure(3, weight=1)
        self.parent.rowconfigure(13, weight=1)

        self.parent.bind('<MouseWheel>', self.on_vertical)
        self.parent.bind('<Shift-MouseWheel>', self.on_horizontal)
        self.parent.bind('<Left>', lambda _: self.scroll_canvas(-utility.SCROLL_SPEED, 0))
        self.parent.bind('<Right>', lambda _: self.scroll_canvas(utility.SCROLL_SPEED, 0))
        self.parent.bind('<Up>', lambda _: self.scroll_canvas(0, -utility.SCROLL_SPEED))
        self.parent.bind('<Down>', lambda _: self.scroll_canvas(0, utility.SCROLL_SPEED))

        self.canvas = Canvas(self.parent, bd=1, relief=RIDGE, scrollregion=(0, 0, utility.S_WIDTH, utility.S_HEIGHT))
        self.canvas.bind('<Button-1>', self.get_cell_information)
        self.canvas.config(background='white')

        self.canvas.grid(row=0, column=3, rowspan=14, sticky=W + E + N + S)

        self.continuous = gui.Button(self.parent, text="[R]un until battle", command=self.toggle_run_until_battle)
        self.continuous.grid(row=0, sticky=W)

        self.minimize_battles = gui.Checkbutton(self.parent, text='Minimize battle windows',
                                                command=self.toggle_minimize_battles)
        self.minimize_battles.grid(row=0, column=1, columnspan=2, sticky=W)

        self.religion_history_button = gui.Button(self.parent, text="R[e]ligion history",
                                                  command=self.open_religion_history_window)
        self.religion_history_button.grid(row=2, column=0, sticky=W)

        self.world_history_button = gui.Button(self.parent, text="[W]orld history",
                                               command=self.open_world_history_window)
        self.world_history_button.grid(row=2, column=1, sticky=W)

        self.zoom_label = gui.Label(self.parent, text='Zoom (Cell Size):')
        self.zoom_label.grid(row=3, column=0, sticky=W)

        self.graphical_battles_checkbox = gui.Checkbutton(self.parent, text='Graphical Battles',
                                                          command=self.toggle_graphical_battles)
        self.graphical_battles_checkbox.grid(row=3, column=1, sticky=W)
        self.graphical_battles_checkbox.select()  # Graphical battles are the default

        self.fast_battles_checkbox = gui.Checkbutton(self.parent, text='Fast Battles', command=self.toggle_fast_battles)
        self.fast_battles_checkbox.grid(row=4, column=1, sticky=W)

        self.zoom_scale = gui.Scale(self.parent, from_=1, to_=20, orient=HORIZONTAL)
        self.zoom_scale.grid(row=4, column=0, sticky=W)
        self.zoom_scale.bind('<ButtonRelease-1>', self.zoom)
        self.zoom_scale.set(utility.CELL_SIZE)

        self.advance_button = gui.Button(self.parent, text="[A]dvance Step", command=self.advance_once)
        self.advance_button.grid(row=5, sticky=W)

        self.run_continuously_checkbutton = gui.Checkbutton(self.parent, text='Run continuously',
                                                            command=self.toggle_continuous)
        self.run_continuously_checkbutton.grid(row=5, column=1, sticky=W)

        self.simulation_speed_label = gui.Label(self.parent, text='Simulation Speed (ms):')
        self.simulation_speed_label.grid(row=6, column=0, sticky=W)

        self.save_button = gui.Button(self.parent, text='[S]ave', command=self.save)
        self.save_button.grid(row=6, column=1, sticky=W)

        self.delay = gui.Scale(self.parent, from_=10, to_=1000, orient=HORIZONTAL)
        self.delay.grid(row=7, sticky=W)
        self.delay.set(DEFAULT_SIMULATION_SPEED)

        self.advance_time_button = gui.Button(self.parent, text='Advance [B]y:', command=self.run_to)
        self.advance_time_button.grid(row=8, column=0, sticky=W)

        self.years_box = Entry(self.parent)
        self.years_box.grid(row=9, column=0, sticky=W)

        self.nation_selector_label = gui.Label(self.parent, text='Nations:')
        self.nation_selector_label.grid(row=10, column=0, sticky=W)

        self.nation_selector = Listbox(self.parent)
        self.nation_selector.grid(row=11, column=0, columnspan=3, sticky=W + E)

        self.nation_selector.bind('<Double-Button-1>', self.select_nation)

        self.event_log_box.grid(row=15, column=3, stick=W + E)

        # Set up hotkeys
        self.parent.bind('R', lambda _: self.toggle_run_until_battle())
        self.parent.bind('r', lambda _: self.toggle_run_until_battle())
        self.parent.bind('E', lambda _: self.open_religion_history_window())
        self.parent.bind('e', lambda _: self.open_religion_history_window())
        self.parent.bind('W', lambda _: self.open_world_history_window())
        self.parent.bind('w', lambda _: self.open_world_history_window())
        self.parent.bind('A', lambda _: self.advance_once())
        self.parent.bind('a', lambda _: self.advance_once())
        self.parent.bind('S', lambda _: self.save())
        self.parent.bind('s', lambda _: self.save())
        self.parent.bind('B', lambda _: self.run_to())
        self.parent.bind('b', lambda _: self.run_to())

        self.refresh_nation_selector()

        self.setup()

    def get_real_date(self):
        return '{}-{}-{}'.format(self.year, self.month, self.day)

    def zoom(self, size):
        utility.CELL_SIZE = int(self.zoom_scale.get())

        if utility.CELL_SIZE < 1:
            utility.CELL_SIZE = 1

        utility.S_WIDTH = utility.CELL_SIZE * len(self.cells)
        utility.S_HEIGHT = utility.CELL_SIZE * len(self.cells[0])

        self.canvas.config(scrollregion=(0, 0, utility.S_WIDTH, utility.S_HEIGHT))

        for x in self.cells:
            for y in x:
                self.canvas.delete(y.id)
                y.make_id()

        for nation in self.nations:
            for city in nation.cities:
                city.remake_display_name()

    def scroll_canvas(self, x, y):
        self.canvas.xview_scroll(x, 'units')
        self.canvas.yview_scroll(y, 'units')

    def on_vertical(self, event):
        self.scroll_canvas(0, -event.delta)

    def on_horizontal(self, event):
        self.scroll_canvas(-event.delta, 0)

    def get_neighbor_cells(self, cell, cells):
        return [cells[cell.x + 1][cell.y], cells[cell.x - 1][cell.y], cells[cell.x][cell.y + 1],
                cells[cell.x][cell.y - 1]]

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
                self.cells[-1].append(
                    internal.terrain.cell.Cell(self, '', x, y, data[x][y], random.random() ** 6, 0, None))

        print('')
        self.weather = internal.terrain.weather.Weather(self.cells, self)
        self.weather.run(10)

        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                cell.terrain.setup()
                cell.reset_color()

        print('')

        self.nations = []
        self.religions = []

        for new_nation in xrange(self.nation_count):
            self.add_nation(nation.Nation(self))

        # Initially create one new religion for every nation
        for i in xrange(self.nation_count):
            new_religion = religion.Religion(self, self.nations[i].language, self.nations[i].language.make_name_word())
            new_religion.adherents[self.nations[i].cities[0].name] = self.nations[i].cities[0].population
            self.religions.append(new_religion)

        # Choose a random nation to generate our world's name with
        lang = random.choice(self.nations).language
        self.world_name = lang.translateTo('world')

        self.db = db.DB(self.world_name)
        self.db.setup()

    def create_religion(self, city, nation, founder=None):
        new_religion = religion.Religion(self, nation.language, nation.language.make_name_word())

        self.event_log.add_event('ReligionCreated', {'nation_a': nation.id, 'city_a': city.name,
                                                     'person_a': founder.name,
                                                     'religion_a': new_religion.name},
                                 self.get_current_date())

        self.religions.append(new_religion)
        new_religion.adherents[city.name] = 1  # Hooray! We have an adherent

    def get_next_id(self, id_type):
        if id_type in self.ids:
            self.ids[id_type] += 1
        else:
            self.ids[id_type] = 0

        return self.ids[id_type]

    def advance_once(self):
        self.advance_num = 1
        self.main_loop()

    def open_religion_history_window(self):
        self.religion_history_window = event_analysis.HistoryWindow(self.event_log, 'Religion History',
                                                                    ['ReligionGodAdded', 'ReligionGodRemoved',
                                                                     'ReligionDomainAdded', 'ReligionDomainRemoved'])

    def open_world_history_window(self):
        self.world_history_window = event_analysis.HistoryWindow(self.event_log, 'World History',
                                                                 ['NationFounded', 'CityFounded', 'CityMerged',
                                                                  'ReligionGodAdded', 'ReligionGodRemoved',
                                                                  'ReligionDomainAdded', 'ReligionDomainRemoved',
                                                                  'DiplomacyTrade', 'DiplomacyWar', 'ArmyDispatched',
                                                                  'Attack', 'Revolt'])

    def toggle_graphical_battles(self):
        self.graphical_battles = not self.graphical_battles

    def toggle_fast_battles(self):
        self.fast_battles = not self.fast_battles

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
        # For deep copying
        available_list = list(nation.NATION_COLORS)

        for nat in self.nations:
            available_list.remove(nat.color)

        return available_list

    def add_nation(self, nation):
        self.nations.append(nation)

        # Give them one of the religions that exists already
        # If there are no religions, that means we're at the beginning of world gen, so it's handled separately in the setup() function
        if len(self.religions) > 0:
            religion = random.choice(self.religions)
            for city in nation.cities:
                if len(city.get_religion_populations()) == 0:
                    religion.adherents[city.name] = city.population

        for nation in self.nations:
            for check_nation in self.nations:
                if nation != check_nation:
                    if not check_nation.id in nation.relations:
                        nation.relations[check_nation.id] = 0  # Initially we start out neutral with all nations.

        self.event_log.add_event("NationFounded", {"nation_a": self.nations[-1].id}, self.get_current_date())

    def remove_nation(self, nation):
        # Remove this nation from other treaties.
        for remove_war in nation.at_war:
            war_treaty = nation.get_treaty_with(remove_war, 'war')
            war_treaty.end(self.get_current_date())
        for remove_trade in nation.trading:
            trade_treaty = nation.get_treaty_with(remove_trade, 'trade')
            trade_treaty.end(self.get_current_date())

        self.event_log.add_event("NationEliminated", {"nation_a": nation.id}, self.get_current_date())

        self.old_nations[nation.id] = nation.name

        self.nations.remove(nation)

    def refresh_nation_selector(self):
        self.nation_selector.delete(0, END)
        for nation in self.nations:
            self.nation_selector.insert(END, nation)

    def get_cell_information(self, event):
        if self.parent.focus_get() is not None:
            cell_x, cell_y = event.x // utility.CELL_SIZE, event.y // utility.CELL_SIZE

            # If the user click on an area outside of the drawn map, we'll give an error, but we should really just ignore it.
            if cell_x < len(self.cells) and cell_y < len(self.cells[cell_x]):
                self.cells[cell_x][cell_y].show_information_gui()

    def run_to(self):
        try:
            advance_amount = int(self.years_box.get())

            if advance_amount > 0:
                self.advancing = True
                self.end_year = self.year + advance_amount

                self.after_id = self.parent.after(self.delay.get(), self.main_loop)
            else:
                self.end_year = self.year
                tkMessageBox.showerror('Negative Years', 'Cannot advance a negative or zero amount of time.')
        except ValueError:
            self.end_year = self.year
            tkMessageBox.showerror('Invalid Year', '"{}" is not a valid integer'.format(self.years_box.get()))
            return

    def toggle_run_until_battle(self):
        self.run_until_battle = not self.run_until_battle

        if self.run_until_battle and not self.is_continuous:  # This mean we weren't just running continuously, so start
            self.after_id = self.parent.after(self.delay.get(), self.main_loop)

    def toggle_continuous(self):
        self.is_continuous = not self.is_continuous

        if self.is_continuous:  # This mean we weren't just running continuously, so start
            self.after_id = self.parent.after(self.delay.get(), self.main_loop)

    def change_cell_ownership(self, x, y, city, new_type=None):
        self.cells[x][y].change_owner(city, new_type=new_type)

    def start(self):
        self.parent.mainloop()

    def save(self):
        task = sequence_tasks([call_task(self.db.save, []),
                               call_task(self.event_log.save, [self.db])] +
                              [call_task(cell.save) for row in self.cells for cell in row] +
                              [call_task(nation.save) for nation in self.nations])

        # res = {'date': self.get_current_date(),
        #        'width': utility.S_WIDTH // utility.CELL_SIZE,
        #        'height': utility.S_HEIGHT // utility.CELL_SIZE,
        #        'old_nations': self.old_nations,
        #        'ids': self.ids}
        #
        # with open('saves/{}/main.txt'.format(self.world_name), 'w') as f:
        #     f.write(str(res))
        #
        # i = 0
        # total_cells = len(self.cells) * len(self.cells[0])
        #
        # with open('saves/{}/cells.txt'.format(self.world_name), 'w') as f:
        #     for row in self.cells:
        #         for cell in row:
        #             utility.show_bar(i, total_cells, message='Saving cells ({} of {}): '.format(i, total_cells))
        #             i += 1
        #
        #             f.write('{}\n'.format(cell.get_info()))
        # print('')
        #
        # for i, nation in enumerate(self.nations):
        #     utility.show_bar(i, len(self.nations), message='Saving nations: ')
        #
        #     os.makedirs('saves/{}/nations/{}/'.format(self.world_name, nation.id))
        #     nation.save('saves/{}/nations/{}/'.format(self.world_name, nation.id))
        #
        # for battle in self.battle_history:
        #     battle.save('saves/{}/battle_history/'.format(self.world_name))
        #
        # for treaty in self.treaties:
        #     treaty.save('saves/{}/treaties/'.format(self.world_name))

        progress_bar = ProgressBar('Saving...', task)
        progress_bar.loop()

        print('')

    def main_loop(self):
        self.parent.title("Map View ({}): Year {}".format(self.world_name, self.year))

        if self.month == 12:
            self.year += 1
            self.month = 1

            for r in self.religions:
                r.history_step(self)

            for nat in self.nations:
                nat.history_step()

                if len(nat.cities) == 0 and len(nat.moving_armies) == 0 and len(self.battles) == 0:
                    self.remove_nation(nat)

        if len(self.battles) == 0 or self.day == 30:
            for nat in self.nations:
                nat.grow_population()
                nat.handle_diplomacy()

                if len(nat.cities) == 0 and len(nat.moving_armies) == 0 and len(self.battles) == 0:
                    self.remove_nation(nat)

            # We only want to handle moving the groups after we handle each city.
            # This is because the groups involve caravans, which need to know
            # about a city's production in the last month, so that we can calculate prices
            for nat in self.nations:
                nat.group_step()

            # We can only have one nation per color
            if random.randint(0, len(self.nations) ** 3 + 5) == 0 and len(self.nations) < len(nation.NATION_COLORS):
                self.add_nation(nation.Nation(self))

            self.refresh_nation_selector()

            self.month += 1

            self.start_army_move()

    # Set everything up (like paths and such) so that the armies can later move
    def start_army_move(self):
        for nation in self.nations:
            nation.start_army_moves()

        self.do_army_move()

    def do_army_move(self):
        done = True

        for nation in self.nations:
            if not nation.do_army_moves():
                done = False

        if not done:
            self.after_id = self.parent.after(self.delay.get() / 10, self.do_army_move)
        else:  # If we're done, clean up
            self.end_army_move()

    def end_army_move(self):
        for nation in self.nations:
            nation.end_army_moves()

        if len(self.battles) > 0:
            self.run_until_battle = False

        if self.advance_num > 0:
            self.advance_num -= 1

            if self.advance_num > 0:
                self.after_id = self.parent.after(self.delay.get(), self.main_loop)
        else:
            if self.is_continuous or self.run_until_battle:
                self.after_id = self.parent.after(self.delay.get(), self.main_loop)
            elif self.advancing:
                if self.year < self.end_year:
                    self.after_id = self.parent.after(self.delay.get(), self.main_loop)
                else:
                    # We finish advancing next step
                    self.advancing = False
                    self.after_id = self.parent.after(self.delay.get(), self.main_loop)

    def get_current_date(self):
        return self.year, self.month, self.day

    def get_nation_by_name(self, name):
        for i in self.nations:
            if i.name == name:
                return i

    def start_war(self, a, b, is_holy_war=False):
        if a != b and not b in a.at_war and not a in b.at_war:
            if not b in a.trading and not a in b.trading:
                if is_holy_war:
                    self.event_log.add_event('DiplomacyWar', {'nation_a': a.id, 'nation_b': b.id,
                                                              'reason': 'religious'},
                                             self.get_current_date())
                else:
                    self.event_log.add_event('DiplomacyWar', {'nation_a': a.id, 'nation_b': b.id,
                                                              'reason': 'economic'},
                                             self.get_current_date())

                a.at_war.append(b)
                b.at_war.append(a)

                new_treaty = treaty.Treaty(self, self.get_current_date(), a, b, 'war')

                self.treaties.append(new_treaty)
                a.treaties.append(new_treaty)
                b.treaties.append(new_treaty)

    def start_trade_agreement(self, a, b):
        # Some more sanity checks, just in case.
        if not a in b.trading and not b in a.trading and a != b:
            if not a in b.at_war and not b in a.at_war:
                a.trading.append(b)
                b.trading.append(a)

                new_treaty = treaty.Treaty(self, self.get_current_date(), a, b, 'trade')

                self.treaties.append(new_treaty)
                a.treaties.append(new_treaty)
                b.treaties.append(new_treaty)

                self.event_log.add_event('DiplomacyTrade', {'nation_a': a.id, 'nation_b': b.id},
                                         self.get_current_date())

    def return_levies(self, sender, reinforce_city):
        def do(reinforcing):
            sender.moving_armies.remove(reinforcing)
            self.canvas.delete(reinforcing.id)

            if reinforce_city.nation == sender:  # If we own it, as we should, just join the army.
                reinforce_city.population += reinforcing.members.size()
            elif reinforce_city.nation in sender.at_war:  # If we're at war with the nation that now owns our city, attack it.
                self.attack(sender, reinforcing.members, reinforce_city.nation, None, reinforce_city)
            else:  # if a third party is involved, let's just return back home
                if len(sender.cities) > 0:
                    return_destination = random.choice(sender.cities)
                    sender.moving_armies.append(
                        Group(self, sender.name, reinforcing.members, reinforce_city.position,
                              return_destination.position, sender.color, lambda s: False,
                              self.reinforce(sender, return_destination),
                              is_army=True))

                    self.event_log.add_event('ArmyDispatched',
                                             {'nation_a': sender.id, 'nation_b': sender.id,
                                              'city_a': reinforce_city.name,
                                              'city_b': return_destination.name,
                                              'reason': 'reinforce',
                                              'army_size': reinforcing.members.size()},
                                             self.get_current_date())

        return do

    # These functions return other functions so that they can be called from the Group class and still have all the relevant information
    def reinforce(self, sender, reinforce_city):
        def do(reinforcing):
            sender.moving_armies.remove(reinforcing)
            self.canvas.delete(reinforcing.id)

            if reinforce_city.nation == sender:  # If we own it, as we should, just join the army.
                reinforce_city.army.add_army(reinforcing.members)
            elif reinforce_city.nation in sender.at_war:  # If we're at war with the nation that now owns our city, attack it.
                self.attack(sender, reinforcing.members, reinforce_city.nation, None, reinforce_city)
            else:  # if a third party is involved, let's just return back home
                return_destination = random.choice(sender.cities)
                sender.moving_armies.append(
                    Group(self, sender.name, reinforcing.members, reinforce_city.position,
                          return_destination.position,
                          sender.color, lambda s: False, self.reinforce(sender, return_destination),
                          is_army=True))

                self.event_log.add_event('ArmyDispatched',
                                         {'nation_a': sender.id, 'nation_b': sender.id,
                                          'city_a': reinforce_city.name,
                                          'city_b': return_destination.name,
                                          'reason': 'reinforce',
                                          'army_size': reinforcing.members.size()},
                                         self.get_current_date())

        return do

    def do_attack(self, attacker, attacking_city, defender, city):
        def do(attacking):
            attacker.moving_armies.remove(attacking)
            self.canvas.delete(attacking.id)

            self.attack(attacker, attacking.members, defender, attacking_city, city)

        return do

    def attack(self, attacker, attacking_army, defender, attacking_city, city):
        if city in defender.cities:
            # Somebody has to show up to defend the city.
            defender_max = max(city.population // 3, 3)
            defender_min = max(city.population // 6, 2)
            defending_garrison_size = random.randint(defender_min, defender_max)

            defending_army = defender.army_structure.zero().add_to(defender.army_structure.name,
                                                                   defending_garrison_size)

            city.population = max(city.population - defending_garrison_size, 1)

            # The army should also defend
            defending_army.add_army(city.army)

            city.army = city.army.zero()

            if attacking_army.size() == 0:
                attacking_army.add_number(1, attacker)

            current_battle = battle.Battle(attacker, attacking_army, defender, defending_army, attacking_city, city,
                                           self.end_battle,
                                           use_graphics=self.graphical_battles, fast_battles=self.fast_battles)
            current_battle.setup_soldiers()

            if not current_battle.check_end_battle():
                current_battle.main_phase()

                if self.graphical_battles and not self.fast_battles:
                    self.battles.append(current_battle)
        elif city in attacker.cities:  # if we already own it, just join the army that's already there
            city.army.add_army(attacking_army)
        else:  # If somebody other than us or the person we intended to attack owns this city, just go back to
            # reinforce one of our cities.

            # It could happen that we lose all our cities before we can go back.
            if len(attacker.cities) > 0:
                return_destination = random.choice(attacker.cities)
                attacker.moving_armies.append(
                    Group(self, attacker.name, attacking_army, city.position, return_destination.position,
                          attacker.color, lambda s: False, self.reinforce(attacker, return_destination),
                          is_army=True))

                self.event_log.add_event('ArmyDispatched',
                                         {'nation_a': attacker.id, 'nation_b': attacker.id,
                                          'city_a': city.name,
                                          'city_b': return_destination.name,
                                          'reason': 'reinforce',
                                          'army_size': attacking_army.size()},
                                         self.get_current_date())

    def end_battle(self, battle):
        a = battle.a
        b = battle.b

        attack_city = battle.city

        if battle in self.battles:
            self.battles.remove(battle)

        print('')

        # utility.show_dict(battle.a_stats, recurse=False, gen=self)
        # utility.show_dict(battle.b_stats, recurse=False, gen=self)

        for unit in a.army_structure.make_upgrade_list():
            if unit.name in battle.a_stats:
                unit.handle_battle_end(battle.a_stats[unit.name])
        for unit in b.army_structure.make_upgrade_list():
            if unit.name in battle.b_stats:
                unit.handle_battle_end(battle.b_stats[unit.name])

        war_treaty = a.get_treaty_with(b, 'war')
        war_treaty[a.id]['troops_lost'] += battle.a_stats['troops_lost']
        war_treaty[a.id]['troops_killed'] += battle.a_stats['troops_killed']
        war_treaty[b.id]['troops_lost'] += battle.b_stats['troops_lost']
        war_treaty[b.id]['troops_killed'] += battle.b_stats['troops_killed']

        winner = None

        # Determine the winner
        if battle.a_army.size() > 0:
            self.event_log.add_event('Attack',
                                     {'nation_a': a.id, 'nation_b': b.id, 'city_b': attack_city.name,
                                      'success': True, 'remaining_soldiers': battle.a_army.size()},
                                     self.get_current_date())

            attack_city.capture(battle.a_army, a, battle.attacking_city)
            a.capture_city(attack_city)

            war_treaty.treaty_details[a.id]['cities_conquered'] += 1
            war_treaty.treaty_details[b.id]['cities_lost'] += 1

            winner = a
        elif battle.b_army.size() > 0:
            self.event_log.add_event('Attack',
                                     {'nation_a': a.id, 'nation_b': b.id, 'city_b': attack_city.name,
                                      'success': False, 'remaining_soldiers': battle.b_army.size()},
                                     self.get_current_date())

            b.mod_morale(city.MORALE_INCREMENT)
            a.mod_morale(-city.MORALE_INCREMENT)

            # Add the levy back to the defending city's population, then put the army back as the army.
            attack_city.population += battle.b_army.number
            battle.b_army.number = 0  # Set the first tier soldiers to 0, because they all went back into the city
            attack_city.army = battle.b_army

            winner = b
        else:
            print('----------------------')
            print('No battle winner?')
            print(battle.a_army.size(), battle.b_army.size())
            print('----------------------')

        self.battle_history.append(
            battle_history.BattleHistory(self, attack_city, winner, a, b, self.get_current_date(), battle.a_stats,
                                         battle.b_stats))

        self.after_id = self.parent.after(self.delay.get(), self.main_loop)

    def all_cities(self, ignore_nation=None):
        if len(self.nations) > 0:
            return reduce(lambda a, b: a + b, map(lambda a: a.cities if a != ignore_nation else [], self.nations))
        else:
            return []

    def load(self, filename):
        pass

