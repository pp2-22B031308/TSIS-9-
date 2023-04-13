import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0
COINS_FOR_SPEED_UP = 5
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("road.png")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("car2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self, enemy_pos):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        while self.rect.collidelist(enemy_pos) != -1:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        weights = [1, 2, 3, 4]
        probabilities = [0.4, 0.3, 0.2, 0.1]
        self.weight = random.choices(weights, probabilities)[0]

    def move(self):
        global COINS_COLLECTED
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

            weights = [1, 2, 3, 4]
            probabilities = [0.4, 0.3, 0.2, 0.1]
            self.weight = random.choices(weights, probabilities)[0]
        elif pygame.sprite.spritecollideany(self, players):
            COINS_COLLECTED += self.weight
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            weights = [1, 2, 3, 4]
            probabilities = [0.4, 0.3, 0.2, 0.1]
            self.weight = random.choices(weights, probabilities)[0]



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("car.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


P1 = Player()
E1 = Enemy()
C1 = Coin([E1.rect])

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
players = pygame.sprite.Group()
players.add(P1)

INC_SPEED = pygame.USEREVENT + 1

pygame.time.set_timer(INC_SPEED, 1000)


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    if COINS_COLLECTED >= COINS_FOR_SPEED_UP:
        COINS_FOR_SPEED_UP += 5
        SPEED += 1

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    coins_collected_text = font_small.render("Coins Collected: " + str(COINS_COLLECTED), True, BLACK)
    coins_collected_rect = coins_collected_text.get_rect()
    coins_collected_rect.topright = (SCREEN_WIDTH - 10, 10)
    DISPLAYSURF.blit(coins_collected_text, coins_collected_rect)

    pygame.display.update()
    FramePerSec.tick(FPS)