import pygame
from sys import exit
import random
import math


pygame.init()  # initialises pygame

# Screen and window settings for the program to run on
screen_height = 800  # Height of the screen in pixels
screen_width = 800  # Width of the screen in pixels
screen = pygame.display.set_mode((screen_width, screen_height))  # Making the screen for surfaces and rectangles to be placed on
pygame.display.set_caption("Evolution Simulator")  # Setting the caption or name of the window

# creating the clock object to work with time in Python
clock = pygame.time.Clock()

# Title screen surfaces and rectangles to display on the screen
title_font = pygame.font.Font("Fonts/pixelatedfont.ttf", 45)  # Getting the style and size of the font being used
title_name_surf = title_font.render("Evolution Simulator", False, (0, 0, 0))  # Creating the surface for the title name
title_name_rect = title_name_surf.get_rect(center=(screen_width / 2, 200))  # Converting the surface into a rectangle
title_background_surf = pygame.image.load("Backgrounds/titlebackground.png").convert()  # Getting the background image and turning it into a surface
title_screen = True

# Button fonts and other variables
button_font = pygame.font.Font("Fonts/pixelatedfont.ttf", 20)

# Main screen surface
main_background_surf = pygame.image.load("Backgrounds/mainbackground.png").convert()
main_screen = False

# Settings screen surface
settings_background_surf = pygame.image.load("Backgrounds/settingsbackground.png").convert()
settings_screen = False

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
        if self.body_rect.collidepoint(mouse_pos) == True:
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] == True:
                self.clicked = True
                return True
            else:
                if self.clicked:
                    self.clicked = False

class Organism(pygame.sprite.Sprite):
    def __init__(self, screen, speed):
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
# Buttons
start_button_title = Button("Start", 150, 50, (325, 400))
back_button = Button("Back", 150, 50, (30, 30))
options_button_main = Button("Options", 150, 50, (620, 30))
menu_button = Button("Menu", 150, 50, (620, 720))

# Crab
crab = pygame.sprite.GroupSingle()
crab.add(Organism(screen, 3))

# Game loop
while True:
    for event in pygame.event.get():  # while program is running, it gets every event that happens
        if event.type == pygame.QUIT:  # if the event gotten is quit
            pygame.quit()  # quits python
            exit()  # exits the window

    # Title screen
    if title_screen == True and settings_screen == False:  # Displaying surfaces and rectangles on the screen
        screen.blit(title_background_surf, (0, 0))  # displays the title background image onto the screen
        screen.blit(title_name_surf, title_name_rect)  # displays the title name on top of the background image on the screen
        start_button_title.draw()
        if start_button_title.check_click():
            title_screen, main_screen = False, True

    elif settings_screen == True:
        screen.blit(settings_background_surf, (0, 0))
        back_button.draw()
        menu_button.draw()
        if back_button.check_click() == True:
            main_screen, settings_screen = True, False
        if menu_button.check_click() == True:
            title_screen, settings_screen = True, False

    elif main_screen == True:
        screen.blit(main_background_surf, (0, 0))
        options_button_main.draw()
        if options_button_main.check_click() == True:
            settings_screen, main_screen = True, False
        crab.draw(screen)
        crab.update()

    pygame.display.update()  # updates the display
    clock.tick(60)  # Limits the runtime of the game to 60 ticks/frames per second
