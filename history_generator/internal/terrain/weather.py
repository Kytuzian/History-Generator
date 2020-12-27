import math

from functools import reduce

from internal import utility as utility
from internal.terrain.cloud import Cloud


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
                mag = math.sqrt(dx ** 2 + dy ** 2)
                dx, dy = dx / mag * 5, dy / mag * 5
                dx += 1.5  # Wind goes west to east
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
        moistures = reduce(lambda a, b: a + b,
                           map(lambda row: list(map(lambda cell: cell.terrain.moisture, row)), self.cells))
        max_amount = max(moistures)

        for row in self.cells:
            for cell in row:
                cell.terrain.moisture /= max_amount

    def run(self, steps):
        for step in range(steps + 1):
            utility.show_bar(step, steps + 1, message='Generating rainfall patterns: ', number_limit=True)
            self.step()

            data = reduce(lambda a, b: a + b, map(lambda row: list(map(lambda cell: cell.terrain.moisture, row)), self.cells))
            max_amount = max(data)
            if max_amount != 0:
                data = list(map(lambda i: i / max_amount, data))
