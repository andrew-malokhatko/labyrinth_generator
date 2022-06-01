from enum import Enum
from itertools import product
import random
import sys
from buttons import *
import pygame
from collections import namedtuple

sys.setrecursionlimit(1700)
Position = namedtuple("Position", ["x", "y"])

y_offset = 100
x_offset = 450

timer = pygame.time.Clock()
SIZE = 29
SCREENSIZE = Position(1600, 900)

screen = pygame.display.set_mode(SCREENSIZE)

class Tile:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.generated = False
        self.right = True
        self.visited = 0
        self.left = True
        self.Up = True
        self.bottom = True

    def update(self):
        pass

    def draw(self, screen):
        if self.left:
            pygame.draw.line(screen, (0,0,0), (self.x, self.y), (self.x, self.y + self.size), 1)
        if self.right:
            pygame.draw.line(screen, (0,0,0), (self.x + self.size, self.y), (self.x + self.size, self.y + self.size), 1)
        if self.bottom:
            pygame.draw.line(screen, (0,0,0), (self.x , self.y + self.size), (self.x + self.size, self.y + self.size), 1)
        if self.Up:
            pygame.draw.line(screen, (0,0,0), (self.x, self.y), (self.x + self.size, self.y), 1)

class Field:
    def __init__(self):
        size = (SCREENSIZE.y - y_offset*2) / SIZE
        self.tiles = []
        for i in range(SIZE):
            row = []
            for k in range(SIZE):
                tile = Tile(i * size + x_offset, k  * size + y_offset, size)##################################################################
                row.append(tile)
            self.tiles.append(row)

    def update(self, screen):
        for i, k in product(range(SIZE), range(SIZE)):
            self.tiles[i][k].draw(screen)

    def clear_generation(self):
        for i, k in product(range(SIZE), range(SIZE)):
            self.tiles[i][k].left = True
            self.tiles[i][k].Up = True
            self.tiles[i][k].bottom = True
            self.tiles[i][k].right = True
            self.tiles[i][k].generated = False

    def generate(self):
        self.clear_generation()
        all_moves = []
                
        def check_neighbours(tile: Tile):
            sides = []

            def check_in_range(ind_x, ind_y):
                if in_range(ind_x, ind_y) and not self.tiles[ind_x][ind_y].generated: # replace tile with givven one
                    sides.append(self.tiles[ind_x][ind_y])

            def get_index(pos_x, pos_y):
                for i in range(SIZE):
                    for k in range(SIZE):
                        if self.tiles[i][k].x == pos_x and self.tiles[i][k].y == pos_y:
                            return i, k
                return None

            i, k = get_index(tile.x, tile.y)

            check_in_range(i - 1, k)
            check_in_range(i + 1, k)
            check_in_range(i, k + 1)
            check_in_range(i, k - 1)

            return sides

        def is_dead_end( moves):
            if len(moves) == 0:
                return True
            else:
                return False

        def move(tile: Tile):
            tile.generated = True
            all_moves.append(tile)
            moves = check_neighbours(tile)
            dead_end = is_dead_end(moves)

            if done():
                return

            if not dead_end:
                random_ind = random.randint(0, len(moves) - 1)
                clear_walls(tile, moves[random_ind])
                move(moves[random_ind])
                
            else:
                ind = get_move_index(tile) # here must be smth that will return to previous move
                move(all_moves[ind - 1])

            

        def done():
            for i, k in product(range(SIZE), range(SIZE)):
                if self.tiles[i][k].generated == False:
                    return False
            return True

        def get_move_index(move):
            for i in range(len(all_moves)):
                if all_moves[i] == move:
                    return i

        def clear_walls(tile: Tile, moving_to: Tile):
            
            if moving_to.x > tile.x: #####
                tile.right = False
                moving_to.left = False

            if moving_to.x < tile.x: ###
                tile.left = False
                moving_to.right = False

            if moving_to.y > tile.y:
                tile.bottom = False
                moving_to.Up = False

            if moving_to.y < tile.y:
                tile.Up = False
                moving_to.bottom = False



        def in_range(pos_x, pos_y):
            if pos_x > SIZE - 1 or pos_y > SIZE - 1:
                return False
            if pos_x < 0 or pos_y < 0:
                return False
            return True

        move(self.tiles[0][SIZE - 1])


class Direction(Enum):
    Right = 0
    Left = 1
    Down = 2
    Up = 3

class Bot:
    
    def __init__(self, tiles: Tile):
        global len
        self.tiles = tiles
        size = (SCREENSIZE.y - y_offset*2) / SIZE
        self.tiles[0][SIZE - 1].visited = 2
        self.direction = Direction.Right
        self.image = pygame.Surface((100 - SIZE * 3, 100 - SIZE * 3))
        self.image.fill((100, 100, 100))       
        self.pos = Position(0, SIZE - 1)
        #self.move()

    def update(self, screen):
        x_pos = x_offset + self.pos.x * self.tiles[0][0].size + self.tiles[0][0].size / 2
        y_pos = y_offset + self.pos.y * self.tiles[0][0].size + self.tiles[0][0].size / 2
        #print(x_pos, y_pos)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def move(self):
        while self.pos != Position(SIZE - 1, 0):
            self.check_all()
            #print(self.pos)

    def check_and_move(self, pos_x, pos_y, dir: Direction):
        if self.in_range(pos_x, pos_y):
            if not self.check_wall(pos_x, pos_y, dir) and not self.tiles[pos_x][pos_y].visited >= 2:
                #print("new position is ", pos_x, pos_y)
                self.direction = dir
                self.pos = Position(pos_x, pos_y)
                return True
        return False

    def check_all(self):
        if self.direction == Direction.Right:
            can_move = self.check_and_move(self.pos.x, self.pos.y + 1, Direction.Down)
            if not can_move:
                can_move = self.check_and_move(self.pos.x + 1, self.pos.y, Direction.Right)
                if not can_move:
                    can_move = self.check_and_move(self.pos.x, self.pos.y - 1, Direction.Up)
                    if not can_move:
                        can_move = self.check_and_move(self.pos.x - 1, self.pos.y, Direction.Left)
            return

        if self.direction == Direction.Down:
            can_move = self.check_and_move(self.pos.x - 1, self.pos.y, Direction.Left)
            if not can_move:
                can_move = self.check_and_move(self.pos.x, self.pos.y + 1, Direction.Down)
                if not can_move:
                    can_move = self.check_and_move(self.pos.x + 1, self.pos.y, Direction.Right)
                    if not can_move:
                        can_move = self.check_and_move(self.pos.x, self.pos.y - 1, Direction.Up)
            return

        if self.direction == Direction.Left:
            can_move = self.check_and_move(self.pos.x, self.pos.y - 1, Direction.Up)
            if not can_move:
                can_move = self.check_and_move(self.pos.x - 1, self.pos.y, Direction.Left)
                if not can_move:
                    can_move = self.check_and_move(self.pos.x, self.pos.y + 1, Direction.Down)
                    if not can_move:
                        can_move = self.check_and_move(self.pos.x + 1, self.pos.y, Direction.Right)
            return
        
        if self.direction == Direction.Up:
            can_move = self.check_and_move(self.pos.x + 1, self.pos.y, Direction.Right)
            if not can_move:
                can_move = self.check_and_move(self.pos.x, self.pos.y - 1, Direction.Up)
                if not can_move:
                    can_move = self.check_and_move(self.pos.x - 1, self.pos.y, Direction.Left)
                    if not can_move:
                        can_move = self.check_and_move(self.pos.x, self.pos.y + 1, Direction.Down)
            return
                                    

    def in_range(self, pos_x, pos_y):
        if pos_x < 0 or pos_y < 0:
            return False
        if pos_x > SIZE - 1 or pos_y > SIZE - 1:
            return False
        return True

    def check_wall(self, pos_x, pos_y, dir):
        x = self.pos.x
        y = self.pos.y

        if dir == Direction.Right:
            return self.tiles[x][y].right and self.tiles[pos_x][pos_y].left

        if dir == Direction.Left:
            return self.tiles[x][y].left and self.tiles[pos_x][pos_y].right

        if dir == Direction.Down:
            return self.tiles[x][y].bottom and self.tiles[pos_x][pos_y].Up

        if dir == Direction.Up:
            return self.tiles[x][y].Up and self.tiles[pos_x][pos_y].bottom
        
        return None


def start_solve():
    global solving
    solving = True
    bot.pos = Position(0, SIZE - 1)

def stop_solve():
    global solving
    solving = False
    bot.pos = Position(0, SIZE - 1)

def slider_work(slider_list):
    global SIZE
    SIZE = int(slider_list[0])

    size = (SCREENSIZE.y - y_offset*2) / SIZE
    for i, k in product(range(SIZE), range(SIZE)):
        field.tiles[i][k].x = i * size + x_offset
        field.tiles[i][k].y = k  * size + y_offset
        field.tiles[i][k].size = size
    print("at slider", 100 - SIZE * 3.29)
    bot.image = pygame.Surface((100 - SIZE * 3.29 , 100 - SIZE * 3.29))
    bot.image.fill((100, 100, 100))

    field.generate()

field = Field()
field.generate()

bot = Bot(field.tiles)

game_on = True
solving = False

btns = pygame.sprite.Group()
sliders = pygame.sprite.Group()
lbls = pygame.sprite.Group()

generate_button = mButton(1400, 100, 150, 50, (100, 100, 100), (255, 255, 255), "Generate", screen, field.generate)
solve_button = mButton(1400, 200, 150, 50, (100, 100, 100), (255, 255, 255), "Solve", screen, start_solve)
stop_button = mButton(1400, 300, 150, 50, (100, 100, 100), (255, 255, 255), "Stop", screen, stop_solve)
size_slider = Slider(1300, 400, 250, 10, (100, 100, 100), screen, 40, 20, 2, 30, ((20, 20, 20)))
size_label = Label(1390, 450, 200, 50, (255, 255, 255), (50, 50, 50), "Size", screen)

btns.add(generate_button, solve_button, stop_button)
sliders.add(size_slider)
lbls.add(size_label)

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            slider_list = []
            size_slider.drag(slider_list)
            if len(slider_list) > 0:
                slider_work(slider_list)

        if event.type == pygame.MOUSEBUTTONUP:
            generate_button.check_pressed()
            solve_button.check_pressed()
            stop_button.check_pressed()

    if solving:
        if bot.pos != Position(SIZE - 1, 0):
            bot.check_all()

    screen.fill((255,255,255))
    
    field.update(screen)

    btns.draw(screen)
    btns.update(None)

    lbls.draw(screen)
    lbls.update(None)

    sliders.update()

    bot.update(screen)
    screen.blit(bot.image, bot.rect)
    pygame.display.flip()
    timer.tick(7)

