import pygame
import random

pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Obby Game")
clock = pygame.time.Clock()  # Limits frame rate so game doesn't run too fast

# Game state variable
game_state = 1

# Player setup
player_idle = pygame.surface.Surface((100, 100))  # Placeholder if image fails to load
player_idle.fill((255, 255, 255))
try:
    player_idle = pygame.image.load("imgs/walking.png").convert_alpha()
    player_idle = pygame.transform.scale(player_idle, (100, 100))
except pygame.error:
    print("Warning: 'imgs/walking.png' not found. Using white square fallback.")

player_x = 350
player_y = 450
player_vel_x = 0
player_vel_y = 0

# Falling object setup
falling_object = pygame.surface.Surface((50, 50))
falling_object.fill((255, 0, 0))  # Changed to red for visibility
falling_object_x = random.randint(0, 750)
falling_object_y = 0
falling_object_vel_x = 0
falling_object_vel_y = 5  # Increased speed (0.3 is too slow for 60FPS)

# Font setup for game over text
font = pygame.font.SysFont("Arial", 50)
game_over_text = font.render("GAME OVER", True, (255, 0, 0))

def collision_detection():
    # Pygame Surfaces use .get_width() and .get_height() instead of .width / .height attributes
    return (player_x <= (falling_object_x + falling_object.get_width()) and 
            (player_x + player_idle.get_width()) >= falling_object_x and 
            player_y <= (falling_object_y + falling_object.get_height()) and 
            (player_y + player_idle.get_height()) >= falling_object_y)

running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                player_vel_x = -5
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                player_vel_x = 5
            elif event.key in (pygame.K_UP, pygame.K_w):
                player_vel_y = -5
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                player_vel_y = 5
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a) and player_vel_x < 0:
                player_vel_x = 0
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and player_vel_x > 0:
                player_vel_x = 0
            elif event.key in (pygame.K_UP, pygame.K_w) and player_vel_y < 0:
                player_vel_y = 0
            elif event.key in (pygame.K_DOWN, pygame.K_s) and player_vel_y > 0:
                player_vel_y = 0

    # 2. Game Logic Updates
    if game_state == 1:
        # Move Player
        player_x += player_vel_x
        player_y += player_vel_y

        # Move Falling Object
        falling_object_y += falling_object_vel_y
        falling_object_x += falling_object_vel_x

        # Reset object if it goes off screen
        if falling_object_y >= 600:
            falling_object_y = -50
            falling_object_x = random.randint(0, window.get_width() - 50)

        # Check collision to trigger Game Over
        if collision_detection():
            game_state = 2

    # 3. Drawing / Rendering
    window.fill((0, 0, 0))  # Clear screen with black every frame

    if game_state == 1:
        window.blit(player_idle, (player_x, player_y))
        window.blit(falling_object, (falling_object_x, falling_object_y))
    elif game_state == 2:
        window.blit(game_over_text, (280, 250))

    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second

pygame.quit()
