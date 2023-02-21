import pygame
from sys import exit
import random
import math

# initialising pygame
pygame.init()
screen_height = 800
screen_width = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Evolution Simulator")
clock = pygame.time.Clock()

# different screens and menus
title_font = pygame.font.Font("Fonts/pixelatedfont.ttf", 45)
title_name_surf = title_font.render("Evolution Simulator", False, (0, 0, 0))
title_name_rect = title_name_surf.get_rect(center=(screen_width / 2, 200))
title_background_surf = pygame.image.load("Backgrounds/titlebackground.png").convert()
title_screen = True
main_background_surf = pygame.image.load("Backgrounds/mainbackground.png").convert()
main_screen = False
settings_background_surf = pygame.image.load("Backgrounds/settingsbackground.png").convert()
settings_screen = False

# Buttons
button_font = pygame.font.Font("Fonts/pixelatedfont.ttf", 20)


class Button:
    def __init__(self, text, width, height, pos):
        self.clicked = False

        self.body_rect = pygame.Rect(pos, (width, height))
        self.body_colour = (145, 151, 176)

        self.text_surf = button_font.render(text, False, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.body_rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.body_colour, self.body_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.body_rect.collidepoint(mouse_pos):
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                return True
            else:
                if self.clicked:
                    self.clicked = False


start_button_title = Button("Start", 150, 50, (325, 400))
back_button = Button("Back", 150, 50, (30, 30))
options_button_main = Button("Options", 150, 50, (620, 30))
menu_button = Button("Menu", 150, 50, (620, 720))


# Organism
class Organism(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        crab1 = pygame.image.load("Crab/crab1.png").convert_alpha()
        self.image = crab1
        self.original_image = self.image.copy()
        self.rect = crab1.get_rect(center=(400, 625))

        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.pos = pygame.Vector2(self.rect.center)

        self.speed = speed * -1

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.angle += 3
        if keys[pygame.K_d]:
            self.angle -= 3

    def rotate(self):
        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        direction = pygame.Vector2(0, self.speed).rotate(-self.angle)
        self.pos += direction
        self.rect.center = round(self.pos[0]), round(self.pos[1])

    def update(self):
        self.player_input()
        self.rotate()
        self.move()

        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > 800:
            self.pos.x = 800
        elif self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > 800:
            self.pos.y = 800


crab = pygame.sprite.GroupSingle()
crab.add(Organism(3))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if title_screen and not settings_screen:
        screen.blit(title_background_surf, (0, 0))
        screen.blit(title_name_surf, title_name_rect)
        start_button_title.draw()
        if start_button_title.check_click():
            title_screen, main_screen = False, True

    elif settings_screen:
        screen.blit(settings_background_surf, (0, 0))
        back_button.draw()
        menu_button.draw()
        if back_button.check_click():
            main_screen, settings_screen = True, False
        if menu_button.check_click():
            title_screen, settings_screen = True, False

    elif main_screen:
        screen.blit(main_background_surf, (0, 0))
        options_button_main.draw()
        if options_button_main.check_click():
            settings_screen, main_screen = True, False
        crab.draw(screen)
        crab.update()

    pygame.display.update()
    clock.tick(60)
