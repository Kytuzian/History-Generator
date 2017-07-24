import utility

GROUP_SPEED_MULTIPLIER = 10
ARMY_SPEED_MULTIPLIER = 2 # Armies can move twice as far as other groups.

# A group of some band of people, who go to some place, and do something when they get there
class Group:
    def __init__(self, parent, name, members, start_position, end_position, color, on_step, on_end, canvas, is_army=False):
        self.name = name
        self.parent = parent

        self.group_id = parent.get_next_id('group')

        self.members = members

        self.on_step = on_step
        self.on_end = on_end

        self.canvas = canvas

        self.x, self.y = start_position
        self.end_x, self.end_y = end_position

        self.color = color
        self.id = self.canvas.create_rectangle(self.x * utility.CELL_SIZE, self.y * utility.CELL_SIZE, self.x * utility.CELL_SIZE + utility.CELL_SIZE, self.y * utility.CELL_SIZE + utility.CELL_SIZE, fill=color)

        self.cur_path = []
        self.path_ids = [] # The ids of the path squares we're going to draw

        self.can_move_amount = 0
        self.move_dist = GROUP_SPEED_MULTIPLIER
        self.is_army = is_army
        if self.is_army:
            self.move_dist *= ARMY_SPEED_MULTIPLIER

    # A basic A* implementation instead of greedy so that we can block off certain tiles later
    def path(self):
        self.cur_path = []

        open = []
        closed = []
        visited = {}

        moves = 0
        x, y = int(self.x), int(self.y)

        while x != self.end_x or y != self.end_y:
            moves += 1
            if x < len(self.parent.cells) - 1 and self.parent.cells[x + 1][y].can_move(self):
                if not (x + 1, y) in visited:
                    visited[(x + 1, y)] = True
                    open.append((x + 1, y, x, y, moves))

            if x > 0 and self.parent.cells[x - 1][y].can_move(self):
                if not (x - 1, y) in visited:
                    visited[(x - 1, y)] = True
                    open.append((x - 1, y, x, y, moves))

            if y < len(self.parent.cells[x]) - 1 and self.parent.cells[x][y + 1].can_move(self):
                if not (x, y + 1) in visited:
                    visited[(x, y + 1)] = True
                    open.append((x, y + 1, x, y, moves))

            if y > 0 and self.parent.cells[x][y - 1].can_move(self):
                if not (x, y - 1) in visited:
                    visited[(x, y - 1)] = True
                    open.append((x, y - 1, x, y, moves))

            min_score = -1
            ci = 0

            for i, (cx, cy, px, py, cur_moves) in enumerate(open):
                d = utility.distance_squared((cx, cy), (self.end_x, self.end_y))
                if min_score == -1 or (d + cur_moves) < min_score:
                    min_score = d + cur_moves
                    ci = i

            x, y, px, py, moves = open.pop(ci)
            closed.append((x, y, px, py, moves))

        # Rebuild the path from the last node we chose, which should be the one that got us to the target
        x, y, px, py, _ = closed.pop()
        while px != int(self.x) or py != int(self.y):
            self.cur_path.append((x, y))

            for i, (x1, y1, px1, py1, _) in enumerate(closed):
                if x1 == px and y1 == py:
                    x, y, px, py, _ = closed.pop(i)
                    break

        # Reverse it back it starts at the last node, not the first like it should
        self.cur_path = self.cur_path[::-1]

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

    # Find the path and then draw as many squares as we will be able to move this move-turn-thing
    def start_move(self):
        self.path()

        self.can_move_amount = self.move_dist

        self.path_ids = []
        # DRAW THE PATH SQUARES HERE
        for x, y in self.cur_path:
            id = self.canvas.create_rectangle(int(x) * utility.CELL_SIZE,
                                              int(y) * utility.CELL_SIZE,
                                              int(x) * utility.CELL_SIZE + utility.CELL_SIZE,
                                              int(y) * utility.CELL_SIZE + utility.CELL_SIZE,
                                              fill=self.color, width=0)
            self.path_ids.append(id)

        self.canvas.tag_raise(self.id)

    def end_move(self):
        for path_id in self.path_ids:
            self.canvas.delete(path_id)
        self.path_ids = []
        self.cur_path = []

    def do_move(self):
        if self.can_move_amount > 0 and len(self.cur_path) > 0:
            self.move_to(*self.cur_path.pop(0))

            self.can_move_amount -= 1

        return self.can_move_amount <= 0 or len(self.cur_path) == 0

    def move_to(self, x, y):
        self.x = x
        self.y = y

        self.canvas.coords(self.id, int(self.x) * utility.CELL_SIZE,
                                    int(self.y) * utility.CELL_SIZE,
                                    int(self.x) * utility.CELL_SIZE + utility.CELL_SIZE,
                                    int(self.y) * utility.CELL_SIZE + utility.CELL_SIZE)

    def step(self, groups):
        #We are at our destination, do the stuff
        if utility.rough_match(self.x, self.end_x, GROUP_SPEED_MULTIPLIER) and utility.rough_match(self.y, self.end_y, GROUP_SPEED_MULTIPLIER):
            self.canvas.delete(self.id)
            self.on_end(self)

            return True

        if self.on_step != None:
            self.on_step(self)

        # Do simple movement for all non-army groups, as they aren't as important
        if not self.is_army:
            dist = utility.distance((self.x, self.y), (self.end_x, self.end_y))

            self.move_to(self.x + float(self.end_x - self.x) / dist * GROUP_SPEED_MULTIPLIER,
                         self.y + float(self.end_y - self.y) / dist * GROUP_SPEED_MULTIPLIER)

        return False
