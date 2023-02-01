import pygame
from sys import exit

pygame.init()

# Screen settings
screen_height = 800
screen_width = 800
screen_dimensions = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_dimensions)
pygame.display.set_caption("Evolution Simulator")
clock = pygame.time.Clock()

# Title screen
title_font = pygame.font.Font("Fonts/pixelatedfont.ttf", 50)
title_name = title_font.render("Evolution Simulator", False, (0, 0, 0))
title_name_rect = title_name.get_rect(center=(screen_width/2, 200))
title_surf = pygame.image.load("Backgrounds/titlebackground.png").convert()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Title Screen
    screen.blit(title_surf,(0, 0))
    screen.blit(title_name, title_name_rect)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)