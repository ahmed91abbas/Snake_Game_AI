import pygame
import sys

class body_part:
    def __init__(self, pos, gap, x_dir=1, y_dir=0, color=(255,0,0)):
        self.pos = pos
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.color = color
        self.gap = gap

    def draw(self, surface, flag=False):
        i = self.pos[0]
        j = self.pos[1]
        area = (i*self.gap+1, j*self.gap+1, self.gap-2, self.gap-2)
        pygame.draw.rect(surface, self.color, area)

    def move(self, x_dir, y_dir):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.pos = (self.pos[0] + x_dir, self.pos[1] + y_dir)

class snake:
    def __init__(self, color, pos, settings):
        self.color = color
        self.pos = pos
        self.width = settings[0]
        self.rows = settings[2]
        gap = self.width // self.rows
        self.body = []
        self.turns = {}
        self.head = body_part(pos, gap, color=(155, 46, 108))
        self.body.append(self.head)

    def move(self):
        if not self.valid_head_pos():
            self.kill_snake()
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.x_dir = -1
                self.y_dir = 0
                self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
            elif keys[pygame.K_RIGHT]:
                self.x_dir = 1
                self.y_dir = 0
                self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
            elif keys[pygame.K_UP]:
                self.x_dir = 0
                self.y_dir = -1
                self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
            elif keys[pygame.K_DOWN]:
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
        return True

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def kill_snake(self):
        print("The snake is dead!")
        sys.exit()

    def valid_head_pos(self):
        x = self.head.pos[0]
        y = self.head.pos[1]
        if x < self.rows and y < self.rows and x >= 0 and y >= 0:
            return True
        return False

class game_win:
    def __init__(self, settings):
        self.width = settings[0]
        self.height = settings[1]
        self.rows = settings[2]
        self.gap = self.width // self.rows
        self.snake  = snake((255,0,0), (10,10), settings)
        self.create_game()

    def draw_grid(self, surface):
        color = (255,255,255)
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
            pygame.time.delay(50)
            clock.tick(10) #game won't run more than 10 fps
            self.redraw(surface)
            run = self.snake.move()
        pass

def main():
    width = 500
    height = 500
    rows = 20
    settings = (width, height, rows)
    win = game_win(settings)
    win.create_game()

main()
