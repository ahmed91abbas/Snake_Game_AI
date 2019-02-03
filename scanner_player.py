
class event:
    def __init__(self):
        self.type = None

#arrow key values in pygame
UP = 273
DOWN = 274
RIGHT = 275
LEFT = 276

class Scanner_player:
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

        if rows % 2 == 0:
            self.even_next_move()
        else:
            self.odd_next_move()

        return self.keys

    def even_next_move(self):
        rows = self.snake.rows
        head = self.snake.head
        sx = head.pos[0]
        sy = head.pos[1]
        if sy == 0 and sx != rows-1:
            self.set_key(RIGHT)
        elif sy == rows-1 and sx != 0:
            self.set_key(LEFT)
        elif sx == rows-1 and sy != rows-1:
            self.set_key(DOWN)
        elif (sy+1) % 2 != 0 and sx != rows-2:
            self.set_key(RIGHT)
        elif (sy+1) % 2 == 0 and sx != 0:
            self.set_key(LEFT)
        elif sx == rows-2 or sx == 0:
            self.set_key(UP)
        else:
            print("Should never happen!")
            exit()

    def odd_next_move(self):
        print("TODO")
        exit()

    def get_events(self):
        return [event()]

if __name__ == '__main__':
    algo_player(None)
