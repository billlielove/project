import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
