from internal import utility


class CityHeader:
    def __init__(self, city):
        self.city = city

        x, y = self.get_position()

        self.name_id = self.city.parent.canvas.create_text(x, y - utility.CELL_SIZE * 4, text='{} ({})'.format(self.city.name, self.city.population))
        self.food_indicator_id = self.city.parent.canvas.create_rectangle(x - 7, y - utility.CELL_SIZE * 3, x + 7, y - utility.CELL_SIZE * 2, fill='green')
        self.resource_indicator_id = self.city.parent.canvas.create_rectangle(x - 7, y - utility.CELL_SIZE * 2, x + 7, y - utility.CELL_SIZE, fill='green')

    def get_position(self):
        x, y = self.city.get_average_position()
        return x * utility.CELL_SIZE, y * utility.CELL_SIZE

    def lerp(self, rgb1, rgb2, t):
        r1,g1,b1 = rgb1
        r2,g2,b2 = rgb2
        return r2 + (r1 - r2) * t, g2 + (g1 - g2) * t, b2 + (b1 - b2) * t

    def remake(self):
        self.city.parent.canvas.delete(self.name_id)
        self.city.parent.canvas.delete(self.food_indicator_id)
        self.city.parent.canvas.delete(self.resource_indicator_id)

        x, y = self.get_position()

        self.name_id = self.city.parent.canvas.create_text(x, y - utility.CELL_SIZE * 4, text='{} ({})'.format(self.city.name, self.city.population))
        self.food_indicator_id = self.city.parent.canvas.create_rectangle(x + 7, y - utility.CELL_SIZE * 3, x + 7, y - utility.CELL_SIZE * 2)
        self.resource_indicator_id = self.city.parent.canvas.create_rectangle(x - 7, y - utility.CELL_SIZE * 2, x + 7, y - utility.CELL_SIZE)

    def handle(self):
        x, y = self.get_position()

        self.city.parent.canvas.coords(self.name_id, x, y - utility.CELL_SIZE * 4)
        self.city.parent.canvas.itemconfig(self.name_id, text='{} ({})'.format(self.city.name, self.city.population))

        food_color = 'green' if self.city.produced_resources['food'] > self.city.consumed_resources['food'] else 'red'

        self.city.parent.canvas.coords(self.food_indicator_id, x - 7, y - utility.CELL_SIZE * 3, x + 7, y - utility.CELL_SIZE * 2)
        self.city.parent.canvas.itemconfig(self.food_indicator_id, fill=food_color)

        produced = utility.sum_dict(self.city.produced_resources)
        consumed = utility.sum_dict(self.city.consumed_resources)

        resource_color = 'green' if produced > consumed else 'red'

        self.city.parent.canvas.coords(self.resource_indicator_id, x - 7, y - utility.CELL_SIZE * 2, x + 7, y - utility.CELL_SIZE)
        self.city.parent.canvas.itemconfig(self.resource_indicator_id, fill=resource_color)
