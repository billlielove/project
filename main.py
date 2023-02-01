import pygame
from sys import exit

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

# Game loop
while True:
    for event in pygame.event.get():  # while program is running, it gets every event that happens
        if event.type == pygame.QUIT:  # if the event gotten is quit
            pygame.quit()  # quits python
            exit()  # exits the window

    # Displaying surfaces and rectangles on the screen
    screen.blit(title_background_surf, (0, 0))  # displays the title background image onto the screen
    screen.blit(title_name_surf, title_name_rect)  # displays the title name on top of the background image on the screen

    pygame.display.update()  # updates the display
    clock.tick(60)  # Limits the runtime of the game to 60 ticks/frames per second
