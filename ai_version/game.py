import pygame
import random

# Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Constants

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAPTION = "Human Version"
FPS = 60

PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_COLOR = RED
PLAYER_START_X = SCREEN_WIDTH/2 - PLAYER_SIZE/2 - 50
PLAYER_START_Y = SCREEN_HEIGHT - PLAYER_SIZE

BULLET_SIZE = 10
BULLETT_SPEED = 10
BULLET_COLOR = BLUE
BULLET_COOLDOWN = 30

ENEMY_SIZE = 25
ENEMY_SPEED = 2
ENEMY_COLOR = BLACK

NUMBER_OF_ENEMIES = 20

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()
    running = True

    # Setup
    game_over = False

    player = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, PLAYER_SIZE, PLAYER_SIZE)  # x, y, width, height

    bullet_list = []
    bullet_cooldown = 0

    enemy_list = []

    for _ in range(NUMBER_OF_ENEMIES):
        enemy = pygame.Rect(random.randint(0, SCREEN_WIDTH - ENEMY_SIZE), random.randint(-SCREEN_HEIGHT, -ENEMY_SIZE - 50), ENEMY_SIZE, ENEMY_SIZE)
        enemy_list.append(enemy)

    # Main loop

    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False     

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:    
            player.y += PLAYER_SPEED
        if keys[pygame.K_SPACE]:

            if bullet_cooldown == 0:
                bullet = pygame.Rect(player.x + player.width/2 - BULLET_SIZE/2, player.y, BULLET_SIZE, BULLET_SIZE)
                bullet_list.append(bullet)

                bullet_cooldown = BULLET_COOLDOWN

        if keys[pygame.K_r]:
            player.x = PLAYER_START_X
            player.y = PLAYER_START_Y
            game_over = False
            bullet_list = []
            enemy_list = []

            for _ in range(NUMBER_OF_ENEMIES):
                enemy = pygame.Rect(random.randint(0, SCREEN_WIDTH - ENEMY_SIZE), random.randint(-SCREEN_HEIGHT, -ENEMY_SIZE - 50), ENEMY_SIZE, ENEMY_SIZE)
                enemy_list.append(enemy)

        # Update

        if game_over:
            continue

        # --- Game logic ---

        if player.x < 0 or player.right > SCREEN_WIDTH or player.y < 0 or player.bottom > SCREEN_HEIGHT:
            game_over = True

        for bullet in bullet_list:
            bullet.y -= BULLETT_SPEED

            if bullet.y < 0:
                bullet_list.remove(bullet)

        if bullet_cooldown > 0:
            bullet_cooldown -= 1

        for enemy in enemy_list:
            enemy.y += ENEMY_SPEED

            if enemy.colliderect(player):
                game_over = True

            for bullet in bullet_list:
                if enemy.colliderect(bullet):
                    enemy_list.remove(enemy)
                    bullet_list.remove(bullet)

            if enemy.y > SCREEN_HEIGHT:
                enemy.y = random.randint(-SCREEN_HEIGHT, -ENEMY_SIZE - 50)
                enemy.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)

        if len(enemy_list) == 0:
            game_over = True
                    

        # --- End Game logic ---

        # ---

        # Draw
        
        screen.fill(WHITE)

        # --- Draw here ---

        if game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(text, text_rect)

        pygame.draw.rect(screen, PLAYER_COLOR, player)

        for bullet in bullet_list:
            pygame.draw.rect(screen, BULLET_COLOR, bullet)

        for enemy in enemy_list:
            pygame.draw.rect(screen, ENEMY_COLOR, enemy)

        font = pygame.font.Font(None, 36)
        text = font.render("Number of enemies: " + str(len(enemy_list)), True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, 20))
        screen.blit(text, text_rect)

        # --- End Draw ---

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()