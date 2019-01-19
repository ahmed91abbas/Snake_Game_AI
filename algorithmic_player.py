
class event:
    def __init__(self):
        self.type = None

#arrow key values in pygame
UP = 273
DOWN = 274
RIGHT = 275
LEFT = 276

class algo_player:
    def __init__(self, snake):
        self.snake = snake
        self.keys = self.init_keys()

    def init_keys(self):
        keys = {}
        keys[UP] = 0
        keys[DOWN] = 0
        keys[RIGHT] = 0
        keys[LEFT] = 0
        return keys

    def set_key(self, key):
        self.keys = self.init_keys()
        self.keys[key] = 1

    def next_move(self):
        head = self.snake.head
        food = self.snake.food
        rows = self.snake.rows
        x_dir = head.x_dir
        y_dir = head.y_dir
        sx = head.pos[0]
        sy = head.pos[1]
        fx = food.pos[0]
        fy = food.pos[1]
        #food to the right of snake head
        if sx < fx:
            if x_dir == -1:
                if sy > rows // 2:
                    self.set_key(UP)
                else:
                    self.set_key(DOWN)
            else:
                self.set_key(RIGHT)
        #food to the left of snake head
        elif sx > fx:
            if x_dir == 1:
                if sy > rows // 2:
                    self.set_key(UP)
                else:
                    self.set_key(DOWN)
            else:
                self.set_key(LEFT)
        #food upove of snake head
        elif sy < fy:
            if y_dir == -1:
                if sx > rows // 2:
                    self.set_key(LEFT)
                else:
                    self.set_key(RIGHT)
            else:
                self.set_key(DOWN)
        #food under of snake head
        elif sy > fy:
            if y_dir == 1:
                if sx > rows // 2:
                    self.set_key(LEFT)
                else:
                    self.set_key(RIGHT)
            else:
                self.set_key(UP)
        if self.about_to_die():
            self.evade()
        return self.keys

    def about_to_die(self):
        pos = self.snake.head.pos
        for key in self.keys:
            if self.keys[key]:
                x_dir = 0
                y_dir = 0
                if key == UP:
                    y_dir = -1
                elif key == DOWN:
                    y_dir = 1
                elif key == LEFT:
                    x_dir = -1
                elif key == RIGHT:
                    x_dir = 1
                pos = (pos[0] + x_dir, pos[1] + y_dir)
        if pos in self.snake.snake_positions:
            return True
        return False

    def evade(self):
        free_slots = self.get_free_slots()
        max_slots = -1
        best_move = None
        for key in free_slots:
            if free_slots[key] > max_slots:
                best_move = key
                max_slots = free_slots[key]
        self.set_key(best_move)

    def get_free_slots(self):
        free_slots = {}
        for key in self.keys:
            free_slots[key] = 0
        rows = self.snake.rows
        #count in left direction
        x = self.snake.head.pos[0]
        y = self.snake.head.pos[1]
        x -= 1
        pos = (x, y)
        advantage = self.snake.rows
        while x >= 0 and pos not in self.snake.snake_positions:
            if x == 0:
                free_slots[LEFT] += advantage
            free_slots[LEFT] += 1
            x -= 1
            pos = (x, y)
        #count in right direction
        x = self.snake.head.pos[0]
        y = self.snake.head.pos[1]
        x += 1
        pos = (x, y)
        while x < rows and pos not in self.snake.snake_positions:
            if x == rows - 1:
                free_slots[RIGHT] += advantage
            free_slots[RIGHT] += 1
            x += 1
            pos = (x, y)

        #count in up direction
        x = self.snake.head.pos[0]
        y = self.snake.head.pos[1]
        y -= 1
        pos = (x, y)
        while y >= 0 and pos not in self.snake.snake_positions:
            if y == 0:
                free_slots[UP] += advantage
            free_slots[UP] += 1
            y -= 1
            pos = (x, y)
        #count in down direction
        x = self.snake.head.pos[0]
        y = self.snake.head.pos[1]
        y += 1
        pos = (x, y)
        while y < rows and pos not in self.snake.snake_positions:
            if y == rows - 1:
                free_slots[DOWN] += advantage
            free_slots[DOWN] += 1
            y += 1
            pos = (x, y)

        return free_slots

    def get_events(self):
        return [event()]

if __name__ == '__main__':
    algo_player(None)
