import internal.events as events
import internal.event_analysis as event_analysis
import internal.gui as gui
import internal.utility as utility

import math
import random

from Tkinter import *

from civil.city_header import CityHeader
from civil.resources import base_resources, base_resource_prices
from internal.group.caravan import Caravan
from internal.group.group import Group

CELL_POPULATION_CAPACITY = 10

FOOD_PER_PERSON = 1

# The chance that a new person will create a whole new religion
CREATE_RELIGION_CHANCE = 50000

MORALE_NOT_ENOUGH_FOOD = 12
MORALE_NOT_ENOUGH_HOUSING = 2
MORALE_ENOUGH_FOOD = 2
CAPITAL_CITY_MORALE_BONUS = 2  # Multiplier
MORALE_INCREMENT = 30
GARRISON_MORALE_BONUS = 2.5  # Multiplier

SEND_CARAVAN_CHANCE = 10
CARAVAN_RELIGION_CHANCE = 10


class City:
    def __init__(self, nation, name, cell, parent):
        self.name = name
        self.name_id = -1  # The id of the label that displays this cities name

        self.parent = parent

        self.id = self.parent.get_next_id('city')

        self.population = 10
        self.population_capacity = 10

        self.nation = nation

        self.age = 0

        self.morale = 0

        self.cells = []

        self.position = (cell.x, cell.y)

        self.army = None

        self.resources = base_resources()
        self.resource_prices = base_resource_prices()
        self.consumed_resources = base_resources()
        self.produced_resources = base_resources()

        if self.parent.cells[self.position[0]][self.position[1]].owner is not None:
            self.destroy = True
        else:
            self.destroy = False

        self.is_capital = False

        self.gui_window = None

        self.merges = []

        self.caravans = []

        self.city_header = CityHeader(self)

        # self.can_build_boats = False

    def save(self, path):
        res = {'name': self.name, 'population': self.population, 'nation': self.nation.id, 'age': self.age,
               'morale': self.morale, 'cells': map(lambda cell: cell.id, self.cells), 'army': self.army.get_info(),
               'resources': self.resources, 'resource_prices': self.resource_prices,
               'consumed_resources': self.consumed_resources, 'produced_resources': self.produced_resources,
               'is_capital': self.is_capital, 'merges': self.merges,
               'caravans': map(lambda caravan: caravan.get_info(), self.caravans)}

        with open(path + self.name + '.txt', 'w') as f:
            f.write(str(res))

    # Creates a new window showing basic information about itself
    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title(self.name)
        self.gui_window.geometry("600x375+0+0")
        self.gui_window.config(background='white')

        self.gui_window.columnconfigure(2, weight=1)

        x, y = self.get_average_position()
        self.position_label = gui.Label(self.gui_window, text='Position: ({}, {})'.format(x, y))
        self.position_label.grid(row=0, sticky=W)

        self.resources_display = Listbox(self.gui_window)

        for resource in self.resources:
            self.resources_display.insert(END, '{}: {}'.format(resource, self.resources[resource]))

        self.resources_display.config(height=len(self.resources))
        self.resources_display.grid(row=0, column=1, rowspan=4, columnspan=3, sticky=N + S + W + E)

        self.size_label = gui.Label(self.gui_window, text='Size: {}'.format(self.total_cell_count()))
        self.size_label.grid(row=1, sticky=W)

        self.population_label = gui.Label(self.gui_window, text='Population: {} of {}'.format(self.population,
                                                                                              self.calculate_population_capacity()))
        self.population_label.grid(row=3, sticky=W)

        self.army_label = gui.Label(self.gui_window, text='Army: {}'.format(self.army.size()))
        self.army_label.grid(row=4, sticky=W)

        self.morale_label = gui.Label(self.gui_window, text='Morale: {}'.format(self.morale))
        self.morale_label.grid(row=5, sticky=W)

        self.buildings_display = Listbox(self.gui_window)

        self.building_counts = {}

        for cell in self.cells:
            for building in cell.buildings:
                if building.name in self.building_counts:
                    self.building_counts[building.name] += building.number
                else:
                    self.building_counts[building.name] = building.number

        for building in self.building_counts:
            self.buildings_display.insert(END, '{}: {}'.format(building, self.building_counts[building]))

        self.buildings_display.grid(row=4, column=1, columnspan=3, rowspan=2, sticky=W + E)

        self.nation_label = gui.Label(self.gui_window, text='Nation: ')
        self.nation_label.grid(row=6, sticky=W)

        self.nation_button = gui.Button(self.gui_window, text=self.nation.name,
                                        command=self.nation.show_information_gui)
        self.nation_button.grid(row=6, column=1, sticky=W)

        all_events = event_analysis.find_city_mentions(self.parent.event_log, [self.name] + self.merges)
        all_events = all_events.search('name', r'Attack|CityFounded|CityMerged')
        all_events = sorted(all_events.event_list, key=lambda event: event.date)

        self.event_log_display = Listbox(self.gui_window)

        for event in all_events:
            self.event_log_display.insert(END, event.text_version())

        self.event_log_display.grid(row=7, column=0, columnspan=3, rowspan=10, sticky=W + E)

    def get_religion_populations(self):
        res = []

        for religion in self.parent.religions:
            if self.name in religion.adherents:
                res.append((religion, religion.adherents[self.name]))

        return res

    def handle_religious_conversion(self, converting_religion, magnitude):
        for (check_religion, adherents) in self.get_religion_populations():
            if check_religion != converting_religion:
                converted_population = min(adherents, random.randint(0, magnitude))

                self.handle_population_change(-converted_population)

                if self.name in converting_religion.adherents:
                    converting_religion.adherents[self.name] += converted_population
                else:
                    converting_religion.adherents[self.name] = converted_population

    def handle_caravans(self):
        if random.randint(0, SEND_CARAVAN_CHANCE) == 0:
            self.send_caravan()

        for cell in self.cells:
            for building in cell.buildings:
                for caravan in xrange(building.send_caravans()):
                    self.send_caravan()

    def get_resource_differences(self, other):
        res = {}

        for resource in self.resources:
            res[resource] = self.resources[resource] - other.resources[resource]

        return res

    def select_trade_city(self):
        trade_city = None

        if len(self.nation.trading) > 0 and random.randint(0, 2) == 0:
            partner = random.choice(self.nation.trading)

            if len(partner.cities) > 0:
                trade_city = random.choice(partner.cities)

                trade_treaty = self.nation.get_treaty_with(partner, 'trade')
                trade_treaty[self.nation.id]['caravans_sent'] += 1
        else:
            trade_city = random.choice(self.nation.cities)

        return trade_city

    def send_caravan(self):
        cx, cy = self.position

        destination_city = self.select_trade_city()

        if destination_city is None:
            return

        caravan = Caravan(self.parent, self.get_random_religion(), self, destination_city, self.resources['boats'] > 0)
        self.caravans.append(caravan)

    def rearm_army(self, unit):
        self.army.rearm(unit.name, unit.weapons, unit.armor, unit.mount)

    def make_capital(self):
        self.is_capital = True

    def combine_cities(self, other):
        if self.destroy:  # We can't merge if we're about to be destroyed, that doesn't make any sense
            return

        while len(other.cells) > 0:
            other.cells[0].change_owner(self)

        # Combine the religious populations
        for religion in self.parent.religions:
            if other.name in religion.adherents:
                v = religion.adherents.pop(other.name)
                if self.name in religion.adherents:
                    religion.adherents[self.name] += v
                else:
                    religion.adherents[self.name] = v

        self.population += other.population
        self.army.add_army(other.army)

        for resource in self.resources:
            self.resources[resource] += other.resources[resource]

        for merge in other.merges:
            self.merges.append(merge)

        self.merges.append(other.name)

        self.parent.event_log.add_event('CityMerged', {'nation_a': self.nation.id, 'city_a': self.name,
                                                       'city_b': other.name},
                                            self.parent.get_current_date())
        self.parent.write_to_gen_log(self.parent.events[-1].text_version())

        other.destroy = True

    def capture(self, attacking_army, new_nation, attacking_city):
        # Old nation loses the city and morale
        original_cities = len(self.nation.cities)
        if self in self.nation.cities:  # should be, but just to be sure
            self.nation.cities.remove(self)

            # This nation has been completely conquered, transfer its notable people and art
            if len(self.nation.cities) == 0:
                new_nation.culture.combine(self.nation.culture)

                for person in self.nation.notable_people:
                    person.nation = new_nation
                    new_nation.notable_people.append(person)
        else:
            raise Exception('{} not in {}'.format(self.name, map(lambda c: c.name, self.nation.cities)))

        if original_cities == len(self.nation.cities):
            raise Exception('{} was not removed from {}.'.format(self.name, map(lambda c: c.name, self.nation.cities)))

        # If there is an army still here, we should send it away first, instead of just deleting it from existence.
        if self.army.size() > 0:
            if len(self.nation.cities) > 0:  # this shouldn't happen because the army should fight to the death first
                return_destination = random.choice(self.nation.cities)
                self.nation.moving_armies.append(
                    Group(self.parent, self.nation.name, self.army, self.position, return_destination.position,
                          self.nation.color, lambda s: False,
                          self.parent.reinforce(self.nation, return_destination),
                          is_army=True, has_boat=(self.resources['boats'] > 0)))

                self.parent.event_log.add_event('ArmyDispatched', {'nation_a': self.nation.id,
                                                                   'nation_b': self.nation.id,
                                                                   'city_a': self.name,
                                                                   'city_b': return_destination.name,
                                                                   'reason': 'evacuate',
                                                                   'army_size': self.army.size()},
                                                    self.parent.get_current_date())

        if self.is_capital:  # We lose twice as much morale for losing the capital
            self.nation.mod_morale(-MORALE_INCREMENT * CAPITAL_CITY_MORALE_BONUS)
        else:
            self.nation.mod_morale(-MORALE_INCREMENT)

        # print('TAKENCITY: {} ({}, {}), ({})'.format(self.nation.name, original_cities, len(self.nation.cities), new_nation.name, len(new_nation.cities)))

        self.nation = new_nation
        self.nation.cities.append(self)

        # Gain twice as much morale for capturing the enemies capital
        if self.is_capital:
            self.nation.mod_morale(MORALE_INCREMENT * CAPITAL_CITY_MORALE_BONUS)
            self.morale -= MORALE_INCREMENT * CAPITAL_CITY_MORALE_BONUS
        else:
            self.nation.mod_morale(MORALE_INCREMENT)
            self.morale -= MORALE_INCREMENT

        # Switch the cells to the new color/anything else that needs to be done
        for cell in self.cells:
            cell.update_self()

        self.is_capital = False

        self.army = attacking_army

        # This is just the number of levies, which need to be sent home now that we've conquered the enemy.
        if self.army.number > 0 and attacking_city is not None:
            send_army = self.army.zero()
            send_army.add_to(send_army.name, self.army.number)
            self.army.number = 0

            self.nation.moving_armies.append(
                Group(self.parent, self.nation.name, send_army, self.position, attacking_city.position,
                      self.nation.color, lambda s: False, self.parent.return_levies(self.nation, attacking_city),
                      is_army=True))

            self.parent.event_log.add_event('ArmyDispatched', {'nation_a': self.nation.id,
                                                               'nation_b': self.nation.id,
                                                               'city_a': self.name,
                                                               'city_b': attacking_city.name,
                                                               'reason': 'return levies',
                                                               'army_size': send_army.size()},
                                            self.parent.get_current_date())

    def destroy_self(self):
        for cell in self.cells:
            cell.change_owner(None)

        # We don't want any lingering city names on the map
        if self.name_id > 0:
            self.parent.canvas.delete(self.name_id)

        if self in self.nation.cities:
            self.nation.cities.remove(self)

        del self

    def remove_cell(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            raise 'Cell ({}, {}) not in list of cells.'.format(cell.x, cell.y)

    def add_cell(self, cell):
        if cell.type == 'city':
            self.cells.append(cell)
        else:
            raise Exception('Unknown cell type: {}'.format(cell.type))

    def get_center(self):
        return (self.position[0], self.position[1])

    def calculate_population_capacity(self):
        self.population_capacity = len(self.cells) * CELL_POPULATION_CAPACITY

        for cell in self.cells:
            self.population_capacity += cell.get_population_capacity()

        return self.population_capacity

    def get_expansion_candidates(self):
        result = []

        for cell in self.cells:
            for neighbor in cell.neighbors():
                if neighbor.owner is None:
                    if neighbor.terrain.is_settleable():
                        # It's okay if the cell is in there multiple times. It makes more sense that you'd be more
                        # likely to take that cell
                        result.append(neighbor)
                elif neighbor.owner.nation != self.nation:  # If there is a nation neighboring one of our cities
                    # we must either be at war with them, or be their trading partner.
                    if not neighbor.owner.nation in self.nation.trading and not neighbor.owner.nation in self.nation.at_war:
                        if random.randint(0, 10 * self.nation.get_tolerance()) == 0:
                            self.parent.start_war(self.nation, neighbor.owner.nation, is_holy_war=True)
                        elif random.randint(0, 3) == 0:  # Those bastards have stuff we want
                            self.parent.start_war(self.nation, neighbor.owner.nation, is_holy_war=False)
                        else:  # Nah jk let's just trade.
                            self.parent.start_trade_agreement(self.nation, neighbor.owner.nation)
                elif neighbor.owner != self and neighbor.owner.nation == self.nation:
                    # It's not a neighboring nation, but it is a neighboring city, so we'll merge together with it.
                    self.combine_cities(neighbor.owner)

                    # Use the newly combined lists of cells to determine the result now.
                    return self.get_expansion_candidates()

        return result

    def total_cell_count(self):
        return len(self.cells)

    def get_average_position(self):
        # This shouldn't happen, but in case it does
        if self.total_cell_count() == 0:
            return self.position

        x = 0
        y = 0

        for cell in self.cells:
            x += cell.x
            y += cell.y

        return (x // self.total_cell_count(), y // self.total_cell_count())

    def remake_display_name(self):
        self.city_header.remake()

    def handle_display_name(self):
        self.city_header.handle()

    # We'll get rid of cells or transform city cells back into surroundings cells
    def handle_abandonment(self):
        if self.calculate_population_capacity() == 0:
            self.destroy = True
            return

        # Less than 50% of our capacity is filled, then remove some squares.
        if float(self.population) / float(self.calculate_population_capacity()) < 0.5:
            if len(self.cells) > 1:  # Make sure we always have at least one cell left
                removed_cell = random.choice(self.cells)

                removed_cell.change_owner(None)
            else:  # If we're about to lose the last square, then just destroy the whole city.
                self.destroy = True

    def handle_disconnected_cells(self):
        if self.total_cell_count() == 1:  # If there's more than one cell, we need to check for disconnected cells and remove them if necessary.
            return

        for cell in self.cells:
            has_owned_neighbor = False
            for neighbor in cell.neighbors():
                if neighbor.owner == self:
                    has_owned_neighbor = True
                    break

            if not has_owned_neighbor:
                cell.change_owner(None)

    def mod_resource(self, resource, amount):
        multiplier = None
        if resource == 'metal':
            multiplier = self.nation.tech.get_best_in_category('mining')
            if multiplier is not None:
                multiplier = multiplier.effect_strength
        elif resource == 'food':
            multiplier = self.nation.tech.get_best_in_category('agriculture')

            if multiplier is not None:
                multiplier = multiplier.effect_strength * self.nation.get_resource_bonus('food')

        if multiplier is None:
            multiplier = 1.0

        if amount > 0:
            actual_mod = int(multiplier * amount)
            self.produced_resources[resource] += actual_mod
        else:
            actual_mod = int(amount)
            self.consumed_resources[resource] += -actual_mod
        self.resources[resource] += actual_mod

    def handle_food(self):
        food_max_spoilage = int(
            math.sqrt(self.resources['food']) * math.sqrt(self.age) * math.sqrt(self.total_cell_count()))
        if food_max_spoilage > 0:
            self.food = max(0, self.resources['food'] - random.randint(1, food_max_spoilage))

        for cell in self.cells:
            food_amount = cell.get_food_output()

            # print('Was producing {}, now producing {}'.format(prev, food_amount))
            self.mod_resource('food', food_amount)

        # It takes 1 food to feed each person
        self.mod_resource('food', -self.population * FOOD_PER_PERSON)

        if self.army is not None:
            self.mod_resource('food', -self.army.size() * FOOD_PER_PERSON)

        # There wasn't enough food for everybody.
        if self.resources['food'] < 0:
            # These people die. Or wander off. Who cares. They've gone.
            # Negative because the food value is less than zero
            losses = -self.resources['food'] // FOOD_PER_PERSON
            army_losses = random.randint(1, int(math.sqrt(losses) + 1))

            # Remove some random amount of troops.
            # Not all desert, because they're hopefully more disciplined than that.
            self.army.remove_number('', army_losses)

            losses -= army_losses

            if losses > 0:
                population_losses = random.randint(1,
                                                   losses)  # Not everybody immediately starves when there isn't enough food.

                self.handle_population_change(-population_losses)

            self.resources['food'] = 0

            self.handle_abandonment()

            self.morale -= MORALE_NOT_ENOUGH_FOOD
        else:
            self.morale += MORALE_ENOUGH_FOOD

    def get_random_religion(self):
        religion_populations = self.get_religion_populations()
        weight = lambda _, (religion, adherents): adherents
        religion, _ = utility.weighted_random_choice(religion_populations, weight=weight)
        return religion

    def handle_population_change(self, amount):
        original_population = int(self.population)
        self.population = int(max(self.population + amount, 1))  # Can't be fewer than one person in the city

        # Remove religious adherents
        if self.population != original_population:
            lose = original_population > self.population

            pop_change = 0
            if lose:
                pop_change = original_population - self.population
            else:
                pop_change = self.population - original_population

            for i in xrange(pop_change):
                religion = self.get_random_religion()

                if lose:
                    if religion.adherents[self.name] > 0:
                        religion.adherents[self.name] -= 1
                else:
                    if random.randint(0, CREATE_RELIGION_CHANCE) == 0:
                        # Might as well keep track of the founder, eh?
                        self.nation.add_person(role='priest')

                        # Take care of all of these shenanigans.
                        self.parent.create_religion(self, self.nation, founder=self.nation.notable_people[-1])
                        religion.adherents[self.name] += 1
                    else:
                        religion.adherents[self.name] += 1

    def handle_money(self):
        total_tax_rate = utility.product([cell.get_tax_rate() for cell in self.cells])
        final_tax_rate = total_tax_rate * self.nation.get_tax_rate()

        self.nation.money += total_tax_rate * self.get_tax_score()

        for cell in self.cells:
            self.nation.money += cell.get_money_output()

    def handle_resources(self):
        for cell in self.cells:
            production = cell.get_resource_productions()

            for resource in production:
                self.mod_resource(resource, production[resource])

    def handle_train_bonus(self):
        train_bonus = 0

        for cell in self.cells:
            for building in cell.buildings:
                train_bonus += building.get_train_bonus()

        return train_bonus

    def handle_army(self):
        if not self.army:
            self.army = self.nation.army_structure.zero()

        train_bonus = self.handle_train_bonus()

        # This is the number of recruits, it remains to be seen if we can pay for all of them
        conscripted = int(
            (random.random() * 0.2 + 0.2) * self.population ** (2.0 / 3.0) * self.nation.get_conscription_bonus())
        max_soldiers = int(
            self.nation.money / (self.nation.get_soldier_cost(self.army)) * self.nation.get_army_spending())

        # print(self.population, conscripted, max_soldiers)

        if conscripted > max_soldiers:  # If we are recruiting more than we can afford, reduce the number
            conscripted = max_soldiers

        # Pay for new conscripted soldiers
        self.nation.money -= conscripted * self.nation.get_soldier_cost(self.army)

        if self.nation.money > self.army.size() * self.nation.get_soldier_upkeep(self.army):
            self.nation.money -= self.army.size() * self.nation.get_soldier_upkeep(self.army)
        else:
            # print('Not enough money for upkeep, removing {} soldiers!'.format(int((self.army.size() * self.nation.get_soldier_upkeep(self.army.name) - self.nation.money) / self.nation.get_soldier_upkeep(self.army.name))))
            self.army.remove_number('', int((self.army.size() * self.nation.get_soldier_upkeep(
                self.army) - self.nation.money) / self.nation.get_soldier_upkeep(self.army.name)))

            self.nation.money = 0

        self.handle_population_change(-conscripted)

        if not self.army:
            self.army = self.nation.army_structure.zero()

        self.army.add_number(conscripted, self.nation)
        self.army.train(train_bonus)

        if not self.nation.army_structure.make_upgrade_list() == self.army.zero().make_upgrade_list():
            self.nation.army_structure = self.nation.army_structure.merge_structure(self.army).zero()
            self.army.merge_all(self.nation.army_structure)

    def building_count(self):
        return sum([cell.building_count() for cell in self.cells])

    def handle_morale(self):
        if self.morale <= 0:
            if self.army.size() > 0:
                pop_log = math.log(self.population, 3)

                if pop_log != 0:
                    garrison_bonus = math.log(self.army.size(), 2) / pop_log
                    garrison_bonus *= GARRISON_MORALE_BONUS

                    self.morale += garrison_bonus

        if self.population > self.population_capacity:
            self.morale -= MORALE_NOT_ENOUGH_HOUSING

        # TODO: Refactor building effects application to make more consistent (not just here)
        morale_bonus_a = 0
        for cell in self.cells:
            for building in cell.buildings:
                morale_bonus_a += building.get_morale_bonus()

        if self.morale < morale_bonus_a:
            self.morale = morale_bonus_a

    def history_step(self):
        self.consumed_resources = base_resources()
        self.produced_resources = base_resources()

        self.handle_disconnected_cells()

        if self.population < self.calculate_population_capacity():
            t = float(self.resources['food']) / self.population * self.population_capacity / self.population
            rate = 0.005 * t
            new_pop = self.population * (1.0 + rate / 12.0) # + 1
            # print(self.resources['food'], self.population_capacity, self.population, t, rate, new_pop)
            change = new_pop - self.population
            self.handle_population_change(change)

        if random.randint(0, len(self.cells)) < math.sqrt(self.age):  # Add new surrounding land
            candidate_expansion_squares = self.get_expansion_candidates()

            if len(candidate_expansion_squares) > 0:
                new_square = random.choice(candidate_expansion_squares)

                new_square.change_owner(self, 'city')

        self.handle_resources()
        self.handle_food()
        self.handle_money()
        self.handle_army()
        self.handle_morale()
        self.handle_caravans()

        # Because we need to know our producions in order to know what we need to build.
        for cell in self.cells:
            cell.build_buildings()

        self.calculate_population_capacity()

        self.age += 1

        # do this at the end so we have access to the produced resources for the resource indicators
        self.handle_display_name()

    def get_tax_score(self):
        amount = self.population

        for cell in self.cells:
            for building in cell.buildings:
                amount += building.get_tax_score()

        return amount

    def __repr__(self):
        result = ""

        result += "{}({}): Pop/Pop Capacity: {} / {}; Buildings: {}\n".format(self.name, self.age, self.population,
                                                                              self.calculate_population_capacity(),
                                                                              self.building_count())

        return result
