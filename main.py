import neat.config
import pygame
from sys import exit
from random import randint
import os
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
text_font = pygame.font.Font("Fonts/Pixeltype.ttf", 30)
main_background_surf = pygame.image.load("Backgrounds/mainbackground.png").convert()
main_screen = False

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
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                return True
            else:
                if self.clicked:
                    self.clicked = False


start_button_title = Button("Start", 150, 50, (325, 400))
pause_button = Button("Pause", 150, 50, (600, 700))


# Organism
class Organism(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        crab1 = pygame.image.load("images/crab1.png").convert_alpha()
        self.image = crab1
        self.original_image = self.image.copy()
        self.rect = crab1.get_rect(center=(400, 625))

        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.pos = pygame.Vector2(self.rect.center)

        self.speed = speed * -1
        self.energy = 1000
        self.time_alive = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    # Player inputs
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move_forward()
        if keys[pygame.K_a]:
            self.turn_left()
        if keys[pygame.K_d]:
            self.turn_right()
        self.rect.center = round(self.pos[0]), round(self.pos[1])

    def turn_left(self):
        self.angle += 5

    def turn_right(self):
        self.angle -= 5

    def move_forward(self):
        direction = pygame.Vector2(0, self.speed).rotate(-self.angle)
        self.pos += direction
        self.energy -= abs(self.speed)

    # Rotating the organism
    def rotate(self):
        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def metabolism(self):
        self.energy -= 0.8

    def collided(self, food):
        if pygame.Rect.colliderect(self.rect, food):
            return True
        return False

    # Updating the organism
    def update(self):
        if self.energy > 0:
            self.player_input()
            self.rotate()
            self.metabolism()
            self.time_alive += 1 / 60
            self.draw()
        else:
            self.energy = 0

        # Stopping organism from going out of screen
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > 800:
            self.pos.x = 800
        elif self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > 630:
            self.pos.y = 630

        if self.energy > 1000:
            self.energy = 1000


crab = (Organism(2))


class Food(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        seaweed1 = pygame.image.load("images/seaweed1.png").convert_alpha()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = seaweed1

    def draw(self):
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        screen.blit(self.image, self.rect)


# Game loop
def main(genomes, config):
    # different screens and menus
    title_font = pygame.font.Font("Fonts/pixelatedfont.ttf", 45)
    title_name_surf = title_font.render("Evolution Simulator", False, (0, 0, 0))
    title_name_rect = title_name_surf.get_rect(center=(screen_width / 2, 200))
    title_background_surf = pygame.image.load("Backgrounds/titlebackground.png").convert()
    title_screen = True
    text_font = pygame.font.Font("Fonts/Pixeltype.ttf", 30)
    main_background_surf = pygame.image.load("Backgrounds/mainbackground.png").convert()
    main_screen = False
    
    foods = []
    for x in range(100):
        foods.append(Food(randint(0, 800), randint(0, 630)))

    crabs = []
    crabs.append(Organism(2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if title_screen:
            screen.blit(title_background_surf, (0, 0))
            screen.blit(title_name_surf, title_name_rect)
            start_button_title.draw()
            if start_button_title.check_click():
                title_screen, main_screen = False, True

        elif main_screen:
            screen.blit(main_background_surf, (0, 0))
            for crab in crabs:
                for food in foods:
                    food.draw()
                    if crab.collided(food):
                        foods.remove(food)
                        crab.energy += 50
                crab.update()
            pause_button.draw()
            for crab in crabs:
                amount_of_energy = crab.energy
                energy_info_surf = text_font.render("Energy: " + str(int(amount_of_energy)), False, (0, 0, 0))
                energy_info_rect = energy_info_surf.get_rect(center=(100, 50))
                screen.blit(energy_info_surf, energy_info_rect)
                time_alive = crab.time_alive
                time_alive_surf = text_font.render("Time Alive: " + str(int(time_alive)), False, (0, 0, 0))
                time_alive_rect = time_alive_surf.get_rect(center=(100, 70))
                screen.blit(time_alive_surf, time_alive_rect)

        pygame.display.update()
        clock.tick(60)


main(1, 1)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter
    p.add_reporter(stats)

    winner = p.run(main, 50)

# if __name__ == "__main__":
    # local_dir = os.path.dirname(__file__)
    # config_path = os.path.join(local_dir, "config-feedforward.txt")
    # run(config_path)
