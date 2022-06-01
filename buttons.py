import pygame
from threading import Thread

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 32)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, surface: pygame.Surface):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.surface = surface
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x, y))

class Label(Block):
    def __init__(self, x, y, width, height, color, text_color, text, surface: pygame.Surface):
        super().__init__(x, y, width, height, color, surface)
        self.text_color = text_color
        self.text = font.render(text, False, text_color, None)

    def update(self, text):
        if text != None:
            self.text = font.render(text, False, self.text_color, None)
        self.surface.blit(self.text, (self.rect))

class mButton(Label):
    def __init__(self, x, y, width, height, color, text_color, text, surface: pygame.Surface, func):
        super().__init__(x, y, width, height, color, text_color, text, surface)
        self.func = func
    
    def check_pressed(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.func()

class Slider(Block):
    def __init__(self, x, y, width, height, color, surface: pygame.Surface, slider_height, slider_width, min_value, max_value, slider_color):
        super().__init__(x, y, width, height, color, surface)
        self.sliderw = slider_width
        self.sliderh = slider_height
        self.max_x = self.x + width
        self.min_x = self.x
        self.min_value = min_value
        self.max_value = max_value
        self.value_per_pixel = (self.max_x - self.min_x) / (self.max_value - self.min_value)
        print(self.value_per_pixel)
        self.slider_color = slider_color
        self.slider_surf = pygame.Surface((self.sliderw, self.sliderh))
        self.slider_surf.fill(slider_color)
        self.slider_rect = self.slider_surf.get_rect(center = (self.x + self.width/2, self.y + self.height/2))

    def drag(self, list):
        need_to_return = False
        pos = pygame.mouse.get_pos()
        if not self.slider_rect.collidepoint(pos):
            return None

        while True:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    need_to_return = True

            if need_to_return:
                list.append((self.x - self.min_x) // self.value_per_pixel + self.min_value)
                return list

            self.x = pos[0]
            if self.x > self.max_x:
                self.x = self.max_x
            if self.x < self.min_x:
                self.x = self.min_x 
            self.slider_rect = self.slider_surf.get_rect(center = (self.x , self.y + self.height/2))

    def update(self):
        self.draw()

    def draw(self):
        self.surface.blit(self.image, self.rect)
        self.surface.blit(self.slider_surf, self.slider_rect)


"""


def dinma():
    print("body builder dima!!!")

lbl_group = pygame.sprite.Group()
btns_group = pygame.sprite.Group()
lbl_group.add(Label(100, 100, 300, 100, (100, 10, 100), (0, 100, 10), "im amongus", screen))
btn = Button(100, 400, 100, 100, (255,0,0), (0,255,0), "i am...", screen, dinma)
s = Slider(100, 550, 300, 10, (100, 100, 100), screen, 20, 10, 2, 20, (0,240,100))
btns_group.add(btn)

game_on = True
drag = False

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        

        if event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
            btn.check_pressed()
            l = []
            thread = Thread(target = s.drag(), args=(l))
            print(l)


        if event.type == pygame.MOUSEBUTTONUP:
            drag = False

    screen.fill((255,255,255))
    btns_group.draw(screen)
    btns_group.update(None)
    s.update()
    lbl_group.draw(screen)
    lbl_group.update(None)
    pygame.display.flip()
    """