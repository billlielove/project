import neat.config
import pygame
from sys import exit
from random import randint
import os
import math


def calculate_angle(crab_pos, food_pos):
    x1 = crab_pos[0]
    x2 = food_pos[0]
    y1 = crab_pos[1]
    y2 = food_pos[1]
    return math.atan(math.pi - abs(x1-x2)/abs(y1-y2))


def calculate_distance(crab_pos, food_pos):
    x1 = crab_pos[0]
    x2 = food_pos[0]
    y1 = crab_pos[1]
    y2 = food_pos[1]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# initialising pygame
pygame.init()
screen_height = 800
screen_width = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Project")
clock = pygame.time.Clock()

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
        self.energy = 10000
        self.time_alive = 0

        self.xy = (self.pos.x, self.pos.y)
        self.smallest_distance = None

    def update_xy(self):
        self.xy = (self.pos.x, self.pos.y)

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
        self.angle -= 5
        self.angle %= 360

    def turn_right(self):
        self.angle += 5
        self.angle %= 360

    def move_forward(self):
        direction = pygame.Vector2(0, self.speed).rotate(self.angle)
        self.pos += direction
        self.energy -= abs(self.speed)

    # Rotating the organism
    def rotate(self):
        self.direction = pygame.Vector2(1, 0).rotate(self.angle)
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def metabolism(self):
        self.energy -= 2

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
            self.update_xy()
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

        if self.energy > 10000:
            self.energy = 10000


crab = (Organism(10))


class Food(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        seaweed1 = pygame.image.load("images/seaweed1.png").convert_alpha()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = seaweed1
        self.xy = (self.x_pos, self.y_pos)

    def draw(self):
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        screen.blit(self.image, self.rect)


# Game loop
def main():
    # different screens and menus
    title_font = pygame.font.Font("Fonts/pixelatedfont.ttf", 45)
    title_name_surf = title_font.render("Evolution Simulator", False, (0, 0, 0))
    title_name_rect = title_name_surf.get_rect(center=(screen_width / 2, 200))
    title_background_surf = pygame.image.load("Backgrounds/titlebackground.png").convert()
    title_screen = True
    text_font = pygame.font.Font("Fonts/Pixeltype.ttf", 30)
    main_background_surf = pygame.image.load("Backgrounds/mainbackground.png").convert()
    main_screen = False
    win_font = pygame.font.Font("Fonts/pixelatedfont.ttf", 45)
    win_surf = win_font.render("YOU WIN", False, (0, 0, 0))
    win_rect = win_surf.get_rect(center=(screen_width / 2, 200))
    win_screen = False

    foods = []
    food_coordinates = []
    for x in range(20):
        food_x_spawn = randint(0, 800)
        food_y_spawn = randint(0, 630)
        foods.append(Food(food_x_spawn, food_y_spawn))
        food_coordinates.append((food_x_spawn, food_y_spawn))

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

        elif main_screen and len(foods) > 0:
            screen.blit(main_background_surf, (0, 0))
            for crab in crabs:
                distances_from_crab = []
                list_of_food_coords = []
                for food in foods:
                    for x, food_coord in enumerate(food_coordinates):
                        distances_from_crab.append([calculate_distance(crab.xy, food_coord)])
                        list_of_food_coords.append(food_coord)
                    food.draw()
                    if crab.collided(food):
                        foods.remove(food)
                        food_coordinates.remove(food.xy)
                        list_of_food_coords.remove(food.xy)
                        distances_from_crab.remove(min(distances_from_crab))
                        crab.energy += 200
                    if len(distances_from_crab) == 0:
                        main_screen = False
                        win_screen = True
                        break
                    smallest_distance = min(distances_from_crab)
                    crab.smallest_distance = int(min(distances_from_crab)[0])
                    smallest_distance_coords = list_of_food_coords[distances_from_crab.index(smallest_distance)]

                crab.update()
            for crab in crabs:
                amount_of_energy = crab.energy
                energy_info_surf = text_font.render("Energy: " + str(int(amount_of_energy)), False, (0, 0, 0))
                energy_info_rect = energy_info_surf.get_rect(midleft=(20, 50))
                screen.blit(energy_info_surf, energy_info_rect)
                time_alive = crab.time_alive
                time_alive_surf = text_font.render("Time Alive: " + str(int(time_alive)), False, (0, 0, 0))
                time_alive_rect = time_alive_surf.get_rect(midleft=(20, 70))
                screen.blit(time_alive_surf, time_alive_rect)

                angle_surf = text_font.render("Angle: " + str(int(crab.angle)), False, (0, 0, 0))
                angle_rect = angle_surf.get_rect(midleft=(20, 90))
                screen.blit(angle_surf, angle_rect)

                crabcoords_surf = text_font.render("x coords: (" + str(int(crab.pos.x)) + ", " + str(int(crab.pos.y)) + ")", False, (0, 0, 0))
                crabcoords_rect = crabcoords_surf.get_rect(midleft=(20, 110))
                screen.blit(crabcoords_surf, crabcoords_rect)

                shortest_distance_surf = text_font.render("shortest distance: " + str(crab.smallest_distance), False, (0, 0, 0))
                shortest_distance_rect = crabcoords_surf.get_rect(midleft=(20, 130))
                screen.blit(shortest_distance_surf, shortest_distance_rect)

                shortest_distance_coords_surf = text_font.render("coords of closest food " + str(smallest_distance_coords), False, (0, 0, 0))
                shortest_distance_coords_rect = shortest_distance_coords_surf.get_rect(midleft=(20, 150))
                screen.blit(shortest_distance_coords_surf, shortest_distance_coords_rect)
                pygame.draw.line(screen, (0, 0, 0), (crab.pos.x, crab.pos.y), smallest_distance_coords, 2)

        elif win_screen:
            screen.fill((255, 255, 255))
            screen.blit(win_surf, win_rect)

        pygame.display.update()
        clock.tick(60)


main()
