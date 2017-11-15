import utility

from martial import *
from language import *
from group import *
from religion import *
from research import *
import gui

import events
import event_analysis

import math

from Tkinter import *

CELL_POPULATION_CAPACITY = 10

FOOD_PER_PERSON = 1

# The chance that a new person will create a whole new religion
CREATE_RELIGION_CHANCE = 50000

MORALE_NOT_ENOUGH_FOOD = 12
MORALE_NOT_ENOUGH_HOUSING = 2
MORALE_ENOUGH_FOOD = 2
CAPITAL_CITY_MORALE_BONUS = 2 #Multiplier
MORALE_INCREMENT = 30
GARRISON_MORALE_BONUS = 2.5 #Multiplier

SEND_CARAVAN_CHANCE = 10
CARAVAN_RELIGION_CHANCE = 10

TRADE_GOOD_PRICE = 25

building_effects = {}

building_effects['Farm'] = {'population_capacity': 5, 'food': 60, 'cost': 200, 'size': 15}
building_effects['Tavern'] = {'population_capacity': 5, 'cost': 500, 'money_output': 1200, 'size': 50}
building_effects['Fishery'] = {'population_capacity': 2, 'food': 125, 'cost': 200, 'size': 40}
building_effects['Ranch'] = {'population_capacity': 2, 'food': 125, 'cost': 300, 'size': 50}
building_effects['Hunting Lodge'] = {'population_capacity': 2, 'food': 50, 'cost': 50, 'size': 20}
building_effects['Leatherworker'] = {'population_capacity': 2, 'money_output': 200, 'leather': 5, 'cost': 300, 'size': 15}
building_effects['Weaver'] = {'population_capacity': 2, 'money_output': 200, 'cloth': 5, 'cost': 300, 'size': 15}
building_effects['Woodcutter'] = {'population_capacity': 2, 'money_output': 150, 'wood': 5, 'cost': 300, 'size': 50}
building_effects['Mine'] = {'population_capacity': 8, 'money_output': 1000, 'metal': 3, 'cost': 1000, 'size': 90}
building_effects['Library'] = {'population': 4, 'research_rate': 2, 'cost': 1000, 'size': 90}
building_effects['Lab'] = {'population_capacity': 2, 'research_rate': 5, 'cost': 1000, 'size': 75}
building_effects['Market'] = {'tax_score': 100, 'money_output': 1000, 'cost': 1500, 'size': 60}
building_effects['Caravansary'] = {'population_capacity': 5, 'caravan_chance': 20, 'cost': 2000, 'size': 90}



#Kenny - Additions
building_effects['Small Hut'] = {'population_capacity': 1, 'tax_score': 1, 'cost': 1, 'size': 1}
building_effects['Hut'] = {'population_capacity': 2, 'tax_score': 2, 'cost': 2, 'size': 2}
building_effects['Long Hut'] = {'population_capacity': 4, 'tax_score': 5, 'cost': 5, 'size': 4}

building_effects['Small House'] = {'population_capacity': 5, 'tax_score': 10, 'cost': 10, 'size': 5}
building_effects['House'] = {'population_capacity': 10, 'tax_score': 20, 'cost': 50, 'size': 15}
building_effects['Large House'] = {'population_capacity': 15, 'tax_score': 30, 'cost': 100, 'size': 25}

building_effects['Small Villa'] = {'population_capacity': 20, 'tax_score': 50, 'cost': 200, 'size': 50}
building_effects['Villa'] = {'population_capacity': 25, 'tax_score': 60, 'cost': 400, 'size': 60}
building_effects['Large Villa'] = {'population_capacity': 40, 'tax_score': 70, 'cost': 800, 'size': 70}

building_effects['Manor'] = {'population_capacity': 50, 'tax_score': 80, 'cost': 1600, 'size': 70}
building_effects['Mansion'] = {'population_capacity': 60, 'tax_score': 90, 'cost': 3200, 'size': 80}
building_effects['Castle'] = {'population_capacity': 100, 'weapons':10, 'train_bonus':10, 'tax_score': 100, 'cost': 6400, 'size': 100}

building_effects['Bank'] = {'population_capacity': 8, 'money_output': 3000,  'cost': 1500, 'size': 20}

building_effects['Guildhouse'] = {'population_capacity': 20, 'research_rate': 2, 'caravan_chance': 20, 'money_output': 500, 'cost': 4000, 'size': 50}
building_effects['College'] = {'population_capacity': 20,  'research_rate': 3, 'cost': 3500, 'size': 50}
building_effects['Inn'] = {'population_capacity': 50,  'tax_score': 5, 'money_output':500,'cost': 1000, 'size': 40}
building_effects['Baracks'] = {'population_capacity': 15,  'sergeants':1, 'morale_bonus': 25, 'train_bonus':5, 'weapons':2,'cost': 500, 'size': 30}
building_effects['Blacksmith'] = {'population_capacity': 2,  'weapons': 10, 'cost': 350, 'size': 10}
building_effects['Church'] = {'population_capacity': 5,  'tax_score': 5, 'cost': 200, 'size': 40}
building_effects['Gun Smith'] = {'population_capacity': 5,  'gunpowder': 10, 'weapons':2, 'cost': 700, 'size': 50}
building_effects['Sewer'] = {'population_capacity': 12,  'tax_score': 5, 'morale':25, 'cost': 1200, 'size': 35}
building_effects['Graveyard'] = {'population_capacity': 2,  'morale': -5, 'gunpowder':5,'cost': 100, 'size': 30}
building_effects['Carpenter House'] = {'population_capacity': 3,  'money_output':1000, 'cost': 50, 'size': 10}

building_effects['School of Combat'] = {'population_capacity': 10,  'train_bonus':20, 'weapons': 5, 'sergeants':2,'cost': 900, 'size': 50}
building_effects['Dockyard'] = {'population_capacity': 3, 'wood':-5, 'boats':1,'cost': 2300, 'size': 20}
building_effects['Court'] = {'population_capacity': 6,  'morale_bonus': 25, 'cost': 1500, 'size': 30}
building_effects['Workshop'] = {'population_capacity': 10,  'cloth': 5, 'metal':5, 'wood':5, 'cost': 1700, 'size': 35}

def base_resources():
    return {'leather': 0, 'wood': 0, 'cloth': 0, 'metal': 0, 'food': 0, 'boats':0, 'weapons':0, 'gunpowder':0, 'sergeants':0}

def base_resource_prices():
    return {'leather': 50, 'wood': 75, 'cloth': 50, 'metal': 150, 'food': 10, 'boats':250, 'weapons':80, 'gunpowder':200, 'sergeants':300}

class Building:
    def __init__(self, name, city, effects, number):
        self.name = name
        self.city = city

        self.effects = effects
        self.number = number

    def get_info(self):
        res = {}

        # We don't need to save effects because we have a whole list of those above
        res['name'] = self.name
        res['number'] = self.number

        return res

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

    def get_size(self):
        return self.effects['size']

    def send_caravans(self):
        if 'caravan_chance' in self.effects:
            c = 0
            for i in xrange(self.number):
                if random.randint(0, self.effects['caravan_chance']) == 0:
                    c += 1
            return c
        else:
            return 0

    def get_tax_score(self):
        if 'tax_score' in self.effects:
            return self.effects['tax_score'] * self.number
        else:
            return 0.0

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

    def get_train_bonus(self):
        if 'train_bonus' in self.effects:
            return self.effects['train_bonus'] * self.number
        else:
            return 1

    def get_morale_bonus(self):
        if 'morale_bonus' in self.effects:
            return self.effects['morale_bonus'] * self.number
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
                production[effect] = self.effects[effect] * self.number

        return production

def base_buildings(city):
    buildings = []

    buildings.append(Building('Small Hut', city, building_effects['Small Hut'], 0))
    buildings.append(Building('Hut', city, building_effects['Hut'], 0))
    buildings.append(Building('Long Hut', city, building_effects['Long Hut'], 0))

    buildings.append(Building('Small House', city, building_effects['Small House'], 0))
    buildings.append(Building('House', city, building_effects['House'], 0))
    buildings.append(Building('Large House', city, building_effects['Large House'], 0))

    buildings.append(Building('Small Villa', city, building_effects['Small Villa'], 0))
    buildings.append(Building('Villa', city, building_effects['Villa'], 0))
    buildings.append(Building('Large Villa', city, building_effects['Large Villa'], 0))

    buildings.append(Building('Manor', city, building_effects['Manor'], 0))
    buildings.append(Building('Mansion', city, building_effects['Mansion'], 0))
    buildings.append(Building('Castle', city, building_effects['Castle'], 0))

    buildings.append(Building('Farm', city, building_effects['Farm'], 0))
    buildings.append(Building('Hunting Lodge', city, building_effects['Hunting Lodge'], 0))
    buildings.append(Building('Fishery', city, building_effects['Fishery'], 0))
    buildings.append(Building('Ranch', city, building_effects['Ranch'], 0))
    buildings.append(Building('Tavern', city, building_effects['Tavern'], 0))
    buildings.append(Building('Mine', city, building_effects['Mine'], 0))
    buildings.append(Building('Leatherworker', city, building_effects['Leatherworker'], 0))
    buildings.append(Building('Weaver', city, building_effects['Weaver'], 0))
    buildings.append(Building('Woodcutter', city, building_effects['Woodcutter'], 0))
    buildings.append(Building('Library', city, building_effects['Library'], 0))
    buildings.append(Building('Lab', city, building_effects['Lab'], 0))
    buildings.append(Building('Market', city, building_effects['Market'], 0))
    buildings.append(Building('Caravansary', city, building_effects['Caravansary'],0 ))

    buildings.append(Building('Guildhouse', city, building_effects['Guildhouse'],0 ))
    buildings.append(Building('College', city, building_effects['College'],0 ))
    buildings.append(Building('Inn', city, building_effects['Inn'],0 ))
    buildings.append(Building('Bank', city, building_effects['Bank'],0 ))
    buildings.append(Building('Baracks', city, building_effects['Baracks'],0 ))
    buildings.append(Building('Gun Smith', city, building_effects['Gun Smith'],0 ))
    buildings.append(Building('Church', city, building_effects['Church'],0 ))
    buildings.append(Building('Sewer', city, building_effects['Sewer'],0 ))
    buildings.append(Building('Graveyard', city, building_effects['Graveyard'],0 ))
    buildings.append(Building('Carpenter House', city, building_effects['Carpenter House'],0 ))
    buildings.append(Building('School of Combat', city, building_effects['School of Combat'],0 ))
    buildings.append(Building('Dockyard', city, building_effects['Dockyard'],0 ))
    buildings.append(Building('Court', city, building_effects['Court'],0 ))
    buildings.append(Building('Workshop', city, building_effects['Workshop'],0 ))
    return buildings

class City:
    def __init__(self, nation, name, cell, parent):
        self.name = name
        self.name_id = -1 #The id of the label that displays this cities name

        self.parent = parent

        self.population = 10
        self.population_capacity = 10

        self.nation = nation

        self.age = 0

        self.morale = 0

        #self.conscription_bonus = 0
        self.sergeants = 0

        self.cells = []

        self.position = (cell.x, cell.y)

        self.army = None

        self.resources = base_resources()
        self.resource_prices = base_resource_prices()
        self.consumed_resources = base_resources()
        self.produced_resources = base_resources()

        if self.parent.cells[self.position[0]][self.position[1]].owner != None:
            self.destroy = True
        else:
            self.destroy = False

        self.is_capital = False

        self.gui_window = None

        self.merges = []

        self.caravans = []

        #self.can_build_boats = False

    def save(self, path):
        res = {}
        res['name'] = self.name
        res['population'] = self.population
        res['nation'] = self.nation.id
        res['age'] = self.age
        res['morale'] = self.morale
        res['cells'] = map(lambda cell: cell.id, self.cells)
        res['army'] = self.army.get_info()
        res['resources'] = self.resources
        res['resource_prices'] = self.resource_prices
        res['consumed_resources'] = self.consumed_resources
        res['produced_resources'] = self.produced_resources
        res['is_capital'] = self.is_capital
        res['merges'] = self.merges
        res['caravans'] = map(lambda caravan: caravan.get_info(), self.caravans)

        with open(path + self.name + '.txt', 'w') as f:
            f.write(str(res))

    #Creates a new window showing basic information about itself
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
        self.resources_display.grid(row=0, column=1, rowspan=4, columnspan=3, sticky=N+S+W+E)

        self.size_label = gui.Label(self.gui_window, text='Size: {}'.format(self.total_cell_count()))
        self.size_label.grid(row=1, sticky=W)

        self.population_label = gui.Label(self.gui_window, text='Population: {} of {}'.format(self.population, self.calculate_population_capacity()))
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

        self.buildings_display.grid(row=4, column=1, columnspan=3, rowspan=2, sticky=W+E)

        self.nation_label = gui.Label(self.gui_window, text='Nation: ')
        self.nation_label.grid(row=6, sticky=W)

        self.nation_button = gui.Button(self.gui_window, text=self.nation.name, command=self.nation.show_information_gui)
        self.nation_button.grid(row=6, column=1, sticky=W)

        all_events = event_analysis.find_city_mentions([self.name] + self.merges)
        all_events = all_events.search('name', r'Attack|CityFounded|CityMerged')
        all_events = sorted(all_events.event_list, key=lambda event: event.date)

        self.event_log_display = Listbox(self.gui_window)

        for event in all_events:
            self.event_log_display.insert(END, event.text_version())

        self.event_log_display.grid(row=7, column=0, columnspan=3, rowspan=10, sticky=W+E)

    def get_religion_populations(self):
        res = []

        for religion in self.parent.religions:
            if self.name in religion.adherents:
                res.append((religion, religion.adherents[self.name]))

        return res

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

    def send_caravan(self):
        cx, cy = self.position

        if len(self.nation.trading) > 0 and random.randint(0, 2) == 0:
            partner = random.choice(self.nation.trading)

            if len(partner.cities) > 0:
                trade_city = random.choice(partner.cities)

                trade_treaty = self.nation.get_treaty_with(partner, 'trade')
                trade_treaty[self.nation.id]['caravans_sent'] += 1
            else: # There was a problem, just exit the function.
                return
        else:
            trade_city = random.choice(self.nation.cities)

        # We obviously don't need to send them something if they have more of it than we do.
        resource_diff = self.get_resource_differences(trade_city)
        resource_send = {}

        for resource in resource_diff:
            if resource_diff[resource] > 0:
                resource_send[resource] = random.randint(1, int(resource_diff[resource]))

        # This is to ensure that all caravans make at least some money
        resource_send['trade_goods'] = random.randint(1, int(math.log(self.population))**2 + 1)

	# Each caravan has a random religion.
	religion = self.get_random_religion()

        dx, dy = trade_city.position #Send it to a random city
	self.caravans.append(Group(self.parent, "caravan", (religion, resource_send), (cx, cy), (dx, dy), self.nation.color, lambda s: False, trade_city.receive_caravan(self), self.nation.parent.canvas, has_boat=(self.resources['boats'] > 0)))

    def receive_caravan(self, city):
        def f(caravan):
            caravan_religion, caravan_resources = caravan.members
            city.caravans.remove(caravan)

            # Construct a demand ranking
            consumption_ranking = sorted(self.consumed_resources.items(), key=utility.snd)
            res_count = float(len(consumption_ranking))
            resource_mults = {k: (res_count / 2.0 - i) / res_count for i, (k, v) in enumerate(consumption_ranking)}
            prices = base_resource_prices()

            for resource in prices:
                prices[resource] *= resource_mults[resource]

            profit = 0
            for resource in caravan_resources:
                if resource in prices:
                    profit += caravan_resources[resource] * prices[resource]
                elif resource == 'trade_goods':
                    profit += TRADE_GOOD_PRICE * caravan_resources[resource]

            profit = int(profit)

            # print('{} made a profit of {} while trading {} with {}'.format(city.nation.name.short_name(), profit, caravan_resources, self.nation.name.short_name()))

            self.nation.money += profit

            if city.nation != self.nation: # Trading with ourselves doesn't give any bonus
                city.nation.money += profit // 2 # The senders only makes half as much

                trade_treaty = self.nation.get_treaty_with(city.nation, 'trade')

                if trade_treaty != None: # Although this should always be the case, really.
                    trade_treaty[self.nation.id]['caravans_received'] += 1
                    trade_treaty[self.nation.id]['money'] += profit
                    trade_treaty[city.nation.id]['money'] += profit // 2

    	    # The religion of the caravan influences the religion of this city (but only if they have a different religion than the caravan)
    	    religion_populations = self.get_religion_populations()
    	    for (religion, adherents) in religion_populations:
                if religion != caravan_religion:
                    if random.randint(0,CARAVAN_RELIGION_CHANCE):
                        self.handle_population_change(-1)

                        if self.name in caravan_religion.adherents:
                            caravan_religion.adherents[self.name] += 1
                        else:
                            caravan_religion.adherents[self.name] = 1

        return f

    def rearm_army(self, unit):
        self.army.rearm(unit.name, unit.weapons, unit.armor, unit.mount)

    def make_capital(self):
        self.is_capital = True

    def combine_cities(self, other):
        if self.destroy: #We can't merge if we're about to be destroyed, that doesn't make any sense
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

        self.parent.events.append(events.EventCityMerged('CityMerged', {'nation_a': self.nation.id, 'city_a': self.name, 'city_b': other.name}, self.parent.get_current_date()))
        self.parent.write_to_gen_log(self.parent.events[-1].text_version())

        other.destroy = True

    def capture(self, attacking_army, new_nation, attacking_city):
        #Old nation loses the city and morale
        original_cities = len(self.nation.cities)
        if self in self.nation.cities: #should be, but just to be sure
            self.nation.cities.remove(self)

            # This nation has been completely conquered, transfer its notable people and art
            if len(self.nation.cities) == 0:
                new_nation.culture.combine(self.nation.culture)

                for person in self.nation.notable_people:
                    person.nation = new_nation
                    new_nation.notable_people.append(person)
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
                self.nation.moving_armies.append(Group(self.parent, self.nation.name, self.army, self.position, return_destination.position, self.nation.color, lambda s: False, self.parent.reinforce(self.nation, return_destination), self.parent.canvas, is_army=True, has_boat=(self.resources['boats'] > 0)))
                
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
            self.morale -= MORALE_INCREMENT * CAPITAL_CITY_MORALE_BONUS
        else:
            self.nation.mod_morale(MORALE_INCREMENT)
            self.morale -= MORALE_INCREMENT

        #Switch the cells to the new color/anything else that needs to be done
        for cell in self.cells:
            cell.update_self()

        self.is_capital = False

        self.army = attacking_army

        #This is just the number of levies, which need to be sent home now that we've conquered the enemy.
        if self.army.number > 0 and attacking_city != None:
            send_army = self.army.zero()
            send_army.add_to(send_army.name, self.army.number)
            self.army.number = 0

            self.nation.moving_armies.append(Group(self.parent, self.nation.name, send_army, self.position, attacking_city.position, self.nation.color, lambda s: False, self.parent.return_levies(self.nation, attacking_city), self.parent.canvas, is_army=True))

            self.parent.events.append(events.EventArmyDispatched('ArmyDispatched', {'nation_a': self.nation.id, 'nation_b': self.nation.id, 'city_a': self.name, 'city_b': attacking_city.name, 'reason': 'return levies', 'army_size': send_army.size()}, self.parent.get_current_date()))

    def destroy_self(self):
        for cell in self.cells:
            cell.change_owner(None)

        #We don't want any lingering city names on the map
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
                if neighbor.owner == None:
                    if neighbor.terrain.is_settleable():
                        #It's okay if the cell is in there multiple times. It makes more sense that you'd be more likely to take that cell
                        result.append(neighbor)
                elif neighbor.owner.nation != self.nation: #If there is a nation neighboring one of our cities
                    #we must either be at war with them, or be their trading partner.
                    if not neighbor.owner.nation in self.nation.trading and not neighbor.owner.nation in self.nation.at_war:
                        if random.randint(0, 10 * self.nation.get_tolerance()) == 0:
                            self.parent.start_war(self.nation, neighbor.owner.nation, is_holy_war=True)
                        elif random.randint(0, 3) == 0: #Those bastards have stuff we want
                            self.parent.start_war(self.nation, neighbor.owner.nation, is_holy_war=False)
                        else: #Nah jk let's just trade.
                            self.parent.start_trade_agreement(self.nation, neighbor.owner.nation)
                elif neighbor.owner != self and neighbor.owner.nation == self.nation: #It's not a neighboring nation, but it is a neighboring city, so we'll merge together with it.
                    self.combine_cities(neighbor.owner)

                    #Use the newly combined lists of cells to determine the result now.
                    return self.get_expansion_candidates()

        return result

    def total_cell_count(self):
        return len(self.cells)

    def get_average_position(self):
        #This shouldn't happen, but in case it does
        if self.total_cell_count() == 0:
            return self.position

        x = 0
        y = 0

        for cell in self.cells:
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
            self.parent.canvas.itemconfig(self.name_id, text='{} ({})'.format(self.name, self.population))

    #We'll get rid of cells or transform city cells back into surroundings cells
    def handle_abandonment(self):
        if self.calculate_population_capacity() == 0:
            self.destroy = True
            return

        #Less than 50% of our capacity is filled, then remove some squares.
        if float(self.population) / float(self.calculate_population_capacity()) < 0.5:
            if len(self.cells) > 1: #Make sure we always have at least one cell left
                removed_cell = random.choice(self.cells)

                removed_cell.change_owner(None)
            else: #If we're about to lose the last square, then just destroy the whole city.
                self.destroy = True

    def handle_disconnected_cells(self):
        if self.total_cell_count() == 1: #If there's more than one cell, we need to check for disconnected cells and remove them if necessary.
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
            if multiplier != None:
                multiplier = multiplier.effect_strength
        elif resource == 'food':
            multiplier = self.nation.tech.get_best_in_category('agriculture')

            if multiplier != None:
                multiplier = multiplier.effect_strength * self.nation.get_resource_bonus('food')

        if multiplier == None:
            multiplier = 1.0

        if amount > 0:
            actual_mod = int(multiplier * amount)
            self.produced_resources[resource] += actual_mod
        else:
            actual_mod = int(amount)
            self.consumed_resources[resource] += -actual_mod
        self.resources[resource] += actual_mod

    def handle_food(self):
        food_max_spoilage = int(math.sqrt(self.resources['food']) * math.sqrt(self.age) * math.sqrt(self.total_cell_count()))
        if food_max_spoilage > 0:
            self.food = max(0, self.resources['food'] - random.randint(1, food_max_spoilage))

        for cell in self.cells:
            food_amount = cell.get_food_output()

            # print('Was producing {}, now producing {}'.format(prev, food_amount))
            self.mod_resource('food', food_amount)

        #It takes 1 food to feed each person
        self.mod_resource('food', -self.population * FOOD_PER_PERSON)

        if self.army != None:
            self.mod_resource('food', -self.army.size() * FOOD_PER_PERSON)

        #There wasn't enough food for everybody.
        if self.resources['food'] < 0:
            #These people die. Or wander off. Who cares. They've gone.
            #Negative because the food value is less than zero
            losses = -self.resources['food'] // FOOD_PER_PERSON
            army_losses = random.randint(1, int(math.sqrt(losses) + 1))

            #Remove some random amount of troops.
            #Not all desert, because they're hopefully more disciplined than that.
            self.army.remove_number('', army_losses)

            losses -= army_losses

            if losses > 0:
                population_losses = random.randint(1, losses) #Not everybody immediately starves when there isn't enough food.

                self.handle_population_change(-population_losses)

            self.resources['food'] = 0

            self.handle_abandonment()

            self.morale -= MORALE_NOT_ENOUGH_FOOD
        else:
            self.morale += MORALE_ENOUGH_FOOD


    def get_random_religion(self):
        religion_populations = self.get_religion_populations()
        weight = lambda _, (religion, adherents): adherents
        religion,_ = utility.weighted_random_choice(religion_populations, weight=weight)
        return religion

    def handle_population_change(self, amount):
        original_population = int(self.population)
        self.population = int(max(self.population + amount, 1)) # Can't be fewer than one person in the city

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
            self.army = nation.army_structure.zero()


        train_bonus = self.handle_train_bonus()

        #This is the number of recruits, it remains to be seen if we can pay for all of them
        conscripted = int((random.random() * 0.2 + 0.2) * self.population**(2.0/3.0) * self.nation.get_conscription_bonus())
        max_soldiers = int(self.nation.money / (self.nation.get_soldier_cost(self.army)) * self.nation.get_army_spending())

        #print(self.population, conscripted, max_soldiers)

        if conscripted > max_soldiers: #If we are recruiting more than we can afford, reduce the number
            conscripted = max_soldiers

        #Pay for new conscripted soldiers
        self.nation.money -= conscripted * self.nation.get_soldier_cost(self.army)

        if self.nation.money > self.army.size() * self.nation.get_soldier_upkeep(self.army):
            self.nation.money -= self.army.size() * self.nation.get_soldier_upkeep(self.army)
        else:
            # print('Not enough money for upkeep, removing {} soldiers!'.format(int((self.army.size() * self.nation.get_soldier_upkeep(self.army.name) - self.nation.money) / self.nation.get_soldier_upkeep(self.army.name))))
            self.army.remove_number('', int((self.army.size() * self.nation.get_soldier_upkeep(self.army) - self.nation.money) / self.nation.get_soldier_upkeep(self.army.name)))

            self.nation.money = 0

        self.handle_population_change(-conscripted)

        if not self.army:
            self.army = self.nation.army_structure.zero()

        self.army.add_number(conscripted, self.nation)
        self.army.train(train_bonus)

        if (self.resources['weapons'] - conscripted) > 0:
            self.army.upgrade_gear()
            self.resources['weapons'] -= conscripted


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

        #Kenny Additions
        morale_bonus_a = 0
        for cell in self.cells:
            for building in cell.buildings:
                morale_bonus_a += building.get_morale_bonus()

        if self.morale < morale_bonus_a:
            self.morale = morale_bonus_a

    def history_step(self):
        self.consumed_resources = base_resources()
        self.produced_resources = base_resources()

        self.handle_display_name()
        self.handle_disconnected_cells()

        if self.population < self.calculate_population_capacity():
            t = float(self.resources['food']) / self.population * self.population_capacity / self.population
            rate = 1.0 / (1.0 + self.population**0.5 * e**(-t)) / 9.0
            new_pop = self.population * (1.0 + rate/12.0)**12.0 + 2
            # print(self.resources['food'], self.population_capacity, self.population, t, rate, new_pop)
            change = new_pop - self.population
            self.handle_population_change(change)

        if random.randint(0, len(self.cells)) < math.sqrt(self.age): #Add new surrounding land
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

        #Because we need to know our producions in order to know what we need to build.
        for cell in self.cells:
            cell.build_buildings()

        self.calculate_population_capacity()

        self.age += 1

    def get_tax_score(self):
        amount = self.population

        for cell in self.cells:
            for building in cell.buildings:
                amount += building.get_tax_score()

        return amount

    def __repr__(self):
        result = ""

        result += "{}({}): Pop/Pop Capacity: {} / {}; Buildings: {}\n".format(self.name, self.age, self.population, self.calculate_population_capacity(), self.building_count())

        return result
