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
    if y2 <= y1 and x2 >= x1:
        if x2 == x1:
            angle = crab_degrees - abs(math.degrees(math.atan(y2 - y1)))
        else:
            angle = crab_degrees - abs(math.degrees(math.atan((y2 - y1) / (x2 - x1))))
        if angle > 0:
            angle = angle
        if angle < 0:
            angle += 360

    elif y2 <= y1 and x2 <= x1:
        if y2 == y1:
            angle = crab_degrees - math.degrees(math.atan((x2 - x1)))
        else:
            angle = crab_degrees - math.degrees(math.atan((x2 - x1) / (y2 - y1))) - 90
        if angle < 0:
            angle += 360

    elif y2 >= y1 and x2 <= x1:
        if y2 == y1:
            angle = crab_degrees - math.degrees(math.atan((x2 - x1)))
        else:
            angle = crab_degrees - math.degrees(math.atan((x2 - x1) / (y2 - y1)))
        angle = (angle + 90) % 360

    elif y2 >= y1 and x2 >= x1:
        if y2 == y1:
            angle = crab_degrees - math.degrees(math.atan(x2 - x1))
        else:
            angle = crab_degrees - math.degrees(math.atan((x2 - x1) / (y2 - y1))) + 90
        angle = angle % 360
    if angle > 180:
        angle -= 360
    return angle


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
class Text:
    def __init__(self, text, font, position):
         self.font = font
         self.surf = self.font.render(text, False, (0, 0, 0))
         self.rect = self.surf.get_rect(midleft=position)
    def draw(self):
        screen.blit(self.surf, self.rect)


start_button_title = Button("Start Generation", 300, 50, (250, 400))
play_again_button = Button("Play again?", 150, 50, (325, 400))
exit_button = Button("Exit", 150, 50, (325, 470))
settings_button = Button("Settings", 150, 50, (325, 470))
back_button = Button("Back", 150, 50, (20, 20))


# Organism
class Organism(pygame.sprite.Sprite):
    def __init__(self, speed, x_position, y_position, image):
        super().__init__()
        crab1 = pygame.image.load(image).convert_alpha()
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

    def center_update(self):
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
        self.energy -= 7

    def collided(self, food):
        if pygame.Rect.colliderect(self.rect, food):
            return True
        return False

    # Updating the organism
    def update(self):
        self.center_update()
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


class PlayerControlledOrganism(Organism):
    def __init__(self, Speed, Xpos, Ypos, Image):
        super().__init__(speed=Speed, x_position=Xpos, y_position=Ypos, image=Image)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move_forward()
        if keys[pygame.K_a]:
            self.turn_left()
        if keys[pygame.K_d]:
            self.turn_right()

    def update(self):
        self.player_input()
        self.center_update()
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

generation = 0
def main(genomes, config):
    global generation
    generation += 1
    title_font = pygame.font.Font("Fonts/pixelatedfont.ttf", 45)
    title_name_surf = title_font.render("Project", False, (0, 0, 0))
    title_name_rect = title_name_surf.get_rect(center=(screen_width / 2, 200))
    title_background_surf = pygame.image.load("Backgrounds/titlebackground.png").convert()
    title_screen = True
    text_font = pygame.font.Font("Fonts/Pixeltype.ttf", 30)
    main_background_surf = pygame.image.load("Backgrounds/mainbackground.png").convert()
    main_screen = False
    settings_background_surf = pygame.image.load("Backgrounds/settingsbackground.png").convert()
    settings_screen = False

    nets = []
    ge = []
    crabs = []
    players = []

    players.append(PlayerControlledOrganism(1, randint(0, 800), randint(350, 450), "images/player1.png"))

    for _, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        crabs.append(Organism(1, randint(0, 800), randint(350, 450), "images/crab1.png"))
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
            settings_button.draw()
            if start_button_title.been_clicked():
                title_screen, main_screen = False, True
            if settings_button.been_clicked():
                settings_screen, title_screen = True, False

        if settings_screen:
            screen.blit(settings_background_surf, (0, 0))
            back_button.draw()
            if back_button.been_clicked():
                title_screen, settings_screen = True, False

        elif main_screen and not settings_screen and len(foods) > 0:

            if len(crabs) <= 0:
                break
            for x, crab in enumerate(crabs):
                ge[x].fitness += 0.1
                crab.move_forward()

                output = nets[x].activate((crab.energy, crab.angle_to_turn, crab.smallest_distance))

                if 1/2 < output[0]:
                    crab.turn_right()
                else:
                    crab.turn_left()

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

                direction_facing = (crab.angle + 90) % 360
                crab.angle_to_turn = int(calculate_angle_between_crab_and_food(direction_facing, (crab.position.x, crab.position.y), (smallest_distance_coords)))
                pygame.draw.line(screen, (0, 0, 0), (crab.position.x, crab.position.y), smallest_distance_coords, 2)

            for x, crab in enumerate(players):
                distances_from_crab = []
                list_of_food_coords = []
                for food in foods:
                    for food_coord in food_coordinates:
                        distances_from_crab.append([calculate_distance(crab.xy, food_coord)])
                        list_of_food_coords.append(food_coord)
                    food.draw()
                    if crab.collided(food):
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
                    players.remove(crab)
                amount_of_energy = crab.energy
                time_alive = crab.time_alive
                direction_facing = (crab.angle + 90) % 360
                crab.angle_to_turn = int(calculate_angle_between_crab_and_food(direction_facing, (crab.position.x, crab.position.y), (smallest_distance_coords)))
                pygame.draw.line(screen, (0, 0, 0), (crab.position.x, crab.position.y), smallest_distance_coords, 2)

                energy_display = Text("Energy: " + str(int(amount_of_energy)), text_font, (20, 50))
                energy_display.draw()

                time_alive_display = Text("Time Alive: " + str(int(time_alive)), text_font, (20, 70))
                time_alive_display.draw()

                angle = Text("Angle: " + str(crab.angle), text_font, (20, 90))
                angle.draw()

                crab_coordinates_display = Text("Crab Coordinates: (" + str(int(crab.position.x)) + ", " + str(int(crab.position.y)) + ")", text_font, (20, 110))
                crab_coordinates_display.draw()

                shortest_distance_display = Text("Shortest Distance: " + str(crab.smallest_distance), text_font, (20, 130))
                shortest_distance_display.draw()

                coordinates_food_display = Text("Coordinates of closest food: " + str(smallest_distance_coords), text_font, (20, 150))
                coordinates_food_display.draw()

                angle_turn_display = Text("Angle to turn: " + str(crab.angle_to_turn), text_font, (20, 170))
                angle_turn_display.draw()

            generation_display = Text("Generation: " + str(generation), text_font, (20, 30))
            generation_display.draw()
        pygame.display.update()
        clock.tick(60)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(main, 10)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

# def move_forward(self):
#     direction = pygame.Vector2(0, self.speed).rotate(-self.angle)
#     self.position += direction
#     self.energy -= self.speed
#
# def turn_left(self):
#     self.angle += 5
#     self.angle %= 360
#
# def turn_right(self):
#     self.angle -= 5
#     self.angle %= 360
#
# def rotate(self):
#     self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
#     self.image = pygame.transform.rotate(self.original_image, self.angle)
#     self.rect = self.image.get_rect(center=self.rect.center)

# self.direction = pygame.Vector2(1, 0)
# self.position = pygame.Vector2(self.rect.center)
