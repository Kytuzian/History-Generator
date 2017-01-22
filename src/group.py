import utility

GROUP_SPEED_MULTIPLIER = 10

#A group some band of people, who go to some place, and do something when they get there
class Group:
    def __init__(self, parent, name, members, start_position, end_position, color, on_step, on_end, canvas):
        self.name = name

        self.group_id = parent.get_next_group_id()

        self.members = members

        self.on_step = on_step
        self.on_end = on_end

        self.canvas = canvas

        self.x, self.y = start_position
        self.end_x, self.end_y = end_position

        self.id = self.canvas.create_rectangle(self.x * utility.CELL_SIZE, self.y * utility.CELL_SIZE, self.x * utility.CELL_SIZE + utility.CELL_SIZE, self.y * utility.CELL_SIZE + utility.CELL_SIZE, fill=color)

    def get_info(self):
        res = {}
        res['name'] = self.name
        res['group_id'] = self.group_id

        # TODO Save the functions somehow
        # res['on_step'] = self.on_step
        # res['on_end'] = self.on_end

        res['x'] = self.x
        res['y'] = self.y
        res['end_x'] = self.end_x
        res['end_y'] = self.end_y

        return res

    def step(self, groups):
        #We are at our destination, do the stuff
        if utility.rough_match(self.x, self.end_x, GROUP_SPEED_MULTIPLIER) and utility.rough_match(self.y, self.end_y, GROUP_SPEED_MULTIPLIER):
            self.canvas.delete(self.id)
            self.on_end(self)

            return True

        if self.on_step != None:
            self.on_step(self)

        dist = utility.distance((self.x, self.y), (self.end_x, self.end_y))
        self.x += float(self.end_x - self.x) / dist * GROUP_SPEED_MULTIPLIER
        self.y += float(self.end_y - self.y) / dist * GROUP_SPEED_MULTIPLIER
        self.canvas.coords(self.id, int(self.x) * utility.CELL_SIZE, int(self.y) * utility.CELL_SIZE, int(self.x) * utility.CELL_SIZE + utility.CELL_SIZE, int(self.y) * utility.CELL_SIZE + utility.CELL_SIZE)

        return False
