import utility

from martial import *
from language import *
from group import *
from religion import *
from research import *

import ai

import events
import event_analysis

from math import *

from Tkinter import *

CITY_CELL_POPULATION_CAPACITY = 100
SURROUNDING_CELL_POPULATION_CAPACITY = 1

BASE_CELL_FOOD_PRODUCTION = 30
BASE_CELL_MIN_FOOD_PRODUCTION = 30

FOOD_PER_PERSON = 1

MORALE_NOT_ENOUGH_FOOD = 4
CAPITAL_CITY_MORALE_BONUS = 2
MORALE_INCREMENT = 30

#Building effects: population_capacity, tax_rate, food_output, money_output
house_effects = {'population_capacity': 20, 'tax_rate': 1.001, 'cost': 20}
farm_effects = {'population_capacity': 10, 'food_output': 100, 'cost': 200}
fishery_effects = {'population_capacity': 5, 'food_output': 150, 'cost': 200}
ranch_effects = {'population_capacity': 5, 'food_output': 200, 'cost': 300}
leatherworker_effects = {'population_capacity': 5, 'money_output': 100, 'leather': 5, 'cost': 300}
weaver_effects = {'population_capacity': 5, 'money_output': 100, 'cloth': 5, 'cost': 300}
woodcutter_effects = {'population_capacity': 5, 'money_output': 100, 'wood': 5, 'cost': 300}
mine_effects = {'population_capacity': 20, 'money_output': 500, 'metal': 5, 'cost': 600}
lab_effects = {'population_capacity': 5, 'research_rate': 5, 'cost': 1000}
market_effects = {'tax_rate': 1.01, 'money_output': 1000, 'cost': 1500}

def base_resources():
    return {'leather': 0, 'wood': 0, 'cloth': 0, 'metal': 0, 'food': 0}

class Building:
    def __init__(self, name, city, effects, number):
        self.name = name
        self.city = city

        self.effects = effects
        self.number = number

    def produce(self):
        return

    def buy(self):
        return

    def copy(self):
        return Building(self.name, self.city, self.effects, self.number)

    #To be used when the copy is for a different city
    def clean_copy(self, new_city, number=0):
        return Building(self.name, new_city, self.effects, number)

    def __call__(self, new_city=None, number=0):
        if new_city != None:
            return self.clean_copy(new_city, number)
        else:
            return self.copy()

    def get_cost(self):
        return self.effects['cost']

    def get_research_rate(self):
        if 'research_rate' in self.effects:
            return self.effects['research_rate'] * self.number
        else:
            return 0

    def get_population_capacity(self):
        if 'population_capacity' in self.effects:
            amount = self.effects['population_capacity'] * self.number

            multiplier = self.city.nation.tech.get_best_in_category('housing')

            if multiplier != None:
                amount *= multiplier.effect_strength

            return amount
        else:
            return 0

    def get_tax_rate(self):
        if 'tax_rate' in self.effects:
            return self.effects['tax_rate'] ** self.number
        else:
            return 1

    def get_food_output(self):
        if 'food_output' in self.effects:
            amount = self.effects['food_output'] * self.number

            multiplier = self.city.nation.tech.get_best_in_category('agriculture')

            if multiplier != None:
                amount *= multiplier.effect_strength

            return amount
        else:
            return 0

    def get_money_output(self):
        if 'money_output' in self.effects:
            amount = self.effects['money_output'] * self.number
            if self.name == 'Mine':
                multiplier = self.city.nation.tech.get_best_in_category('mining')

                if multiplier != None:
                    amount *= multiplier.effect_strength
            return amount
        else:
            return 0

    def get_resource_productions(self):
        production = base_resources()

        for effect in self.effects:
            if effect in production:
                if effect == 'metal':
                    multiplier = self.city.nation.tech.get_best_in_category('mining')

                    if multiplier != None:
                        production[effect] = int(self.effects[effect] * self.number * multiplier.effect_strength)

                production[effect] = self.effects[effect] * self.number

        return production

class City:
    def __init__(self, nation, name, cell, parent):
        self.name = name
        self.name_id = -1 #The id of the label that displays this cities name

        self.parent = parent

        self.population = 10
        self.population_capacity = 10

        self.nation = nation

        self.age = 0

        self.owned_cells = []
        self.surrounding_cells = []

        self.position = (cell.x, cell.y)

        self.army = None

        self.buildings = []
        self.buildings.append(Building('House', self, house_effects, 0))
        self.buildings.append(Building('Farm', self, farm_effects, 0))
        self.buildings.append(Building('Fishery', self, fishery_effects, 0))
        self.buildings.append(Building('Ranch', self, ranch_effects, 0))
        self.buildings.append(Building('Mine', self, mine_effects, 0))
        self.buildings.append(Building('Leatherworker', self, leatherworker_effects, 0))
        self.buildings.append(Building('Weaver', self, weaver_effects, 0))
        self.buildings.append(Building('Woodcutter', self, woodcutter_effects, 0))
        self.buildings.append(Building('Lab', self, lab_effects, 0))
        self.buildings.append(Building('Market', self, market_effects, 0))

        self.resources = base_resources()

        # self.ai = ai.SupplyDemand(base_resources(), self.buildings, )

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
        self.gui_window.geometry("600x375+0+0")

        self.gui_window.columnconfigure(2, weight=1)

        x, y = self.get_average_position()
        self.position_label = Label(self.gui_window, text='Position: ({}, {})'.format(x, y))
        self.position_label.grid(row=0, sticky=W)

        self.resources_display = Listbox(self.gui_window)

        for resource in self.resources:
            self.resources_display.insert(END, '{}: {}'.format(resource, self.resources[resource]))

        self.resources_display.config(height=len(self.resources))
        self.resources_display.grid(row=0, column=1, rowspan=4, columnspan=3, sticky=N+S+W+E)

        self.size_label = Label(self.gui_window, text='Size: {}'.format(self.total_cell_count()))
        self.size_label.grid(row=1, sticky=W)

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

        for resource in self.resources:
            self.resources[resource] += other.resources[resource]

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

    def capture(self, attacking_army, new_nation, attacking_city):
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

        if self.army.number > 0 and attacking_city != None: #This is just the number of levies, which need to be sent home now that we've conquered them.
            send_army = self.army.zero()
            send_army.add_to(send_army.name, self.army.number)
            self.army.number = 0

            self.nation.moving_armies.append(Group(self.nation.name, send_army, self.position, attacking_city.position, self.nation.color, lambda s, c: False, self.parent.return_levies(self.nation, attacking_city), self.parent.canvas))

            self.parent.events.append(events.EventArmyDispatched('ArmyDispatched', {'nation_a': self.nation.id, 'nation_b': self.nation.id, 'city_a': self.name, 'city_b': attacking_city.name, 'reason': 'return levies', 'army_size': send_army.size()}, self.parent.get_current_date()))

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
                    if neighbor.terrain.is_settleable():
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

    def mod_resource(self, resource, amount):
        self.resources[resource] = int(self.resources[resource] + amount * self.nation.get_resource_bonus('food'))

    def handle_food(self):
        food_max_spoilage = int(sqrt(self.resources['food']) * sqrt(self.age) * sqrt(self.total_cell_count()))
        if food_max_spoilage > 0:
            self.food = max(0, self.resources['food'] - random.randint(1, food_max_spoilage))

        for surrounding_cell in self.surrounding_cells:
            food_amount = random.randint(BASE_CELL_MIN_FOOD_PRODUCTION, BASE_CELL_FOOD_PRODUCTION)
            prev = food_amount
            food_amount *= surrounding_cell.food_production_multiplier()

            # print('Was producing {}, now producing {}'.format(prev, food_amount))
            self.mod_resource('food', food_amount)

        for i in self.buildings:
            self.mod_resource('food', i.get_food_output())

        #It takes 1 food to feed each person
        self.resources['food'] -= self.population * FOOD_PER_PERSON

        if self.army != None:
            self.resources['food'] -= self.army.size() * FOOD_PER_PERSON

        #There wasn't enough food for everybody.
        if self.resources['food'] < 0:
            #These people die. Or wander off. Who cares. They've gone.
            #Negative because the food value is less than zero
            losses = -self.resources['food'] // FOOD_PER_PERSON
            army_losses = random.randint(1, int(sqrt(losses) + 1))

            #Remove some random amount of troops.
            #Not all desert, because they're hopefully more disciplined than that.
            self.army.remove_number('', army_losses)

            losses -= army_losses

            if losses > 0:
                population_losses = random.randint(0, losses) #Not everybody immediately starves when there isn't enough food.

                self.population = utility.clamp(self.population - population_losses, self.population, 1) #can't be fewer than one person

            self.resources['food'] = 0

            self.handle_abandonment()

            self.nation.mod_morale(-MORALE_NOT_ENOUGH_FOOD)
        else:
            self.nation.mod_morale(MORALE_NOT_ENOUGH_FOOD)

    def handle_money(self):
        total_tax_rate = self.nation.get_tax_rate() * utility.product([building.get_tax_rate() for building in self.buildings])

        self.nation.money += total_tax_rate * self.get_tax_score()

        for building in self.buildings:
            self.nation.money += building.get_money_output()

    def handle_resources(self):
        for building in self.buildings:
            production = building.get_resource_productions()

            for resource in production:
                self.resources[resource] += production[resource]

    def handle_army(self):
        if not self.army:
            self.army = nation.army_structure.zero()

        #This is the number of recruits, it remains to be seen if we can pay for all of them
        conscripted = int(random.random() * (self.population)**(2.0/3) * self.nation.get_conscription_bonus())
        max_soldiers = int(self.nation.money / self.nation.get_soldier_cost(self.army.name) * self.nation.get_army_spending())

        if conscripted > max_soldiers: #If we are recruiting more than we can afford, reduce the number
            conscripted = max_soldiers

        #Pay for soldiers
        self.nation.money -= conscripted * self.nation.get_soldier_cost(self.army.name)

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

    def building_count(self):
        return sum([building.number for building in self.buildings])

    def history_step(self):
        self.handle_display_name()
        self.handle_disconnected_cells()

        if self.population < self.calculate_population_capacity():
            self.population += int(random.random() * sqrt(self.population_capacity - self.population)) + 1
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

        for i in xrange(int(sqrt(self.population))):
            improvement_chance = int((self.building_count() + 1) / (sqrt(self.population) + 1))
            if random.randint(0, improvement_chance + 1) == 0:
                build_building = utility.weighted_random_choice(self.buildings, weight=lambda _, building: float(building.get_cost()), reverse=True)

                if self.nation.money > build_building.get_cost():
                    self.nation.money -= build_building.get_cost()
                    build_building.number += 1

        self.handle_food()
        self.handle_money()
        self.handle_resources()
        self.handle_army()

        self.calculate_population_capacity()

        self.age += 1

    def get_tax_score(self):
        return self.population * (1.0 + log(self.building_count() + 1))

    def __repr__(self):
        result = ""

        result += "{}({}): Pop/Pop Capacity: {} / {}; Buildings: {}\n".format(self.name, self.age, self.population, self.calculate_population_capacity(), self.building_count())

        return result
