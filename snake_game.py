import pygame
import sys
import random
from algorithmic_player import algo_player

class body_part:
    def __init__(self, pos, gap, x_dir=1,\
                    y_dir=0, color=(255,0,0)):
        self.pos = pos
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.color = color
        self.gap = gap

    def draw(self, surface):
        i = self.pos[0]
        j = self.pos[1]
        area = (i*self.gap+1, j*self.gap+1, self.gap-2, self.gap-2)
        pygame.draw.rect(surface, self.color, area)

    def move(self, x_dir, y_dir):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.pos = (self.pos[0] + x_dir, self.pos[1] + y_dir)

    def place(self, pos):
        self.pos = pos

    def __eq__(self, other):
        return self.pos==other.pos

    def __hash__(self):
        return hash((self.pos))

class snake:
    def __init__(self, pos, settings):
        self.pos = pos
        self.width = settings[0]
        self.rows = settings[2]
        self.gap = self.width // self.rows
        self.body = []
        self.turns = {}
        self.snake_positions = set()
        self.x_dir = 1
        self.y_dir = 0
        self.score = 0
        self.head = body_part(pos, self.gap, color=(155, 46, 108))
        self.body.append(self.head)

        self.food = body_part((0,0), self.gap, color=(164, 244, 66))

        self.all_positions = set()
        for i in range(self.rows):
            for j in range(self.rows):
                self.all_positions.add((i, j))
        self.free_positions = self.all_positions.copy()
        self.free_positions.remove(pos)
        self.place_random_food()

    def move(self, player=None):
        if player:
            events = player.get_events()
        else:
            events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if player:
                keys = player.next_move()
            else:
                keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.x_dir != 1:
                self.x_dir = -1
                self.y_dir = 0
                self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
            elif keys[pygame.K_RIGHT] and self.x_dir != -1:
                self.x_dir = 1
                self.y_dir = 0
                self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
            elif keys[pygame.K_UP] and self.y_dir != 1:
                self.x_dir = 0
                self.y_dir = -1
                self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
            elif keys[pygame.K_DOWN] and self.y_dir != -1:
                self.x_dir = 0
                self.y_dir = 1
                self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]

        for i, bp in enumerate(self.body):
            p = bp.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                bp.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                bp.move(bp.x_dir, bp.y_dir)

        if not self.valid_head_pos(self.head.pos):
            self.kill_snake()
            return False

        if self.reached_food():
            self.eat()
        return True

    def draw(self, surface):
        self.free_positions = self.all_positions.copy()
        self.food.draw(surface)
        self.snake_positions = set()
        for i, bp in enumerate(self.body):
            bp.draw(surface)
            self.free_positions.remove(bp.pos)
            self.snake_positions.add(bp.pos)

    def kill_snake(self):
        print("The snake is dead!", "Score =", self.score)

    def valid_head_pos(self, pos):
        x = pos[0]
        y = pos[1]
        in_bounds = x < self.rows and y < self.rows\
                     and x >= 0 and y >= 0
        temp = set(self.body)
        body_overlap = len(temp) != len(self.body)
        if in_bounds and not body_overlap:
            return True
        return False

    def place_random_food(self):
        pos = random.sample(self.free_positions, 1)[0]
        self.food.place(pos)

    def reached_food(self):
        x = self.head.pos[0]
        y = self.head.pos[1]
        if x == self.food.pos[0] and y == self.food.pos[1]:
            return True
        return False

    def eat(self):
        self.score += 1
        tail = self.body[len(self.body)-1]
        x = tail.pos[0]
        y = tail.pos[1]
        if tail.x_dir == 1:
            pos = (x-1, y)
        elif tail.x_dir == -1:
            pos = (x+1, y)
        elif tail.y_dir == 1:
            pos = (x, y-1)
        elif tail.y_dir == -1:
            pos = (x, y+1)
        #TODO handel the case when it is not valid
        if self.valid_head_pos(pos):
            new_tail = body_part(pos, self.gap,\
                        x_dir=tail.x_dir, y_dir=tail.y_dir)
            self.body.append(new_tail)
        self.place_random_food()

class game_win:
    def __init__(self, settings):
        self.width = settings[0]
        self.height = settings[1]
        self.rows = settings[2]
        self.gap = self.width // self.rows
        self.snake  = snake((0,self.rows//2), settings)
        self.algo_player = algo_player(self.snake)

    def draw_grid(self, surface):
        color = (128, 137, 153)
        v = 0
        for i in range(self.rows):
            v = v + self.gap
            pygame.draw.line(surface, color, (v,0), (v, self.width))
            pygame.draw.line(surface, color, (0,v), (self.width,v))

    def redraw(self, surface):
        surface.fill((0, 0, 0))
        self.snake.draw(surface)
        self.draw_grid(surface)
        pygame.display.update()

    def create_game(self):
        surface = pygame.display.set_mode((self.width, self.height))
        run = True
        clock = pygame.time.Clock()
        while run:
            pygame.time.delay(60)
            clock.tick(10) #game won't run more than 10 fps
            self.redraw(surface)
            run = self.snake.move(player=self.algo_player)
        pass

def main():
    width = 504
    height = 504
    rows = 14
    settings = (width, height, rows)
    for i in range(30):
        win = game_win(settings)
        win.create_game()

main()
