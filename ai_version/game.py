import pygame
import random

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CAPTION = "Human Version"

GAME_FONT = pygame.font.Font(None, 36)
FPS = 60

# Player dimensions
PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_COLOR = RED
PLAYER_START_X = SCREEN_WIDTH/2 - PLAYER_SIZE/2 - 50
PLAYER_START_Y = SCREEN_HEIGHT - PLAYER_SIZE

# Bullet dimensions
BULLET_SIZE = 10
BULLETT_SPEED = 10
BULLET_COLOR = BLUE
BULLET_COOLDOWN = 30

# Enemy dimensions
ENEMY_SIZE = 50
ENEMY_COLOR = BLACK
ENEMY_SPEED = 5

NUMBER_OF_ENEMIES = 20

class Game(object):

    def __init__(self):
        """
        Initialize the game.
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        """
        Reset the game.
        """

        # Setup
        self.game_over = False
        self.frame_iteration = 0
        
        # Player
        self.player = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, PLAYER_SIZE, PLAYER_SIZE)
        self.player_shoot_cooldown = 0

        # Bullets
        self.bullet_list = []

        # Enemies
        self.enemy_list = []

        for _ in range(NUMBER_OF_ENEMIES):
            enemy = pygame.Rect(random.randint(0, SCREEN_WIDTH - ENEMY_SIZE), random.randint(-SCREEN_HEIGHT, -ENEMY_SIZE - 50), ENEMY_SIZE, ENEMY_SIZE)
            self.enemy_list.append(enemy)

    def step(self, action):
        pass