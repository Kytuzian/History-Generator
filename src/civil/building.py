import random

from civil.resources import base_resources

# building_effects['Barracks'] = {'population_capacity': 15,  'sergeants':1, 'morale_bonus': 25, 'train_bonus':5,
# 'weapons':2,'cost': 500, 'size': 30} building_effects['Blacksmith'] = {'population_capacity': 2,  'weapons': 10,
# 'cost': 350, 'size': 10}

building_effects = {'Farm': {'population_capacity': 5, 'food': 60, 'cost': 200, 'size': 15},
                    'Tavern': {'population_capacity': 5, 'cost': 500, 'money_output': 1200, 'size': 50},
                    'Fishery': {'population_capacity': 2, 'food': 125, 'cost': 200, 'size': 40},
                    'Ranch': {'population_capacity': 2, 'food': 125, 'cost': 300, 'size': 50},
                    'Hunting Lodge': {'population_capacity': 2, 'food': 50, 'cost': 50, 'size': 20},
                    'Leatherworker': {'population_capacity': 2, 'money_output': 200, 'leather': 5, 'cost': 300,
                                      'size': 15},
                    'Weaver': {'population_capacity': 2, 'money_output': 200, 'cloth': 5, 'cost': 300, 'size': 15},
                    'Woodcutter': {'population_capacity': 2, 'money_output': 150, 'wood': 5, 'cost': 300, 'size': 50},
                    'Mine': {'population_capacity': 8, 'money_output': 1000, 'metal': 3, 'cost': 1000, 'size': 90},
                    'Library': {'population': 4, 'research_rate': 2, 'cost': 1000, 'size': 90},
                    'Lab': {'population_capacity': 2, 'research_rate': 5, 'cost': 1000, 'size': 75},
                    'Market': {'tax_score': 100, 'money_output': 1000, 'cost': 1500, 'size': 60},
                    'Caravansary': {'population_capacity': 5, 'caravan_chance': 20, 'cost': 2000, 'size': 90},
                    'Small Hut': {'population_capacity': 1, 'tax_score': 1, 'cost': 1, 'size': 1},
                    'Hut': {'population_capacity': 2, 'tax_score': 2, 'cost': 2, 'size': 2},
                    'Long Hut': {'population_capacity': 4, 'tax_score': 5, 'cost': 5, 'size': 4},
                    'Small House': {'population_capacity': 5, 'tax_score': 10, 'cost': 10, 'size': 5},
                    'House': {'population_capacity': 10, 'tax_score': 20, 'cost': 50, 'size': 15},
                    'Large House': {'population_capacity': 15, 'tax_score': 30, 'cost': 100, 'size': 25},
                    'Small Villa': {'population_capacity': 20, 'tax_score': 50, 'cost': 200, 'size': 50},
                    'Villa': {'population_capacity': 25, 'tax_score': 60, 'cost': 400, 'size': 60},
                    'Large Villa': {'population_capacity': 40, 'tax_score': 70, 'cost': 800, 'size': 70},
                    'Manor': {'population_capacity': 50, 'tax_score': 80, 'cost': 1600, 'size': 70},
                    'Mansion': {'population_capacity': 60, 'tax_score': 90, 'cost': 3200, 'size': 80},
                    'Castle': {'population_capacity': 100, 'weapons': 10, 'train_bonus': 10, 'tax_score': 100,
                               'cost': 6400, 'size': 100},
                    'Bank': {'population_capacity': 8, 'money_output': 3000, 'cost': 1500, 'size': 20},
                    'Guildhouse': {'population_capacity': 20, 'research_rate': 2, 'caravan_chance': 20,
                                   'money_output': 500, 'cost': 4000, 'size': 50},
                    'College': {'population_capacity': 20, 'research_rate': 3, 'cost': 3500, 'size': 50},
                    'Inn': {'population_capacity': 50, 'tax_score': 5, 'money_output': 500, 'cost': 1000, 'size': 40},
                    'Church': {'population_capacity': 5, 'tax_score': 5, 'cost': 200, 'size': 40},
                    'Sewer': {'population_capacity': 12, 'tax_score': 5, 'morale': 25, 'cost': 1200, 'size': 35},
                    'Graveyard': {'population_capacity': 2, 'morale': -2, 'cost': 100, 'size': 30},
                    'Carpenter House': {'population_capacity': 3, 'money_output': 1000, 'cost': 50, 'size': 10},
                    'Dockyard': {'population_capacity': 3, 'wood': -5, 'boats': 1, 'cost': 2300, 'size': 20},
                    'Court': {'population_capacity': 6, 'morale_bonus': 25, 'cost': 1500, 'size': 30},
                    'Workshop': {'population_capacity': 10, 'cloth': 5, 'metal': 5, 'wood': 5, 'cost': 1700,
                                 'size': 35}}

def base_buildings(city):
    buildings = [Building('Small Hut', city, building_effects['Small Hut'], 0),
                 Building('Hut', city, building_effects['Hut'], 0),
                 Building('Long Hut', city, building_effects['Long Hut'], 0),
                 Building('Small House', city, building_effects['Small House'], 0),
                 Building('House', city, building_effects['House'], 0),
                 Building('Large House', city, building_effects['Large House'], 0),
                 Building('Small Villa', city, building_effects['Small Villa'], 0),
                 Building('Villa', city, building_effects['Villa'], 0),
                 Building('Large Villa', city, building_effects['Large Villa'], 0),
                 Building('Manor', city, building_effects['Manor'], 0),
                 Building('Mansion', city, building_effects['Mansion'], 0),
                 Building('Castle', city, building_effects['Castle'], 0),
                 Building('Farm', city, building_effects['Farm'], 0),
                 Building('Hunting Lodge', city, building_effects['Hunting Lodge'], 0),
                 Building('Fishery', city, building_effects['Fishery'], 0),
                 Building('Ranch', city, building_effects['Ranch'], 0),
                 Building('Tavern', city, building_effects['Tavern'], 0),
                 Building('Mine', city, building_effects['Mine'], 0),
                 Building('Leatherworker', city, building_effects['Leatherworker'], 0),
                 Building('Weaver', city, building_effects['Weaver'], 0),
                 Building('Woodcutter', city, building_effects['Woodcutter'], 0),
                 Building('Library', city, building_effects['Library'], 0),
                 Building('Lab', city, building_effects['Lab'], 0),
                 Building('Market', city, building_effects['Market'], 0),
                 Building('Caravansary', city, building_effects['Caravansary'], 0),
                 Building('Guildhouse', city, building_effects['Guildhouse'], 0),
                 Building('College', city, building_effects['College'], 0),
                 Building('Inn', city, building_effects['Inn'], 0), Building('Bank', city, building_effects['Bank'], 0),
                 Building('Church', city, building_effects['Church'], 0),
                 Building('Sewer', city, building_effects['Sewer'], 0),
                 Building('Graveyard', city, building_effects['Graveyard'], 0),
                 Building('Carpenter House', city, building_effects['Carpenter House'], 0),
                 Building('Dockyard', city, building_effects['Dockyard'], 0),
                 Building('Court', city, building_effects['Court'], 0),
                 Building('Workshop', city, building_effects['Workshop'], 0)]

    # buildings.append(Building('Baracks', city, building_effects['Baracks'],0 ))

    return buildings

class Building:
    def __init__(self, name, city, effects, number):
        self.name = name
        self.city = city

        self.effects = effects
        self.number = number

    def save(self, db, cell_id):
        # only save name, number, cell_id, get the effects from the dictionary above.
        db.execute('db/civil/building_insert.sql', {'cell_id': cell_id, 'name': self.name, 'number': self.number})

    def produce(self):
        return

    def buy(self):
        return

    def copy(self):
        return Building(self.name, self.city, self.effects, self.number)

    # To be used when the copy is for a different city
    def clean_copy(self, new_city, number=0):
        return Building(self.name, new_city, self.effects, number)

    def __call__(self, new_city=None, number=0):
        if new_city is not None:
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

            if multiplier is not None:
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

                if multiplier is not None:
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


