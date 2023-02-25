import pygame
from sys import exit
from random import randint
import math
import os
import neat


def calculate_angle_between_crab_and_food(crab_degrees, crab_pos, food_pos):
    x1 = crab_pos[0]
    x2 = food_pos[0]
    y1 = crab_pos[1]
    y2 = food_pos[1]
    # angle = crab_degrees - math.degrees(math.atan((y2 - y1) / (x2 - x1)))
    if y2 <= y1 and x2 >= x1:
        if x2 == x1:
            angle = crab_degrees - abs(math.degrees(math.atan(y2 - y1)))
        else:
            angle = crab_degrees - abs(math.degrees(math.atan((y2 - y1) / (x2 - x1))))
        if angle > 0:
            return angle
        if angle < 0:
            return 360 + angle

    if y2 <= y1 and x2 <= x1:
        if y2 == y1:
            angle = crab_degrees - math.degrees(math.atan((x2 - x1)))
        else:
            angle = crab_degrees - math.degrees(math.atan((x2 - x1) / (y2 - y1))) - 90
        if angle > 0:
            return angle
        elif angle < 0:
            return 360 + angle

    if y2 >= y1 and x2 <= x1:
        if y2 == y1:
            angle = crab_degrees - math.degrees(math.atan((x2 - x1)))
        else:
            angle = crab_degrees - math.degrees(math.atan((x2 - x1) / (y2 - y1)))
        return (angle + 90) % 360

    if y2 >= y1 and x2 >= x1:
        if y2 == y1:
            angle = crab_degrees - math.degrees(math.atan(x2 - x1))
        else:
            angle = crab_degrees - math.degrees(math.atan((x2 - x1) / (y2 - y1))) + 90
        return angle % 360



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
        self.been_clicked()

    def been_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.body_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                return True
            else:
                if self.clicked:
                    self.clicked = False


start_button_title = Button("Start", 150, 50, (325, 400))
play_again_button = Button("Play again?", 150, 50, (325, 400))
exit_button = Button("Exit", 150, 50, (325, 470))


# Organism
class Organism(pygame.sprite.Sprite):
    def __init__(self, speed, x_position, y_position):
        super().__init__()
        crab1 = pygame.image.load("images/crab1.png").convert_alpha()
        self.image = crab1
        self.original_image = self.image.copy()
        self.rect = crab1.get_rect(center=(x_position, y_position))

        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.position = pygame.Vector2(self.rect.center)

        self.speed = speed * -2
        self.energy = 1000000
        self.time_alive = 0

        self.xy = (self.position.x, self.position.y)
        self.smallest_distance = 0
        self.angle_to_turn = 0

    def update_xy(self):
        self.xy = (self.position.x, self.position.y)

    def draw(self):
        screen.blit(self.image, self.rect)

    # Player inputs
    def player_input(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_w]:
    #         self.move_forward()
    #     if keys[pygame.K_a]:
    #         self.turn_left()
    #     if keys[pygame.K_d]:
    #         self.turn_right()
        self.rect.center = round(self.position[0]), round(self.position[1])

    def turn_left(self):
        self.angle += 5
        self.angle %= 360

    def turn_right(self):
        self.angle -= 5
        self.angle %= 360

    # Rotating
    def rotate(self):
        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move_forward(self):
        direction = pygame.Vector2(0, self.speed).rotate(-self.angle)
        self.position += direction
        self.energy -= abs(self.speed)

    def metabolism(self):
        self.energy -= 10

    def collided(self, food):
        if pygame.Rect.colliderect(self.rect, food):
            return True
        return False

    # Updating the organism
    def update(self):
        self.player_input()
        self.rotate()
        self.metabolism()
        self.time_alive += 1 / 60
        self.draw()
        self.update_xy()

        # Stopping organism from going out of screen
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > 800:
            self.position.x = 800
        elif self.position.y < 0:
            self.position.y = 0
        elif self.position.y > 630:
            self.position.y = 630
        #
        if self.energy > 1500:
            self.energy = 1500



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
def main(genomes, config):
    # different screens and menus
    title_font = pygame.font.Font("Fonts/pixelatedfont.ttf", 45)
    title_name_surf = title_font.render("Project", False, (0, 0, 0))
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

    nets = []
    ge = []
    crabs = []

    for _, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        crabs.append(Organism(1, randint(0, 800), randint(350, 450)))
        ge.append(genome)

    foods = []
    food_coordinates = []
    while len(foods) != 50:
        food_x_spawn = randint(10, 790)
        food_y_spawn = randint(10, 630)
        foods.append(Food(food_x_spawn, food_y_spawn))
        food_coordinates.append((food_x_spawn, food_y_spawn))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if title_screen:
            screen.blit(title_background_surf, (0, 0))
            screen.blit(title_name_surf, title_name_rect)
            start_button_title.draw()
            if start_button_title.been_clicked():
                title_screen, main_screen = False, True

        elif main_screen and len(foods) > 0:

            if len(crabs) <= 0:
                break
            for x, crab in enumerate(crabs):
                # crab.move_forward()
                ge[x].fitness += 0.1

                output = nets[x].activate((crab.position.x, crab.angle_to_turn, crab.smallest_distance))
                if output[0] < 1/5:
                    crab.move_forward()
                elif 1/5 <output[0] < 3/5:
                    crab.turn_left()
                elif output[0] > 3/5:
                    crab.turn_right()

            while len(foods) != 50:
                food_x_spawn = randint(10, 790)
                food_y_spawn = randint(10, 630)
                foods.append(Food(food_x_spawn, food_y_spawn))
                food_coordinates.append((food_x_spawn, food_y_spawn))

            screen.blit(main_background_surf, (0, 0))
            for x, crab in enumerate(crabs):
                distances_from_crab = []
                list_of_food_coords = []
                for food in foods:
                    for food_coord in food_coordinates:
                        distances_from_crab.append([calculate_distance(crab.xy, food_coord)])
                        list_of_food_coords.append(food_coord)
                    food.draw()
                    if crab.collided(food):
                        for g in ge:
                            g.fitness += 4
                        foods.remove(food)
                        food_coordinates.remove(food.xy)
                        list_of_food_coords.remove(food.xy)
                        distances_from_crab.remove(min(distances_from_crab))
                        crab.energy += 500
                    smallest_distance = min(distances_from_crab)
                    crab.smallest_distance = int(min(distances_from_crab)[0])
                    smallest_distance_coords = list_of_food_coords[distances_from_crab.index(smallest_distance)]

                crab.update()
                if crab.energy < 0 or crab.energy == 0:
                    ge[x].fitness -= 10
                    crabs.remove(crab)
                    nets.pop(x)
                    ge.pop(x)

                amount_of_energy = crab.energy
                # energy_info_surf = text_font.render("Energy: " + str(int(amount_of_energy)), False, (0, 0, 0))
                # energy_info_rect = energy_info_surf.get_rect(midleft=(20, 50))
                # screen.blit(energy_info_surf, energy_info_rect)

                time_alive = crab.time_alive
                # time_alive_surf = text_font.render("Time Alive: " + str(int(time_alive)), False, (0, 0, 0))
                # time_alive_rect = time_alive_surf.get_rect(midleft=(20, 70))
                # screen.blit(time_alive_surf, time_alive_rect)

                direction_facing = (crab.angle + 90) % 360
                # angle_surf = text_font.render("Angle: " + str(crab.angle), False, (0, 0, 0))
                # angle_rect = angle_surf.get_rect(midleft=(20, 90))
                # screen.blit(angle_surf, angle_rect)

                # crabcoords_surf = text_font.render("crab coords: (" + str(int(crab.position.x)) + ", " + str(int(crab.position.y)) + ")", False, (0, 0, 0))
                # crabcoords_rect = crabcoords_surf.get_rect(midleft=(20, 110))
                # screen.blit(crabcoords_surf, crabcoords_rect)

                shortest_distance_surf = text_font.render("shortest distance: " + str(crab.smallest_distance), False, (0, 0, 0))
                # shortest_distance_rect = shortest_distance_surf.get_rect(midleft=(20, 130))
                # screen.blit(shortest_distance_surf, shortest_distance_rect)

                shortest_distance_coords_surf = text_font.render("coords of closest food " + str(smallest_distance_coords), False, (0, 0, 0))
                # shortest_distance_coords_rect = shortest_distance_coords_surf.get_rect(midleft=(20, 150))
                # screen.blit(shortest_distance_coords_surf, shortest_distance_coords_rect)
                pygame.draw.line(screen, (0, 0, 0), (crab.position.x, crab.position.y), smallest_distance_coords, 2)

                crab.angle_to_turn = int(calculate_angle_between_crab_and_food(direction_facing, (crab.position.x, crab.position.y), (smallest_distance_coords)))
                # angle_to_turn_surf = text_font.render("angle to turn: " + str(crab.angle_to_turn), False, (0, 0, 0))
                # angle_to_turn_rect = crabcoords_surf.get_rect(midleft=(20, 170))
                # screen.blit(angle_to_turn_surf, angle_to_turn_rect)


        pygame.display.update()
        clock.tick(60)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)