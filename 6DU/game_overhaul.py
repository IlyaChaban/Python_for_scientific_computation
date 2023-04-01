import pygame
import random

SCREEN_RESOLUTION = (640, 480)

AMOUNT_OF_ENEMIES = 10

BACKGROUND_IMAGE = pygame.image.load("BACKGROUND2.png")
#BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, SCREEN_RESOLUTION)

MENU_IMAGE = pygame.image.load("MAIN_MENU.png")
MENU_IMAGE = pygame.transform.scale(MENU_IMAGE, SCREEN_RESOLUTION)

MAIN_MENU_IMAGE = pygame.image.load("MAIN_MENU.png")
MAIN_MENU_IMAGE = pygame.transform.scale(MAIN_MENU_IMAGE, SCREEN_RESOLUTION)

ROCKET_SIZE = (280, 280)
ROCKET_IMAGE = pygame.image.load("rocket.png")
ROCKET_IMAGE = pygame.transform.scale(ROCKET_IMAGE, ROCKET_SIZE)
ROCKET_INITIAL_POSITION = [SCREEN_RESOLUTION[0]/2 - ROCKET_SIZE[0]/2,
                           SCREEN_RESOLUTION[1]-ROCKET_SIZE[1]/2-50]
ROCKET_HITBOX_SIZE = (40, 100)
ROCKET_INITIAL_HITBOX = [ROCKET_INITIAL_POSITION[0]+ROCKET_SIZE[0]/2-ROCKET_HITBOX_SIZE[0]/2,
                         ROCKET_INITIAL_POSITION[1],
                         ROCKET_HITBOX_SIZE[0],
                         ROCKET_HITBOX_SIZE[1]]
ROCKET_SPEED = 10
ROCKET_BOUNDARIES = (0-ROCKET_SIZE[0], SCREEN_RESOLUTION[0]-ROCKET_SIZE[1])

ENEMY_SIZE = (30, 30)
ENEMY1_IMAGE = pygame.image.load("ENEMY.png")
ENEMY1_IMAGE = pygame.transform.scale(ENEMY1_IMAGE, ENEMY_SIZE)

ENEMY2_IMAGE = pygame.image.load("ENEMY2.png")
ENEMY2_IMAGE = pygame.transform.scale(ENEMY2_IMAGE, ENEMY_SIZE)

ENEMIES_IMAGES = [ENEMY1_IMAGE, ENEMY2_IMAGE]

ENEMY_SPEED = 5
FPS = 30

SCORE = 0


class Rocket:
    def __init__(self):
        self.image = ROCKET_IMAGE
        self.x_position = ROCKET_INITIAL_POSITION[0]
        self.y_position = ROCKET_INITIAL_POSITION[1]
        self.hitbox = ROCKET_INITIAL_HITBOX.copy()
        self.boundary_x = ROCKET_BOUNDARIES
        self.speed = ROCKET_SPEED

    def move(self, move):

        move_left = move[0]
        move_right = move[1]
        # move rocket and hitbox
        if self.x_position > 0 - ROCKET_SIZE[0]/2:
            if move_left:
                self.x_position -= self.speed
                self.hitbox[0] -= self.speed
        if self.x_position < SCREEN_RESOLUTION[0]-ROCKET_SIZE[0]/2:
            if move_right:
                self.x_position += self.speed
                self.hitbox[0] += self.speed

        # check boundariex


class Enemy:
    def __init__(self, y_position=0, x_position=random.uniform(0, SCREEN_RESOLUTION[0])):
        self.image = ENEMIES_IMAGES[int(random.randint(0, 1))]
        self.x_position = x_position
        self.y_position = y_position - random.uniform(30, 60)
        self.hitbox = [self.x_position, self.y_position, ENEMY_SIZE[0], ENEMY_SIZE[1]]
        self.speed = ENEMY_SPEED

    def fall(self):
        self.y_position += self.speed
        if self.y_position > SCREEN_RESOLUTION[1]:
            self.y_position = 0 - ENEMY_SIZE[1] - random.randint(ENEMY_SIZE[1], ENEMY_SIZE[1]*2)
            self.x_position = random.uniform(0, SCREEN_RESOLUTION[0])
            self.speed += random.randint(-10, 10)
            global SCORE
            SCORE += 1


class Game:
    def __init__(self, number_of_enemies = AMOUNT_OF_ENEMIES):
        self.number_of_enemies = number_of_enemies
        self.in_game = False
        self.quit = False
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREEN_RESOLUTION)
        self.score = 0

        self.menu_or_play()

    def menu_or_play(self):
        if not self.quit:
            while not self.in_game:
                # show main menu image
                self.screen.blit(MENU_IMAGE, (0, 0))
                # show score
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render(f'Score: {SCORE}', True, (0, 0, 0), (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (100, 100)
                self.screen.blit(text, textRect)



                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit = True
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        self.in_game = True
                        self.initialize_game()

                pygame.display.update()
                self.clock.tick(FPS)
        else:
            return None

    def initialize_game(self):
        # initialize game environtment
        self.screen.fill((100, 100, 100))
        self.screen.blit(BACKGROUND_IMAGE, (0, 0))
        pygame.display.update()
        self.clock.tick(FPS)
        self.quit = False
        global SCORE
        SCORE = 0
        self.background_position = -480

        self.rocket = Rocket()
        self.enemies = [Enemy(x_position=random.uniform(0, SCREEN_RESOLUTION[0])) for _ in range(self.number_of_enemies)]

        self.play_game()

    def play_game(self):
        if not self.quit:
            while self.in_game:
                for event in pygame.event.get():
                    # process actions
                    if event.type == pygame.QUIT:
                        # if quit than quit
                        self.quit = True
                        pygame.quit()

                    if event.type == pygame.KEYDOWN:
                        # check left and right movement
                        if event.key == pygame.K_LEFT:
                            self.rocket.move((True, False))
                        if event.key == pygame.K_RIGHT:
                            self.rocket.move((False, True))

                # independent processes

                #falling enemies
                for enemy in self.enemies:
                    enemy.fall()
                # falling background
                self.background_position += 1
                if self.background_position > 0:
                    self.background_position = -480

                # object interaction check
                for enemy in self.enemies:
                    # detect collision for box and hitbox
                    # x direction
                    x_intersect = False
                    y_intersect = False

                    bstart = enemy.x_position
                    bend = enemy.x_position + ENEMY_SIZE[0]
                    hbstart = self.rocket.hitbox[0]
                    hbend = self.rocket.hitbox[0] + self.rocket.hitbox[2]

                    if hbstart < bstart < hbend or hbstart < bend < hbend:
                        x_intersect = True

                    bstart = enemy.y_position
                    bend = enemy.y_position + ENEMY_SIZE[0]
                    hbstart = self.rocket.hitbox[1]
                    hbend = self.rocket.hitbox[1] + self.rocket.hitbox[3]

                    if hbstart < bstart < hbend or hbstart < bend < hbend:
                        y_intersect = True

                    if x_intersect and y_intersect:
                        print("collision")
                        self.in_game = False

                # draw changes
                self.screen.fill((100, 100, 100))
                self.screen.blit(BACKGROUND_IMAGE, (0, self.background_position))

                for enemy in self.enemies:
                    self.screen.blit(enemy.image, (enemy.x_position, enemy.y_position))
                self.screen.blit(self.rocket.image, (self.rocket.x_position, self.rocket.y_position))
                pygame.draw.rect(
                    self.screen,
                    (0, 0, 255),
                    tuple(self.rocket.hitbox),
                )


                pygame.display.update()  # all the changes are applied here
                self.clock.tick(FPS)
            else:
                return None





        self.menu_or_play()


if __name__ == "__main__":
    game = Game()