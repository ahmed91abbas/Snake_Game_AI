
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
        head = self.snake.body[0]
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
        return self.keys

    def get_events(self):
        return [event()]

if __name__ == '__main__':
    algo_player(None)
