import utility
from martial import *
from language import *
from group import *
from religion import *
from research import *

import events
import event_analysis

from math import *

from Tkinter import *

CITY_CELL_POPULATION_CAPACITY = 1000
SURROUNDING_CELL_POPULATION_CAPACITY = 10

BASE_CELL_FOOD_PRODUCTION = 30
BASE_CELL_MIN_FOOD_PRODUCTION = 30

FOOD_PER_PERSON = 1

MORALE_NOT_ENOUGH_FOOD = 4
CAPITAL_CITY_MORALE_BONUS = 2
OFFICE_MORALE_BONUS = 4
MORALE_INCREMENT = 30

NATION_COLORS = ['dark orange', 'cadet blue', 'sea green', 'gold', 'deep sky blue',\
                 'firebrick', 'dark salmon', 'maroon', 'sienna', 'dark slate blue',\
                 'deep pink', 'dark orchid', 'slate gray', 'violet',\
                 'navy', 'magenta', 'sandy brown', 'saddle brown', 'medium spring green',\
                 'orchid', 'blue', 'lawn green', 'violet red',\
                 'medium slate blue', 'purple', 'lime green', 'chartreuse', 'blue violet',\
                 'dark sea green', 'hot pink', 'orange', 'indian red', 'medium sea green',\
                 'red', 'brown', 'dim gray', 'salmon',\
                 'steel blue', 'royal blue', 'medium purple', 'spring green',\
                 'dark slate gray', 'dark olive green', 'cyan', 'chocolate', 'orange red', 'tan',\
                 'dark green', 'tomato', 'gray', 'cornflower blue', 'goldenrod', \
                 'midnight blue', 'rosy brown', 'plum', 'sky blue',\
                 'dark violet', 'dark khaki', 'burlywood', 'green', 'olive drab', 'medium turquoise',\
                 'slate blue', 'powder blue', 'aquamarine']

OFFICE_MODIFIERS = ['tax_rate', 'army_spending', 'morale']
OFFICE_MODIFIER_MAX = 2

MODIFIERS = ["Grand", "Federated", "Democratic", "People's", "Free", "Illustrious", "Glorious", "United"]
GOVERNMENT_TYPES = ["Principality", "Commonwealth", "Kingdom", "Hegemony", "Khanate", "Socialist State", "Sultanate", "Republic", "Democracy", "Theocracy", "Confederacy", "Oligarchy", "Aristocracy", "Meritocracy", "States"]
INIT_CITY_COUNT = 1

CITY_FOUND_COST = 100000
SOLDIER_RECRUIT_COST = 1000
SOLDIER_UPKEEP = 20

TAX_MULTIPLIER = 10

AVERAGE_MAX_LIFE_EXPECTANCY = 60

NAME_SWITCH_THRESHOLD = 20

#Years
MIN_TERM_LENGTH = 5
MAX_TERM_LENGTH = 20

#Chances (1 in x)
LOSE_PLACE_CITY_NAME = 10 #Only applies if the nation no longer owns the city.
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

#Building effects: population_capacity, tax_rate, food_output, money_output
house_effects = {'population_capacity': 100, 'tax_rate': 1.001, 'cost': 100}
farm_effects = {'population_capacity': 10, 'food_output': 100, 'cost': 200}
fishery_effects = {'population_capacity': 5, 'food_output': 150, 'cost': 200}
ranch_effects = {'population_capacity': 5, 'food_output': 200, 'cost': 300}
mine_effects = {'population_capacity': 20, 'money_output': 500, 'cost': 600}
market_effects = {'tax_rate': 1.01, 'money_output': 1000, 'cost': 1500}

class Building:
    def __init__(self, name, city, effects, number):
        self.name = name
        self.city = city

        self.effects = effects
        self.number = number

    def get_cost(self):
        return self.effects['cost']

    def get_population_capacity(self):
        if 'population_capacity' in self.effects:
            return self.effects['population_capacity'] * self.number
        else:
            return 0

    def get_tax_rate(self):
        if 'tax_rate' in self.effects:
            return self.effects['tax_rate'] ** self.number
        else:
            return 1

    def get_food_output(self):
        if 'food_output' in self.effects:
            return self.effects['food_output'] * self.number
        else:
            return 0

    def get_money_output(self):
        if 'money_output' in self.effects:
            return self.effects['money_output'] * self.number
        else:
            return 0

class City:
    def __init__(self, nation, name, (x, y), parent):
        self.name = name
        self.name_id = -1 #The id of the label that displays this cities name

        self.parent = parent

        self.population = 10
        self.population_capacity = 10

        self.nation = nation

        self.age = 0

        self.food = 0

        self.owned_cells = []
        self.surrounding_cells = []

        self.position = (utility.clamp(x + random.randint(-10, 10), utility.S_WIDTH // utility.CELL_SIZE - 1, 0), utility.clamp(y + random.randint(-10, 10), utility.S_HEIGHT // utility.CELL_SIZE - 1, 0))

        self.army = None

        self.buildings = []
        self.buildings.append(Building('House', self, house_effects, 0))
        self.buildings.append(Building('Farm', self, farm_effects, 0))
        self.buildings.append(Building('Fishery', self, fishery_effects, 0))
        self.buildings.append(Building('Ranch', self, ranch_effects, 0))
        self.buildings.append(Building('Mine', self, mine_effects, 0))
        self.buildings.append(Building('Market', self, market_effects, 0))

        if self.parent.cells[self.position[0]][self.position[1]].owner != None:
            self.destroy = True
        else:
            self.destroy = False

        self.is_capital = False

        self.gui_window = None

        self.merges = []

    #Creates a new window showing basic information about itself
    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title(self.name)
        self.gui_window.geometry("500x375+0+0")

        self.gui_window.columnconfigure(2, weight=1)

        x, y = self.get_average_position()
        self.position_label = Label(self.gui_window, text='Position: ({}, {})'.format(x, y))
        self.position_label.grid(row=0, sticky=W)

        self.size_label = Label(self.gui_window, text='Size: {}'.format(self.total_cell_count()))
        self.size_label.grid(row=1, sticky=W)

        self.food_label = Label(self.gui_window, text='Food: {}'.format(self.food))
        self.food_label.grid(row=2, sticky=W)

        self.population_label = Label(self.gui_window, text='Population: {} of {}'.format(self.population, self.calculate_population_capacity()))
        self.population_label.grid(row=3, sticky=W)

        self.army_label = Label(self.gui_window, text='Army: {}'.format(self.army.size()))
        self.army_label.grid(row=4, sticky=W)

        self.buildings_display = Listbox(self.gui_window)

        for building in self.buildings:
            self.buildings_display.insert(END, '{}: {}'.format(building.name, building.number))

        self.buildings_display.grid(row=4, column=1, columnspan=3, sticky=W+E)

        self.nation_label = Label(self.gui_window, text='Nation: ')
        self.nation_label.grid(row=5, sticky=W)

        self.nation_button = Button(self.gui_window, text=self.nation.name, command=self.nation.show_information_gui)
        self.nation_button.grid(row=5, column=1, sticky=W)

        all_events = event_analysis.find_city_mentions([self.name] + self.merges)
        all_events = all_events.search('name', r'Attack|CityFounded|CityMerged')
        all_events = sorted(all_events.event_list, key=lambda event: event.date)

        self.event_log_display = Listbox(self.gui_window)

        for event in all_events:
            self.event_log_display.insert(END, event.text_version())

        self.event_log_display.grid(row=6, column=0, columnspan=3, rowspan=10, sticky=W+E)

    #population_capacity, tax_rate, food_output, money_output

    def make_capital(self):
        self.is_capital = True

    def get_buildings(self, building_name):
        for i in self.buildings:
            if i.name == building_name:
                return i

        return None

    def combine_cities(self, other):
        if self.destroy: #We can't merge if we're about to be destroyed, that doesn't make any sense
            return

        while len(other.owned_cells) > 0:
            other.owned_cells[0].change_owner(self)

        while len(other.surrounding_cells) > 0:
            other.surrounding_cells[0].change_owner(self)

        self.population += other.population
        self.army.add_army(other.army)

        self.food += other.food

        for building in self.buildings:
            other_building = other.get_buildings(building.name)
            if other_building != None:
                building.number += other_building.number

        for merge in other.merges:
            self.merges.append(merge)

        self.merges.append(other.name)

        self.parent.events.append(events.EventCityMerged('CityMerged', {'nation_a': self.nation.id, 'city_a': self.name, 'city_b': other.name}, self.parent.get_current_date()))
        print(self.parent.events[-1].text_version())

        other.destroy = True

    def capture(self, attacking_army, new_nation):
        #Old nation loses the city and morale
        original_cities = len(self.nation.cities)
        if self in self.nation.cities: #should be, but just to be sure
            self.nation.cities.remove(self)
        else:
            raise Exception('{} not in {}'.format(self.name, map(lambda c: c.name, self.nation.cities)))
            return

        if original_cities == len(self.nation.cities):
            raise Exception('{} was not removed from {}.'.format(self.name, map(lambda c: c.name, self.nation.cities)))
            return

        #If there is an army still here, we should send it away first, instead of just deleting it from existence.
        if self.army.size() > 0:
            if len(self.nation.cities) > 0: #this shouldn't happen because the army should fight to the death first
                return_destination = random.choice(self.nation.cities)
                self.nation.moving_armies.append(Group(self.nation.name, self.army, self.position, return_destination.position, self.nation.color, lambda s, c: False, self.parent.reinforce(self.nation, return_destination), self.parent.canvas))

                self.parent.events.append(events.EventArmyDispatched('ArmyDispatched', {'nation_a': self.nation.id, 'nation_b': self.nation.id, 'city_a': self.name, 'city_b': return_destination.name, 'reason': 'evacuate', 'army_size': self.army.size()}, self.parent.get_current_date()))

        if self.is_capital: #We lose twice as much morale for losing the capital
            self.nation.mod_morale(-MORALE_INCREMENT * CAPITAL_CITY_MORALE_BONUS)
        else:
            self.nation.mod_morale(-MORALE_INCREMENT)

        # print('TAKENCITY: {} ({}, {}), ({})'.format(self.nation.name, original_cities, len(self.nation.cities), new_nation.name, len(new_nation.cities)))

        self.nation = new_nation
        self.nation.cities.append(self)

        #Gain twice as much morale for capturing the enemies capital
        if self.is_capital:
            self.nation.mod_morale(MORALE_INCREMENT * CAPITAL_CITY_MORALE_BONUS)
        else:
            self.nation.mod_morale(MORALE_INCREMENT)

        #Switch the cells to the new color/anything else that needs to be done
        for cell in self.owned_cells:
            cell.update_self()

        for cell in self.surrounding_cells:
            cell.update_self()

        self.is_capital = False

        self.army = attacking_army

    def destroy_self(self):
        for cell in self.owned_cells:
            cell.change_owner(None)

        for cell in self.surrounding_cells:
            cell.change_owner(None)

        #We don't want any lingering city names on the map
        if self.name_id > 0:
            self.parent.canvas.delete(self.name_id)

        if self in self.nation.cities:
            self.nation.cities.remove(self)

        del self

    def remove_cell(self, cell):
        if cell in self.owned_cells:
            self.owned_cells.remove(cell)
        elif cell in self.surrounding_cells:
            self.surrounding_cells.remove(cell)
        else:
            raise 'Cell ({}, {}) not in either list of cells.'.format(cell.x, cell.y)

    def add_cell(self, cell):
        if cell.type == 'surrounding':
            self.surrounding_cells.append(cell)
        elif cell.type == 'city':
            self.owned_cells.append(cell)
        else:
            raise 'Unknown cell type: {}'.format(cell.type)

    def get_center(self):
        return (self.position[0], self.position[1])

    def calculate_population_capacity(self):
        self.population_capacity = len(self.owned_cells) * CITY_CELL_POPULATION_CAPACITY
        self.population_capacity += len(self.surrounding_cells) * SURROUNDING_CELL_POPULATION_CAPACITY

        for i in self.buildings:
            self.population_capacity += i.get_population_capacity()

        return self.population_capacity

    def get_expansion_candidates(self):
        result = []

        for cell in self.owned_cells + self.surrounding_cells:
            for neighbor in cell.neighbors():
                if neighbor.owner == None:
                    #It's okay if the cell is in there multiple times. It makes more sense that you'd be more likely to take that cell
                    result.append(neighbor)
                elif neighbor.owner.nation != self.nation: #If there is a nation neighboring one of our cities
                    #we must either be at war with them, or be their trading partner.
                    if not neighbor.owner.nation in self.nation.trading and not neighbor.owner.nation in self.nation.at_war:
                        if neighbor.owner.nation.religion == self.nation.religion: #If they're our religion, we'll just trade
                            self.parent.start_trade_agreement(self.nation, neighbor.owner.nation)
                        else:
                            #Those heathen scum must die.
                            if random.randint(0, 10 * self.nation.get_tolerance()) == 0:
                                self.parent.start_war(self.nation, neighbor.owner.nation, is_holy_war=True)
                            elif random.randint(0, 2) == 0: #Those bastards have stuff we want
                                self.parent.start_war(self.nation, neighbor.owner.nation, is_holy_war=False)
                            else: #Nah jk let's just trade.
                                self.parent.start_trade_agreement(self.nation, neighbor.owner.nation)
                elif neighbor.owner != self and neighbor.owner.nation == self.nation: #It's not a neighboring nation, but it is a neighboring city, so we'll merge together with it.
                    self.combine_cities(neighbor.owner)

                    #Use the newly combined lists of cells to determine the result now.
                    return self.get_expansion_candidates()

        return result

    def total_cell_count(self):
        return len(self.owned_cells) + len(self.surrounding_cells)

    def get_average_position(self):
        #This shouldn't happen, but in case it does
        if self.total_cell_count() == 0:
            return self.position

        x = 0
        y = 0

        for cell in self.owned_cells + self.surrounding_cells:
            x += cell.x
            y += cell.y

        return (x // self.total_cell_count(), y // self.total_cell_count())

    def remake_display_name(self):
        self.parent.canvas.delete(self.name_id)
        self.name_id = -1

        self.handle_display_name()

    def handle_display_name(self):
        x, y = self.get_average_position()
        x = x * utility.CELL_SIZE
        y = y * utility.CELL_SIZE

        if self.name_id == -1:
            self.name_id = self.parent.canvas.create_text(x, y - utility.CELL_SIZE, text=self.name)
        else:
            self.parent.canvas.coords(self.name_id, x, y - utility.CELL_SIZE)
            self.parent.canvas.itemconfig(self.name_id, text='{}: {}/{}, {}'.format(self.name, self.population, self.calculate_population_capacity(), self.army.size()))

    #We'll get rid of cells or transform city cells back into surroundings cells
    def handle_abandonment(self):
        if self.calculate_population_capacity() == 0:
            self.destroy = True
            return

        #Less than 50% of our capacity is filled, then remove some squares.
        if float(self.population) / float(self.calculate_population_capacity()) < 0.5:
            if len(self.owned_cells) > 0:
                converted_cell = random.choice(self.owned_cells)

                self.surrounding_cells.append(converted_cell)
                self.owned_cells.remove(converted_cell)

                converted_cell.change_type('surrounding')
            elif len(self.surrounding_cells) > 1: #Make sure we always have at least one cell left
                removed_cell = random.choice(self.surrounding_cells)

                removed_cell.change_owner(None)
            else: #If we're about to lose the last square, then just destroy the whole city.
                self.destroy = True
                return

    def handle_disconnected_cells(self):
        if self.total_cell_count() == 1: #If there's more than one cell, we need to check for disconnected cells and remove them if necessary.
            return

        for cell in self.owned_cells + self.surrounding_cells:
            has_owned_neighbor = False
            for neighbor in cell.neighbors():
                if neighbor.owner == self:
                    has_owned_neighbor = True
                    break

            if not has_owned_neighbor:
                cell.change_owner(None)

    def mod_food(self, amount):
        self.food = int(self.food + amount * self.nation.get_food_bonus())

    def handle_food(self):
        food_max_spoilage = int(sqrt(self.food) * sqrt(self.age) * sqrt(self.total_cell_count()))
        if food_max_spoilage > 0:
            self.food = max(0, self.food - random.randint(1, food_max_spoilage))

        for surrounding_cell in self.surrounding_cells:
            self.mod_food(random.randint(BASE_CELL_MIN_FOOD_PRODUCTION, BASE_CELL_FOOD_PRODUCTION))

        for i in self.buildings:
            self.food += i.get_food_output()

        #It takes 1 food to feed each person
        self.food -= self.population * FOOD_PER_PERSON

        if self.army != None:
            self.food -= self.army.size() * FOOD_PER_PERSON

        #There wasn't enough food for everybody.
        if self.food < 0:
            #These people die. Or wander off. Who cares. They've gone.
            losses = -self.food // FOOD_PER_PERSON #Negative because the food value is less than zero
            army_losses = random.randint(1, int(sqrt(losses) + 1))

            #Remove some random amount of troops.
            #Not all desert, because they're hopefully more disciplined than that.
            self.army.remove_number('', army_losses)

            losses -= army_losses

            if losses > 0:
                population_losses = random.randint(0, losses) #Not everybody immediately starves when there isn't enough food.

                self.population = utility.clamp(self.population - population_losses, self.population, 1) #can't be fewer than one person

            self.food = 0

            self.handle_abandonment()

            self.nation.mod_morale(-MORALE_NOT_ENOUGH_FOOD)
        else:
            self.nation.mod_morale(MORALE_NOT_ENOUGH_FOOD)

    def handle_money(self):
        total_tax_rate = self.nation.get_tax_rate() * utility.product([building.get_tax_rate() for building in self.buildings])

        self.nation.money += total_tax_rate * self.get_tax_score()

        for building in self.buildings:
            self.nation.money += building.get_money_output()

    def building_count(self):
        return sum([building.number for building in self.buildings])

    def history_step(self, nation):
        self.handle_display_name()
        self.handle_disconnected_cells()

        if self.population < self.calculate_population_capacity():
            self.population += int(random.random() * self.population) + 1
        elif self.population > self.calculate_population_capacity():
            self.population -= int(random.random() * (self.population - self.population_capacity))
            self.population = max(self.population, 1)

        #Handle the expansion of the city.
        city_cell_expand = max(1, max(20 - len(self.surrounding_cells), len(self.owned_cells)**3 - len(self.surrounding_cells)))
        if random.randint(0, city_cell_expand) == 0: #Expand the city if possible/desired
            candidate_expansion_squares = self.surrounding_cells

            if len(candidate_expansion_squares) > 0:
                new_square = random.choice(candidate_expansion_squares)

                self.surrounding_cells.remove(new_square)
                self.owned_cells.append(new_square)

                new_square.change_type('city')

        if random.randint(0, len(self.surrounding_cells)) < self.age // 2: #Add new surrounding land
            candidate_expansion_squares = self.get_expansion_candidates()

            if len(candidate_expansion_squares):
                new_square = random.choice(candidate_expansion_squares)

                new_square.change_owner(self, 'surrounding')

        self.handle_food()
        self.handle_money()

        for i in xrange(int(sqrt(self.population))):
            improvement_chance = self.building_count() // (int(log(self.population)) + 1)
            if improvement_chance > 0:
                if random.randint(0, improvement_chance) == 0:
                    build_building = utility.weighted_random_choice(self.buildings, weight=lambda _, v: v.get_cost() // 100, reverse=True)

                    if self.nation.money > build_building.get_cost():
                        self.nation.money -= build_building.get_cost()
                        build_building.number += 1

        if not self.army:
            self.army = nation.army_structure.zero()

        self.calculate_population_capacity()

        #This is the number of recruits, it remains to be seen if we can pay for all of them
        conscripted = int(random.random() * self.population / 6 * self.nation.get_conscription_bonus())
        max_soldiers = int(self.nation.money / self.nation.get_soldier_cost(self.army.name) * self.nation.get_army_spending())

        if conscripted > max_soldiers: #If we are recruiting more than we can afford, reduce the number
            conscripted = max_soldiers

        #Pay for soldiers
        self.nation.money -= conscripted * SOLDIER_RECRUIT_COST

        if self.nation.money > self.army.size() * self.nation.get_soldier_upkeep(self.army.name):
            self.nation.money -= self.army.size() * self.nation.get_soldier_upkeep(self.army.name)
        else:
            # print('Not enough money for upkeep, removing {} soldiers!'.format(int((self.army.size() * self.nation.get_soldier_upkeep(self.army.name) - self.nation.money) / self.nation.get_soldier_upkeep(self.army.name))))
            self.army.remove_number('', int((self.army.size() * self.nation.get_soldier_upkeep(self.army.name) - self.nation.money) / self.nation.get_soldier_upkeep(self.army.name)))

            self.nation.money = 0

        self.population -= conscripted
        self.population = max(self.population, 1)

        if not self.army:
            self.army = self.nation.army_structure.zero()

        self.army.add_number(conscripted, self.nation)

        if not self.nation.army_structure.make_upgrade_list() == self.army.zero().make_upgrade_list():
            self.nation.army_structure = self.nation.army_structure.merge_structure(self.army).zero()
            self.army.merge_all(self.nation.army_structure)

        self.age += 1

    def get_tax_score(self):
        return self.population * (1.0 + log(self.building_count() + 1))

    def __repr__(self):
        result = ""

        result += "{}({}): Pop/Pop Capacity/Size: {} / {} / {}; Improvements: {}\n".format(self.name, self.age, self.population, self.calculate_population_capacity(), self.total_cell_count(), self.building_count())

        return result

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
        parent_cities_names= map(lambda city: city.name, parent.cities)

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

        x, y = random.randint(100, utility.S_WIDTH - 100), random.randint(100, utility.S_HEIGHT - 100)

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

        self.army_structure = Troop.init_troop(self.language.make_word(self.language.name_length, True))

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
        return self.tax_rate * utility.product([office.get_modifier('tax_rate') for office in self.offices])

    def get_army_spending(self):
        return self.army_spending * utility.product([office.get_modifier('army_spending') for office in self.offices])

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
                nation.money += 20000

                self.money += 20000
            else:
                self.money += 10000

        return f

    def group_step(self):
        for caravan in self.caravans:
            caravan.step(self.caravans)

    def grow_population(self):
        for city in self.cities:
            if not city.destroy: #Dpnt' simualte cities that are marked for destruction
                city.history_step(self)

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

    def create_city(self, name=''):
        if name == '':
            name = self.language.make_name_word()
        self.cities.append(City(self, name, self.get_average_city_position(), self.parent))

        self.chance_add_new_name(self.cities[-1].name)

        print("{}: A new city was founded in the nation of {}, called {}".format(self.parent.get_current_date(), self.name, self.cities[-1].name))
        self.parent.events.append(events.EventCityFounded('CityFounded', {'nation_a': self.id, 'city_a': self.cities[-1].name}, self.parent.get_current_date()))

        self.cities[-1].army = self.army_structure.copy().zero()

        self.money -= CITY_FOUND_COST

        self.mod_morale(MORALE_INCREMENT)

        if self.parent.cells[self.cities[-1].position[0]][self.cities[-1].position[1]].owner == None:
            self.parent.change_cell_ownership(self.cities[-1].position[0], self.cities[-1].position[1], self.cities[-1], new_type='surrounding')

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

    def get_food_bonus(self):
        mult_mod = 1.0
        add_mod = 0.0
        res = self.tech.get_tech('Improved Agriculture')
        if res != None:
            mult_mod *= res.effect_strength
        return GOVERNMENT_TYPE_BONUSES[self.name.government_type]['food'] * mult_mod + add_mod

    def get_efficiency_bonus(self):
        return GOVERNMENT_TYPE_BONUSES[self.name.government_type]['efficiency']

    def get_morale_bonus(self):
        return GOVERNMENT_TYPE_BONUSES[self.name.government_type]['morale']

    def get_conscription_bonus(self):
        return GOVERNMENT_TYPE_BONUSES[self.name.government_type]['conscription']

    def get_soldier_cost(self, name):
        return SOLDIER_RECRUIT_COST

    def get_soldier_upkeep(self, name):
        return SOLDIER_UPKEEP

    def mod_morale(self, amount):
        if amount > 0:
            amount = amount * self.get_morale_bonus()
        else:
            amount = amount / self.get_morale_bonus()

        self.morale = int(self.morale + amount * self.get_morale_bonus())

    def history_step(self, main):
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
                new_capital = utility.weighted_random_choice(self.cities, weight=lambda i, v: v.population)

                new_capital.make_capital()
        else:
            self.mod_morale(CAPITAL_CITY_MORALE_BONUS)

        for city in self.cities:
            if random.randint(0, max([1, len(self.cities)**10 / max([1, city.population])])) == 0 and (self.money > CITY_FOUND_COST * len(self.cities)): #We need enough money
                self.create_city()

            if self.current_research == None or self.current_research.is_unlocked():
                if self.current_research != None and self.current_research.is_unlocked():
                    main.events.append(events.EventTechResearch('TechResearch', {'nation_a': self.id, 'tech_a': self.current_research.name}, main.get_current_date()))

                    print(main.events[-1].text_version())
                available = self.tech.get_available_research()

                if len(available) > 0:
                    self.current_research = random.choice(available)
                else: #There's nothing left to research
                    self.current_research = None
            else:
                self.current_research.do_research(log(city.population + 1))

        self.religion.history_step(self.parent)

        self.age += 1

        for office in self.offices:
            self.mod_morale(int(office.get_modifier('morale') * OFFICE_MORALE_BONUS))

        #More cities means less happiness
        self.mod_morale(-(len(self.cities) + 1))

    def __repr__(self):
        return '{} ({}): ${}; Pop: {}'.format(self.name.short_name(), self.color, int(self.money), sum([i.population for i in self.cities]))
