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
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        """
        Reset the game.
        """

        # Setup
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

        # Split the screen into 4 quadrants
        # Calc number of enemies in each quadrant

        nr_enemies_0_0 = 0
        nr_enemies_0_1 = 0
        nr_enemies_1_0 = 0
        nr_enemies_1_1 = 0

        for enemy in self.enemy_list:
            if enemy.x < SCREEN_WIDTH/2 and enemy.y < SCREEN_HEIGHT/2:
                nr_enemies_0_0 += 1
            elif enemy.x < SCREEN_WIDTH/2 and enemy.y >= SCREEN_HEIGHT/2:
                nr_enemies_0_1 += 1
            elif enemy.x >= SCREEN_WIDTH/2 and enemy.y < SCREEN_HEIGHT/2:
                nr_enemies_1_0 += 1
            else:
                nr_enemies_1_1 += 1

        return (
            self.player.x,
            self.player.y,
            
            nr_enemies_0_0,
            nr_enemies_0_1,
            nr_enemies_1_0,
            nr_enemies_1_1,

            self.player_shoot_cooldown == 0,

        ), 0, False

    def step(self, action: tuple[int, int, int, int, int]):
        self.frame_iteration += 1

        # --- Events ---

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # --- End Events ---



        # --- Update ---

        # Player movement
        if action[0] == 1:
            self.player.x -= PLAYER_SPEED

        if action[1] == 1:
            self.player.x += PLAYER_SPEED

        if action[2] == 1:
            self.player.y -= PLAYER_SPEED

        if action[3] == 1:
            self.player.y += PLAYER_SPEED

        # Player shooting
        if action[4] == 1:
            if self.player_shoot_cooldown == 0:
                bullet = pygame.Rect(self.player.x + self.player.width/2 - BULLET_SIZE/2, self.player.y, BULLET_SIZE, BULLET_SIZE)
                self.bullet_list.append(bullet)
                self.player_shoot_cooldown = BULLET_COOLDOWN

        
        # Update bullets
        for bullet in self.bullet_list:
            bullet.y -= BULLETT_SPEED

            if bullet.y < 0:
                self.bullet_list.remove(bullet)

        # Update player shoot cooldown
        if self.player_shoot_cooldown > 0:
            self.player_shoot_cooldown -= 1

        # Split the screen into 4 quadrants
        # Calc number of enemies in each quadrant

        nr_enemies_0_0 = 0
        nr_enemies_0_1 = 0
        nr_enemies_1_0 = 0
        nr_enemies_1_1 = 0

        for enemy in self.enemy_list:
            if enemy.x < SCREEN_WIDTH/2 and enemy.y < SCREEN_HEIGHT/2:
                nr_enemies_0_0 += 1
            elif enemy.x < SCREEN_WIDTH/2 and enemy.y >= SCREEN_HEIGHT/2:
                nr_enemies_0_1 += 1
            elif enemy.x >= SCREEN_WIDTH/2 and enemy.y < SCREEN_HEIGHT/2:
                nr_enemies_1_0 += 1
            else:
                nr_enemies_1_1 += 1

        # Update enemy
        for enemy in self.enemy_list:
            enemy.y += ENEMY_SPEED

            # Enemy collision with player
            if enemy.colliderect(self.player):
                return (
                    self.player.x,
                    self.player.y,
                    
                    nr_enemies_0_0,
                    nr_enemies_0_1,
                    nr_enemies_1_0,
                    nr_enemies_1_1,

                    self.player_shoot_cooldown == 0,

        ), -1, True

            # Enemy collision with bullet
            for bullet in self.bullet_list:
                if enemy.colliderect(bullet):
                    self.enemy_list.remove(enemy)
                    self.bullet_list.remove(bullet)

            # Enemy out of bounds
            if enemy.y > SCREEN_HEIGHT:
                enemy.y = random.randint(-SCREEN_HEIGHT, -ENEMY_SIZE - 50)
                enemy.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)

        # Check if all enemies are destroyed
        if len(self.enemy_list) == 0:
            return (
                self.player.x,
                self.player.y,
                
                nr_enemies_0_0,
                nr_enemies_0_1,
                nr_enemies_1_0,
                nr_enemies_1_1,

                self.player_shoot_cooldown == 0,

        ), 1, True

        # Check if player is out of bounds
        if self.player.x < 0 or self.player.right > SCREEN_WIDTH or self.player.y < 0 or self.player.bottom > SCREEN_HEIGHT:
            return (
                self.player.x,
                self.player.y,
                
                nr_enemies_0_0,
                nr_enemies_0_1,
                nr_enemies_1_0,
                nr_enemies_1_1,

                self.player_shoot_cooldown == 0,

        ), -1, True

        # --- End Update ---



        # --- Draw ---

        # Background
        self.screen.fill(WHITE)

        # Draw player
        pygame.draw.rect(self.screen, PLAYER_COLOR, self.player)

        # Draw bullets
        for bullet in self.bullet_list:
            pygame.draw.rect(self.screen, BULLET_COLOR, bullet)

        # Draw enemies
        for enemy in self.enemy_list:
            pygame.draw.rect(self.screen, ENEMY_COLOR, enemy)

        # Display number of enemies
        font = pygame.font.Font(None, 36)
        text = font.render("Number of enemies: " + str(len(self.enemy_list)), True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, 20))
        self.screen.blit(text, text_rect)

        # Update display
        pygame.display.flip()

        # --- End Draw ---



        # Update clock
        self.clock.tick(FPS)

        return (
            self.player.x,
            self.player.y,
            
            nr_enemies_0_0,
            nr_enemies_0_1,
            nr_enemies_1_0,
            nr_enemies_1_1,

            self.player_shoot_cooldown == 0,

        ), 0, False
        