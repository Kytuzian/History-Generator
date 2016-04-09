import utility

GROUP_SPEED_MULTIPLIER = 10

#A group some band of people, who go to some place, and do something when they get there
class Group:
    def __init__(self, name, members, start_position, end_position, color, on_step, on_end, canvas):
        self.name = name

        self.members = members

        self.on_step = on_step
        self.on_end = on_end

        self.canvas = canvas

        self.x, self.y = start_position
        self.end_x, self.end_y = end_position

        self.id = self.canvas.create_rectangle(self.x * utility.CELL_SIZE, self.y * utility.CELL_SIZE, self.x * utility.CELL_SIZE + utility.CELL_SIZE, self.y * utility.CELL_SIZE + utility.CELL_SIZE, fill=color)

    def step(self, groups):
        #We are at our destination, do the stuff
        if utility.rough_match(self.x, self.end_x, GROUP_SPEED_MULTIPLIER) and utility.rough_match(self.y, self.end_y, GROUP_SPEED_MULTIPLIER):
            self.canvas.delete(self.id)
            self.on_end(self)

            return True

        self.on_step(self)

        dist = utility.distance((self.x, self.y), (self.end_x, self.end_y))
        self.x += float(self.end_x - self.x) / dist * GROUP_SPEED_MULTIPLIER
        self.y += float(self.end_y - self.y) / dist * GROUP_SPEED_MULTIPLIER
        self.canvas.coords(self.id, int(self.x) * utility.CELL_SIZE, int(self.y) * utility.CELL_SIZE, int(self.x) * utility.CELL_SIZE + utility.CELL_SIZE, int(self.y) * utility.CELL_SIZE + utility.CELL_SIZE)

        return False
