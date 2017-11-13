import math
import random

from Tkinter import *

# from PIL import Image

import utility
import noise
import city
import gui

MAX_HEIGHT = 4000

BASE_CELL_FOOD_PRODUCTION = 10
BASE_CELL_MIN_FOOD_PRODUCTION = 1

def to_celsius(t):
    return (t - 32.0) / (9.0 / 5.0)

def to_farenheit(t):
    return (9.0 / 5.0) * t + 32.0

def to_meters(f):
    return 0.3048 * f

def to_feet(m):
    return m / 0.3048

def temperature(elevation, height, world_height):
    r = float(world_height) / 2
    latitude = (float(height) - r) / world_height * 180 / math.pi

    temp = 103 - 1.45*latitude - 0.00227*elevation - 0.0054*latitude**2 - 0.000007*latitude*elevation

    return to_celsius(temp)

class Terrain:
    def __init__(self, height, moisture):
        self.name = ''
        self.color = ''
        self.height = max(0, height)
        self.moisture = moisture

        self.setup()

    def get_info(self):
        res = {}
        res['height'] = self.height
        res['moisture'] = self.moisture
        res['name'] = self.name
        res['color'] = self.color

        return res

    def setup(self):
        if self.height == 0:
            self.name = 'water'
            self.color = utility.rgb_color(0, 0, 255)
        elif self.height < 0.1 and self.moisture < 0.5:
            self.name = 'sand'
            self.color = utility.rgb_color(237, 201, 175)
        elif self.height > 0.5 and self.moisture < 0.5:
            self.name = 'snow'
            self.color = utility.rgb_color(200, 255, 255)
        elif self.moisture > 0.5:
            self.name = 'forest'
            self.color = utility.rgb_color(34, 139, 34)
        else:
            self.name = 'land'
            self.color = utility.rgb_color(0, 255, 0)

    def get_food_production_multiplier(self):
        if self.name == 'water':
            return 1.1
        elif self.name == 'land':
            return 1.0
        elif self.name == 'sand':
            return 0.95
        elif self.name == 'forest':
            return 1.05
        elif self.name == 'snow':
            return 0.75

    def is_settleable(self):
        return not self.is_water()

    def is_water(self):
        return self.name == 'water'

class Cell:
    def __init__(self, parent, type, x, y, height, temperature_multiplier, moisture, owner):
        self.parent = parent

        self.type = type

        self.x = x
        self.y = y

        self.cell_id = self.parent.get_next_id('cell')

        self.id = -1

        self.building_capacity = 100

        self.terrain = Terrain(height, moisture)

        self.temperature_multiplier = max(0, temperature_multiplier)
        self.temperature = None

        self.buildings = city.base_buildings(None)

        self.high_temp_range = random.random() / 5
        self.low_temp_range = random.random() / 5

        self.owner = owner

        self.make_id()

        self.can_pass=True

        if self.terrain.is_water():
            self.can_pass = False

        
    # Determines whether it is legal for a group to move onto this square
    #Kenny - detects whether or not the cell's terrain is water. If it is water unit can't move through
    def can_move(self, group):
        return self.can_pass # For now it is always lega

    def get_info(self):
        res = {}
        res['x'] = self.x
        res['y'] = self.y
        res['id'] = self.cell_id
        res['type'] = self.type
        res['building_capacity'] = self.building_capacity
        res['high_temp_range'] = self.high_temp_range
        res['low_temp_range'] = self.low_temp_range
        res['temperature'] = self.temperature
        res['temperature_multiplier'] = self.temperature_multiplier
        res['terrain'] = self.terrain.get_info()

        res['buildings'] = []

        for building in self.buildings:
            res['buildings'].append(building.get_info())

        return res

    def get_population_capacity(self):
        return sum([building.get_population_capacity() for building in self.buildings])

    def get_food_output(self):
        result = random.randint(BASE_CELL_MIN_FOOD_PRODUCTION, BASE_CELL_FOOD_PRODUCTION)
        result *= self.food_production_multiplier()

        return result

    def building_count(self):
        return sum([building.number for building in self.buildings])

    def get_total_buiding_size(self):
        return sum([building.get_size() * building.number for building in self.buildings])

    def get_available_building_capacity(self):
        multiplier = 1.0
        if self.owner != None:
            best = self.owner.nation.tech.get_best_in_category('compact_building')

            if best != None:
                multiplier = best.multiplier

        return multiplier * self.building_capacity - self.get_total_buiding_size()

    def build_buildings(self):
        improvement_chance = int((self.building_count() + 1) / (math.sqrt(self.owner.population) + 1))
        if random.randint(0, improvement_chance + 1) == 0:
            available_buildings = filter(lambda b: b.get_size() <= self.get_available_building_capacity(), self.buildings)

            if len(available_buildings) > 0:
                build_building = utility.weighted_random_choice(available_buildings, weight=lambda _, b: 1.0 / b.get_cost())

                if self.owner.nation.money > build_building.get_cost():
                    self.owner.nation.money -= build_building.get_cost()
                    build_building.number += 1

    def get_resource_productions(self):
        result = {}
        for building in self.buildings:
            production = building.get_resource_productions()

            for resource in production:
                if resource in result:
                    result[resource] += production[resource]
                else:
                    result[resource] = production[resource]
        return result

    def get_tax_rate(self):
        return utility.product([building.get_tax_rate() for building in self.buildings])

    def get_money_output(self):
        return sum([building.get_money_output() for building in self.buildings])

    def get_elevation(self):
        return to_meters(self.terrain.height * MAX_HEIGHT)

    def get_high_temperature(self):
        return self.get_temperature() + self.get_temperature() * self.high_temp_range

    def get_low_temperature(self):
        return self.get_temperature() - self.get_temperature() * self.low_temp_range

    def get_temperature_range(self):
        return self.get_high_temperature() - self.get_low_temperature()

    def get_temperature(self):
        #The base temperature never changes, so we only need to calculate it once.
        if self.temperature == None:
            self.temperature = temperature(self.terrain.height * MAX_HEIGHT, self.y, utility.S_HEIGHT) * (1 - self.temperature_multiplier)

        return self.temperature

    #http://www.sciencedirect.com/science/article/pii/0002157177900073
    def get_dew_point(self):
        return 0.0023 * self.get_elevation() + 0.37 * self.get_temperature() + 0.53 * self.get_temperature_range() - 10.9

    def get_evaporation(self):
        amount = (self.get_temperature() + 15.0 * self.get_dew_point()) / (80.0 - self.get_temperature())
        amount *= random.random()

        if self.terrain.is_water():
            return amount

        if amount > self.terrain.moisture:
            amount = self.terrain.moisture
            self.terrain.moisture = 0

            return amount
        else:
            self.terrain.moisture -= amount

            return amount

    def food_production_multiplier(self):
        #Higher temperature means better production.
        multiplier = self.get_temperature() / 98.0 * self.terrain.get_food_production_multiplier()
        for neighbor in self.neighbors():
            #So does being surrounding by water
            if neighbor.terrain.is_water():
                multiplier *= neighbor.terrain.get_food_production_multiplier()

        return multiplier

    def reset_color(self):
        if self.id >= 0:
            if self.owner != None:
                self.parent.canvas.itemconfig(self.id, fill=self.owner.nation.color)
            else:
                self.parent.canvas.itemconfig(self.id, fill=self.terrain.color)

    def make_id(self):
        start_x, start_y = self.x * utility.CELL_SIZE, self.y * utility.CELL_SIZE
        end_x, end_y = start_x + utility.CELL_SIZE, start_y + utility.CELL_SIZE
        try:
            if self.owner != None:
                self.id = self.parent.canvas.create_rectangle(start_x, start_y, end_x, end_y, width=0, fill=self.owner.nation.color)
            else:
                self.id = self.parent.canvas.create_rectangle(start_x, start_y, end_x, end_y, width=0, fill=self.terrain.color)
        except:
            pass

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title('Cell Information: ({}, {})'.format(self.x, self.y))
        self.gui_window.geometry("400x300+0+0")
        self.gui_window.config(background='white')

        self.type_label = gui.Label(self.gui_window, text='Type: {}'.format(self.type))
        self.type_label.grid(row=0, sticky=W)

        self.owning_city_label = gui.Label(self.gui_window, text='Owning city: ')
        self.owning_city_label.grid(row=1, sticky=W)

        self.owning_nation_label = gui.Label(self.gui_window, text='Owning nation: ')
        self.owning_nation_label.grid(row=2, sticky=W)

        if self.owner != None:
            self.owning_city_button = gui.Button(self.gui_window, text=self.owner.name, command=self.owner.show_information_gui)
            self.owning_nation_button = gui.Button(self.gui_window, text=self.owner.nation.name, command=self.owner.nation.show_information_gui)
        else:
            self.owning_city_button = gui.Button(self.gui_window, text='None')
            self.owning_nation_button = gui.Button(self.gui_window, text='None')

        self.owning_city_button.grid(row=1, column=1, sticky=W)
        self.owning_nation_button.grid(row=2, column=1, sticky=W)

        self.building_capacity_label = gui.Label(self.gui_window, text='{} of {} filled.'.format(self.get_total_buiding_size(), self.building_capacity))
        self.building_capacity_label.grid(row=3)

        self.buildings_display = Listbox(self.gui_window)

        for building in self.buildings:
            self.buildings_display.insert(END, '{}: {}'.format(building.name, building.number))

        self.buildings_display.grid(row=4, column=0, columnspan=3, sticky=W+E)

    def update_self(self):
        if self.owner == None:
            self.parent.canvas.itemconfig(self.id, fill=self.terrain.color)
        else:
            self.parent.canvas.itemconfig(self.id, fill=self.owner.nation.color)

    def change_type(self, new_type):
        self.type = new_type

        self.update_self()

    def change_owner(self, new_owner, new_type=None):
        if self.owner != None: #Remove this cell from the list of owned cells
            self.owner.remove_cell(self)

        #This must be before .add_cell
        if new_type != None:
            self.change_type(new_type)

        self.owner = new_owner

        if self.owner != None:
            for building in self.buildings:
                building.city = new_owner
            self.owner.add_cell(self)
        else:
            self.new_type = '' #There is no cell type for an unowned cell.
            self.buildings = city.base_buildings(None)

        self.update_self()

    def neighbors(self):
        result = []

        if self.x > 0:
            result.append(self.parent.cells[self.x - 1][self.y])
        # else:
        #     result.append(self.parent.cells[utility.S_WIDTH // utility.CELL_SIZE - 1][self.y])

        if self.y > 0:
            result.append(self.parent.cells[self.x][self.y - 1])
        # else:
        #     result.append(self.parent.cells[self.x][utility.S_HEIGHT // utility.CELL_SIZE - 1])

        if self.x < utility.S_WIDTH // utility.CELL_SIZE - 1:
            result.append(self.parent.cells[self.x + 1][self.y])
        # else:
        #     result.append(self.parent.cells[0][self.y])

        if self.y < utility.S_HEIGHT // utility.CELL_SIZE - 1:
            result.append(self.parent.cells[self.x][self.y + 1])
        # else:
        #     result.append(self.parent.cells[self.x][0])

        return result

class Cloud:
    def __init__(self, x, y, water):
        self.x = x
        self.y = y
        self.water = water

        self.processed = False

        self.wait = 125 * random.random()**5
        self.age = 0

    def add_water(self, amount):
        self.water += water

    def precipitate(self):
        if self.age > self.wait:
            amount = random.random() * self.water
            self.water -= amount
        else:
            amount = 0
        return amount

class Weather:
    def __init__(self, cells, parent):
        self.cells = cells
        self.water_cells = []

        self.clouds = []

        self.cells_x = utility.S_WIDTH // utility.CELL_SIZE
        self.cells_y = utility.S_HEIGHT // utility.CELL_SIZE

        self.setup(parent)

    def setup(self, parent):
        self.wind_vectors = self.calculate_wind_vectors()
        self.setup_clouds()
        self.water_cells = self.get_water_cells()

    def get_water_cells(self):
        res = []

        for row in self.cells:
            for cell in row:
                if cell.terrain.is_water():
                    res.append(cell)

        return res

    def setup_clouds(self):
        for x, row in enumerate(self.cells):
            self.clouds.append([])
            for y, cell in enumerate(row):
                self.clouds[-1].append([])

    def handle_evaporation(self):
        for i, cell in enumerate(self.water_cells):
            # utility.show_bar(i, self.water_cells, message='Handling evaporation: ')
            amount = cell.get_evaporation() * 4

            if amount <= 0:
                continue

            if len(self.clouds[cell.x][cell.y]) > 0:
                self.clouds[cell.x][cell.y][0].water += amount
            else:
                self.clouds[cell.x][cell.y].append(Cloud(cell.x, cell.y, amount))

    def handle_clouds(self):
        for x, row in enumerate(self.clouds):
            for y, cell in enumerate(row):
                for cloud in cell:
                    cloud.processed = False
                    cloud.age += 1

                    if not self.cells[x][y].terrain.is_water():
                        self.cells[x][y].terrain.moisture += cloud.precipitate()

                    if cloud.water <= 0:
                        cell.remove(cloud)

    def calculate_wind_vectors(self):
        wind_vectors = []
        for x, row in enumerate(self.cells):
            wind_vectors.append([])
            for y, cell in enumerate(row):
                dx, dy = 0.0, 0.0
                for neighbor in cell.neighbors():
                    cdx, cdy = cell.x - neighbor.x, cell.y - neighbor.y
                    cdx = cdx * (cell.get_temperature() - neighbor.get_temperature()) / cell.get_temperature()
                    cdy = cdy * (cell.get_temperature() - neighbor.get_temperature()) / cell.get_temperature()
                    dx += cdx
                    dy += cdy
                mag = math.sqrt(dx**2 + dy**2)
                dx, dy = dx / mag * 5, dy / mag * 5
                dx += 1.5 #Wind goes west to east
                wind_vectors[-1].append((dx, dy))

        return wind_vectors

    def handle_wind(self):
        for x, row in enumerate(self.clouds):
            for y, cell in enumerate(row):
                for cloud in cell:
                    if not cloud.processed:
                        cell.remove(cloud)

                        cloud.processed = True

                        dx, dy = self.wind_vectors[x][y]
                        cloud.x += dx
                        cloud.y += dy

                        if cloud.x >= self.cells_x:
                            cloud.x = 0
                        elif cloud.x < 0:
                            cloud.x = self.cells_x - 1

                        if cloud.y >= self.cells_y:
                            cloud.y = 0
                        elif cloud.y < 0:
                            cloud.y = self.cells_y - 1

                        self.clouds[int(cloud.x)][int(cloud.y)].append(cloud)

    def step(self):
        self.handle_wind()
        self.handle_clouds()
        self.handle_evaporation()

    def normalize_moistures(self):
        print('Normalizing moistures.')
        moistures = reduce(lambda a, b: a + b, map(lambda row: map(lambda cell: cell.terrain.moisture, row), self.cells))
        max_amount = max(moistures)

        for row in self.cells:
            for cell in row:
                cell.terrain.moisture /= max_amount

    def run(self, steps):
        for step in xrange(steps + 1):
            utility.show_bar(step, steps + 1, message='Generating rainfall patterns: ', number_limit=True)
            self.step()

            data = reduce(lambda a, b: a + b, map(lambda row: map(lambda cell: cell.terrain.moisture, row), self.cells))
            max_amount = max(data)
            if max_amount != 0:
                data = map(lambda i: i / max_amount, data)
