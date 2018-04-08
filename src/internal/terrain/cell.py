import math
import random
from Tkconstants import W, END, E
from Tkinter import Tk, Listbox

from civil import building as building
from internal import utility as utility, gui as gui
from internal.terrain.terrain import Terrain, BASE_CELL_MIN_FOOD_PRODUCTION, BASE_CELL_FOOD_PRODUCTION, to_meters, \
    MAX_HEIGHT, temperature


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

        self.buildings = building.base_buildings(None)

        self.high_temp_range = random.random() / 5
        self.low_temp_range = random.random() / 5

        self.owner = owner

        self.make_id()

        self.can_pass = not self.terrain.is_water()

    # Determines whether it is legal for a group to move onto this square
    # Kenny - detects whether or not the cell's terrain is water. If it is water unit can't move through
    def can_move(self, group):
        return self.can_pass  # For now it is always lega

    def save(self):
        self.parent.db.execute('db/internal/terrain/cell_insert.sql', {'cell_id': self.cell_id,
                                                                       'type': self.type,
                                                                       'x': self.x, 'y': self.y,
                                                                       'height': self.terrain.height,
                                                                       'temperature_multiplier': self.temperature_multiplier,
                                                                       'moisture': self.terrain.moisture,
                                                                       'owner': self.owner.id if self.owner is not None else -1,
                                                                       'building_capacity': self.building_capacity,
                                                                       'high_temp_range': self.high_temp_range,
                                                                       'low_temp_range': self.low_temp_range})

        for building in self.buildings:
            if building.number > 0:
                building.save(self.parent.db, self.cell_id)

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
        if self.owner is not None:
            best = self.owner.nation.tech.get_best_in_category('compact_building')

            if best is not None:
                multiplier = best.multiplier

        return multiplier * self.building_capacity - self.get_total_buiding_size()

    def build_buildings(self):
        improvement_chance = int((self.building_count() + 1) / (math.sqrt(self.owner.population) + 1))
        if random.randint(0, improvement_chance + 1) == 0:
            available_buildings = filter(lambda b: b.get_size() <= self.get_available_building_capacity(),
                                         self.buildings)

            if len(available_buildings) > 0:
                build_building = utility.weighted_random_choice(available_buildings,
                                                                weight=lambda _, b: 1.0 / b.get_cost())

                if self.owner.nation.money > build_building.get_cost():
                    self.owner.nation.money -= build_building.get_cost()
                    build_building.number += 1

    def get_resource_productions(self):
        result = {}
        for curBuilding in self.buildings:
            production = curBuilding.get_resource_productions()

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
        # The base temperature never changes, so we only need to calculate it once.
        if self.temperature is None:
            self.temperature = temperature(self.terrain.height * MAX_HEIGHT, self.y, utility.S_HEIGHT) * (
                        1 - self.temperature_multiplier)

        return self.temperature

    # http://www.sciencedirect.com/science/article/pii/0002157177900073
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
        # Higher temperature means better production.
        multiplier = self.get_temperature() / 98.0 * self.terrain.get_food_production_multiplier()
        for neighbor in self.neighbors():
            # So does being surrounding by water
            if neighbor.terrain.is_water():
                multiplier *= neighbor.terrain.get_food_production_multiplier()

        return multiplier

    def reset_color(self):
        if self.id >= 0:
            if self.owner is not None:
                self.parent.canvas.itemconfig(self.id, fill=self.owner.nation.color)
            else:
                self.parent.canvas.itemconfig(self.id, fill=self.terrain.color)

    def make_id(self):
        start_x, start_y = self.x * utility.CELL_SIZE, self.y * utility.CELL_SIZE
        end_x, end_y = start_x + utility.CELL_SIZE, start_y + utility.CELL_SIZE
        try:
            if self.owner is not None:
                self.id = self.parent.canvas.create_rectangle(start_x, start_y, end_x, end_y, width=0,
                                                              fill=self.owner.nation.color)
            else:
                self.id = self.parent.canvas.create_rectangle(start_x, start_y, end_x, end_y, width=0,
                                                              fill=self.terrain.color)
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

        if self.owner is not None:
            self.owning_city_button = gui.Button(self.gui_window, text=self.owner.name,
                                                 command=self.owner.show_information_gui)
            self.owning_nation_button = gui.Button(self.gui_window, text=self.owner.nation.name,
                                                   command=self.owner.nation.show_information_gui)
        else:
            self.owning_city_button = gui.Button(self.gui_window, text='None')
            self.owning_nation_button = gui.Button(self.gui_window, text='None')

        self.owning_city_button.grid(row=1, column=1, sticky=W)
        self.owning_nation_button.grid(row=2, column=1, sticky=W)

        self.building_capacity_label = gui.Label(self.gui_window,
                                                 text='{} of {} filled.'.format(self.get_total_buiding_size(),
                                                                                self.building_capacity))
        self.building_capacity_label.grid(row=3)

        self.buildings_display = Listbox(self.gui_window)

        for building in self.buildings:
            self.buildings_display.insert(END, '{}: {}'.format(building.name, building.number))

        self.buildings_display.grid(row=4, column=0, columnspan=3, sticky=W + E)

    def update_self(self):
        if self.owner is None:
            self.parent.canvas.itemconfig(self.id, fill=self.terrain.color)
        else:
            self.parent.canvas.itemconfig(self.id, fill=self.owner.nation.color)

    def change_type(self, new_type):
        self.type = new_type

        self.update_self()

    def change_owner(self, new_owner, new_type=None):
        if self.owner is not None:  # Remove this cell from the list of owned cells
            self.owner.remove_cell(self)

        # This must be before .add_cell
        if new_type is not None:
            self.change_type(new_type)

        self.owner = new_owner

        if self.owner is not None:
            for curBuilding in self.buildings:
                curBuilding.city = new_owner
            self.owner.add_cell(self)
        else:
            self.new_type = ''  # There is no cell type for an unowned cell.
            self.buildings = building.base_buildings(None)

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