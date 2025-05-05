import pygame
import random
import math
import os

pygame.init()

mouse_img_1 = pygame.transform.scale(pygame.image.load(os.path.join("Graphics", "mysz_1.png")), (20, 20))
mouse_img_2 = pygame.transform.scale(pygame.image.load(os.path.join("Graphics", "mysz_2.png")), (20, 20))
mouse_anim_timer = 0

try:
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)
except:
    print("Nie można załadować pliku muzycznego")

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reverse Snake - Ludzik vs Wąż")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGIC = (255, 0, 255)

font = pygame.font.SysFont(None, 36)

ludzik = pygame.Rect(100, 300, 20, 20)
ludzik_speed = 5

last_direction = [0, 0]
bullet_ready = 0

in_arena = False
score = 0
snake_lives = 10
magic_item = None
portal = pygame.Rect(WIDTH - 40, HEIGHT // 2 - 40, 30, 80)
exit_door = None
has_magic_item = False
mini_game_unlocked = False

snake = []
snake_speed = 2
snake_length = 10
snake_memory_timer = 0
player_last_seen = None

obstacle_img = pygame.transform.scale(pygame.image.load(os.path.join("Graphics", "block.png")), (40, 40))
obstacles = []
veggies = []
bullets = []
food_items = []
food_velocities = []

clock = pygame.time.Clock()
glitch_timer = 0
glitch_frames = [(random.randint(-5, 5), random.randint(-5, 5)) for _ in range(10)]

def safe_div(a, b):
    return a / b if b != 0 else 0

def distance(a, b):
    return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5

def clamp_rect(rect, width, height):
    rect.x = max(0, min(rect.x, width - rect.width))
    rect.y = max(0, min(rect.y, height - rect.height))
    return rect

def spawn_snake():
    global snake, snake_length, snake_lives
    snake_length = 10
    snake_lives = snake_length
    snake.clear()
    x, y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
    for i in range(snake_length):
        snake.append(pygame.Rect(x - i * 20, y, 20, 20))

def spawn_arena():
    global obstacles, veggies, food_items, food_velocities
    obstacles = [pygame.Rect(random.randint(100, WIDTH - 140), random.randint(100, HEIGHT - 140), 40, 40) for _ in range(6)]
    veggies = [pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 15, 15) for _ in range(5)]
    food_items = [pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 20, 20) for _ in range(4)]
    food_velocities.clear()
    for _ in food_items:
        vx = random.choice([-1, 1]) * random.randint(1, 2)
        vy = random.choice([-1, 1]) * random.randint(1, 2)
        food_velocities.append([vx, vy])

running = True
while running:
    clock.tick(60)
    glitch_timer += 1
    mouse_anim_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and bullet_ready > 0:
                bullet = pygame.Rect(ludzik.centerx, ludzik.centery, 8, 8)
                bullets.append((bullet, last_direction[:]))
                bullet_ready -= 1

    keys = pygame.key.get_pressed()
    for dx, dy, key in [(-ludzik_speed, 0, keys[pygame.K_LEFT]), (ludzik_speed, 0, keys[pygame.K_RIGHT]), (0, -ludzik_speed, keys[pygame.K_UP]), (0, ludzik_speed, keys[pygame.K_DOWN])]:
        if key:
            last_direction = [dx // ludzik_speed, dy // ludzik_speed]
            next_pos = ludzik.move(dx, dy)
            if not any(next_pos.colliderect(o) for o in obstacles):
                ludzik = clamp_rect(next_pos, WIDTH, HEIGHT)

    if not in_arena and ludzik.colliderect(portal):
        in_arena = True
        ludzik.x, ludzik.y = WIDTH // 2, HEIGHT // 2
        spawn_snake()
        spawn_arena()
        magic_item = None
        exit_door = None
        has_magic_item = False
        bullet_ready = 0

    if in_arena:
        for veggie in veggies[:]:
            if ludzik.colliderect(veggie):
                veggies.remove(veggie)
                bullet_ready += 1
                veggies.append(pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 15, 15))
                score += 1

        if snake and snake[0].colliderect(ludzik):
            in_arena = False
            ludzik.x, ludzik.y = 100, 300

        if snake:
            targets = [ludzik] + food_items
            closest = min(targets, key=lambda t: distance(snake[0], t))
            dx = closest.x - snake[0].x
            dy = closest.y - snake[0].y
            dist = distance(snake[0], closest)
            dir_x = safe_div(dx, dist)
            dir_y = safe_div(dy, dist)
            new_head = snake[0].move(int(snake_speed * dir_x), int(snake_speed * dir_y))
            if not any(new_head.colliderect(o) for o in obstacles):
                snake.insert(0, clamp_rect(new_head, WIDTH, HEIGHT))
            else:
                for dir_try in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    try_head = snake[0].move(dir_try[0]*snake_speed, dir_try[1]*snake_speed)
                    if not any(try_head.colliderect(o) for o in obstacles):
                        snake.insert(0, clamp_rect(try_head, WIDTH, HEIGHT))
                        break
                else:
                    snake.insert(0, snake[0].copy())
            if len(snake) > snake_length:
                snake.pop()

        for i in range(len(bullets)):
            bullet, direction = bullets[i]
            bullet.x += direction[0] * 6
            bullet.y += direction[1] * 6

        for bullet, _ in bullets[:]:
            if not snake:
                continue
            if bullet.colliderect(snake[0]):
                bullets.remove((bullet, _))
                snake_lives -= 1
                if snake_lives <= 0:
                    magic_item = pygame.Rect(snake[0].x, snake[0].y, 15, 15)
                    exit_door = pygame.Rect(WIDTH // 2 - 15, 50, 30, 60)
                    snake.clear()
                else:
                    snake_length = max(1, snake_length - 2)
                    if len(snake) > snake_length:
                        snake.pop()

        for i in range(len(food_items)):
            food_items[i] = food_items[i].move(food_velocities[i][0], food_velocities[i][1])
            if food_items[i].left <= 0 or food_items[i].right >= WIDTH:
                food_velocities[i][0] *= -1
            if food_items[i].top <= 0 or food_items[i].bottom >= HEIGHT:
                food_velocities[i][1] *= -1
            if snake and snake[0].colliderect(food_items[i]):
                food_items[i] = pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 20, 20)
                food_velocities[i] = [random.choice([-1,1])*random.randint(1,2), random.choice([-1,1])*random.randint(1,2)]
                snake_length += 3
                tail = snake[-1].copy()
                for _ in range(3):
                    snake.append(tail.copy())

        if magic_item and ludzik.colliderect(magic_item):
            has_magic_item = True
            magic_item = None

        if has_magic_item and exit_door and ludzik.colliderect(exit_door):
            mini_game_unlocked = True
            in_arena = False
            ludzik.x, ludzik.y = 100, 300

    screen.fill(BLUE if not in_arena else BLACK)
    if in_arena:
        for o in obstacles:
            screen.blit(obstacle_img, o)

    if not in_arena:
        pygame.draw.rect(screen, YELLOW, ludzik)
        pygame.draw.rect(screen, WHITE, portal)
        if exit_door:
            pygame.draw.rect(screen, CYAN, exit_door)
        if mini_game_unlocked:
            screen.blit(font.render("Mini-gra odblokowana!", True, BLACK), (WIDTH//2 - 120, HEIGHT//2))
        else:
            screen.blit(font.render("Wejście do Areny", True, BLACK), (portal.x - 30, portal.y - 30))
    else:
        offset_x, offset_y = glitch_frames[glitch_timer % len(glitch_frames)] if glitch_timer % 10 < 3 else (0, 0)
        if glitch_timer % 20 < 5:
            screen.fill((random.randint(0,30), random.randint(0,30), random.randint(0,30)))

        pygame.draw.rect(screen, YELLOW, ludzik.move(offset_x, offset_y))
        for s in snake:
            pygame.draw.rect(screen, GREEN, s.move(offset_x, offset_y))
        for veggie in veggies:
            pygame.draw.rect(screen, RED, veggie.move(offset_x, offset_y))
        for bullet, _ in bullets:
            pygame.draw.rect(screen, WHITE, bullet.move(offset_x, offset_y))
        for food in food_items:
            mouse_img = mouse_img_1 if (mouse_anim_timer // 10) % 2 == 0 else mouse_img_2
            screen.blit(mouse_img, food.move(offset_x, offset_y))
        if magic_item:
            pygame.draw.rect(screen, MAGIC, magic_item.move(offset_x, offset_y))
        if exit_door:
            pygame.draw.rect(screen, CYAN, exit_door)
        screen.blit(font.render(f"Punkty: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Amunicja: {bullet_ready}", True, WHITE), (10, 40))
        screen.blit(font.render(f"Życia węża: {snake_lives}", True, WHITE), (10, 70))

    pygame.display.flip()

pygame.quit()
