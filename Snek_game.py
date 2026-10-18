import pygame
import random
import time

pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Endless Obby")
clock = pygame.time.Clock()

try:
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except FileNotFoundError:
    print("No music.mp3 found, playing without music")
except pygame.error:
    print("Music could not be played, playing without music")

death_sound = None
try:
    death_sound = pygame.mixer.Sound("death.mp3")
except FileNotFoundError:
    print("No death.mp3 found, dying will be silent")
except pygame.error:
    print("Death sound could not be loaded")

font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 60)

idle_img = pygame.image.load("imgs/Idle.png").convert_alpha()
idle_img = pygame.transform.scale(idle_img, (64, 64))
walking_img = pygame.image.load("imgs/walking.png").convert_alpha()
walking_img = pygame.transform.scale(walking_img, (64, 64))
jumping1_img = pygame.image.load("imgs/Jumping 1.png").convert_alpha()
jumping1_img = pygame.transform.scale(jumping1_img, (64, 64))
jumping2_img = pygame.image.load("imgs/Jumping 2.png").convert_alpha()
jumping2_img = pygame.transform.scale(jumping2_img, (64, 64))

ground_y = 500
player_size = 64
player_screen_x = 300
jump_height = 140
jump_speed = 8
move_speed = 5
fast_speed = 8
shift_held = False


class Obstacle:
    def __init__(self, kind, x, width):
        self.kind = kind
        self.x = x
        self.width = width

    def draw(self, camera_x):
        screen_x = self.x - camera_x
        if self.kind == "lava":
            pygame.draw.rect(window, (255, 90, 0), (screen_x, ground_y, self.width, 100))
            pygame.draw.rect(window, (255, 200, 40), (screen_x, ground_y, self.width, 12))
        else:
            for i in range(self.width // 40):
                spike_x = screen_x + i * 40
                pygame.draw.polygon(window, (200, 200, 210), [(spike_x, ground_y), (spike_x + 20, ground_y - 40), (spike_x + 40, ground_y)])

    def hits(self, hitbox):
        if self.kind == "lava":
            return False
        spike_box = pygame.Rect(self.x + 6, ground_y - 36, self.width - 12, 36)
        return hitbox.colliderect(spike_box)


def make_hitbox(x, y):
    return pygame.Rect(x + 16, y + 14, 32, 50)


game_state = 1
player_x = 300
player_y = ground_y - player_size
camera_x = 0
vel_x = 0
jump_state = 0
hold_start = 0
start_x = player_x

obstacles = []
next_obstacle_x = 800

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                shift_held = True
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w) and game_state == 1 and jump_state == 0:
                jump_state = 1
            if event.key == pygame.K_r and game_state == 2:
                game_state = 1
                player_x = 300
                player_y = ground_y - player_size
                camera_x = 0
                vel_x = 0
                jump_state = 0
                obstacles = []
                next_obstacle_x = 800
                start_x = player_x
                try:
                    pygame.mixer.music.play(-1)
                except pygame.error:
                    print("No music to restart")
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                shift_held = False

    if game_state == 1:
        vel_x = move_speed
        if shift_held:
            vel_x = fast_speed
        player_x += vel_x
        camera_x = player_x - player_screen_x

        if jump_state == 1:
            player_y -= jump_speed
            if player_y <= ground_y - player_size - jump_height:
                player_y = ground_y - player_size - jump_height
                jump_state = 2
                hold_start = time.time()
        elif jump_state == 2:
            if time.time() - hold_start >= 0.09:
                jump_state = 3
        elif jump_state == 3:
            player_y += jump_speed
            if player_y >= ground_y - player_size:
                player_y = ground_y - player_size
                jump_state = 0

        while next_obstacle_x < camera_x + 1500:
            kind = random.choice(["spike", "lava", "spike"])
            if kind == "lava":
                width = random.randint(90, 150)
            else:
                width = 40 * random.randint(1, 3)
            obstacles.append(Obstacle(kind, next_obstacle_x, width))
            next_obstacle_x += width + random.randint(260, 460)

        kept = []
        for obstacle in obstacles:
            if obstacle.x + obstacle.width > camera_x - 100:
                kept.append(obstacle)
        obstacles = kept

        world_hitbox = make_hitbox(player_x, player_y)
        for obstacle in obstacles:
            if obstacle.hits(world_hitbox):
                game_state = 2
            if obstacle.kind == "lava" and jump_state == 0:
                center = player_x + player_size / 2
                if obstacle.x + 8 < center < obstacle.x + obstacle.width - 8:
                    game_state = 2

        if game_state == 2:
            pygame.mixer.music.stop()
            if death_sound is not None:
                death_sound.set_volume(1.0)
                death_sound.play()

    score = int((player_x - start_x) / 10)

    window.fill((55, 50, 75))
    for i in range(-1, 14):
        brick_x = i * 100 - int(camera_x * 0.5) % 100
        pygame.draw.line(window, (70, 64, 95), (brick_x, 100), (brick_x, ground_y), 2)
    for i in range(1, 8):
        pygame.draw.line(window, (70, 64, 95), (0, 100 + i * 50), (800, 100 + i * 50), 2)
    pygame.draw.rect(window, (30, 28, 42), (0, 0, 800, 100))
    pygame.draw.rect(window, (90, 84, 120), (0, 92, 800, 8))
    pygame.draw.rect(window, (90, 84, 120), (0, ground_y, 800, 100))
    pygame.draw.rect(window, (140, 134, 170), (0, ground_y, 800, 10))

    for obstacle in obstacles:
        obstacle.draw(camera_x)

    if jump_state == 1 or jump_state == 3:
        current_img = jumping1_img
    elif jump_state == 2:
        current_img = jumping2_img
    elif vel_x != 0:
        current_img = walking_img
    else:
        current_img = idle_img

    window.blit(current_img, (player_x - camera_x, player_y))

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (30, 30))
    pygame.draw.rect(window, (30, 28, 42), (0, 100, 16, 400))
    pygame.draw.rect(window, (30, 28, 42), (784, 100, 16, 400))

    if game_state == 2:
        game_over_text = big_font.render("GAME OVER", True, (255, 70, 70))
        restart_text = font.render("Press R to restart", True, (255, 255, 255))
        window.blit(game_over_text, (250, 230))
        window.blit(restart_text, (300, 310))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
