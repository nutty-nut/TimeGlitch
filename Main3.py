import pygame
import random
import math
import os

pygame.init()

# Wczytaj animowane obrazy myszy
mouse_img_1 = pygame.transform.scale(pygame.image.load(os.path.join("Graphics", "mysz_1.png")), (20, 20))
mouse_img_2 = pygame.transform.scale(pygame.image.load(os.path.join("Graphics", "mysz_2.png")), (20, 20))
mouse_anim_timer = 0

# Muzyka
try:
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)
except:
    print("Nie można załadować pliku muzycznego")

# Ekran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reverse Snake - Ludzik vs Wąż")

# Kolory
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGIC = (255, 0, 255)

# Czcionka
font = pygame.font.SysFont(None, 36)

# Postacie
ludzik = pygame.Rect(100, 300, 20, 20)
ludzik_speed = 5

# Tryb gry
in_arena = False
score = 0
snake_lives = 10
magic_item = None
portal = None

# Glitch efekty
glitch_frames = [(random.randint(-5, 5), random.randint(-5, 5)) for _ in range(10)]

# Drzwi wejściowe
door = pygame.Rect(WIDTH - 40, HEIGHT // 2 - 40, 30, 80)

# Snake
snake = []
snake_speed = 2
snake_length = 10

# Obiekty
veggies = [pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 15, 15) for _ in range(5)]
bullets = []
food_items = [pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 15, 15) for _ in range(4)]
food_velocities = [(random.choice([-1, 1]) * random.randint(1, 2), random.choice([-1, 1]) * random.randint(1, 2)) for _ in food_items]

clock = pygame.time.Clock()
glitch_timer = 0

# Funkcje
def safe_div(a, b):
    return a / b if b != 0 else 0

def distance(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

def spawn_snake():
    global snake, snake_length, snake_lives
    snake_length = 10
    snake_lives = snake_length
    start_x = random.randint(100, WIDTH - 100)
    start_y = random.randint(100, HEIGHT - 100)
    snake.clear()
    for i in range(snake_length):
        snake.append(pygame.Rect(start_x - i * 20, start_y, 20, 20))

# Główna pętla gry
running = True
while running:
    clock.tick(60)
    glitch_timer += 1
    mouse_anim_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ludzik.x > 0: ludzik.x -= ludzik_speed
    if keys[pygame.K_RIGHT] and ludzik.x < WIDTH - ludzik.width: ludzik.x += ludzik_speed
    if keys[pygame.K_UP] and ludzik.y > 0: ludzik.y -= ludzik_speed
    if keys[pygame.K_DOWN] and ludzik.y < HEIGHT - ludzik.height: ludzik.y += ludzik_speed

    if not in_arena:
        if ludzik.colliderect(door):
            in_arena = True
            ludzik.x, ludzik.y = WIDTH // 2, HEIGHT // 2
            spawn_snake()
            magic_item = None
            portal = None
            veggies = [pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 15, 15) for _ in range(5)]
            food_items = [pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 15, 15) for _ in range(4)]
            food_velocities = [(random.choice([-1, 1]) * random.randint(1, 2), random.choice([-1, 1]) * random.randint(1, 2)) for _ in food_items]
    else:
        for veggie in veggies[:]:
            if ludzik.colliderect(veggie):
                veggies.remove(veggie)
                bullets.append(pygame.Rect(ludzik.x, ludzik.y, 8, 8))
                veggies.append(pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 15, 15))
                score += 1

        if snake:
            target = ludzik
            min_dist = distance(snake[0], ludzik)
            for food in food_items:
                d = distance(snake[0], food)
                if d < min_dist and d < 150:
                    target = food
                    min_dist = d

            dx = target.x - snake[0].x
            dy = target.y - snake[0].y
            dist = distance(snake[0], target)
            dir_x = safe_div(dx, dist)
            dir_y = safe_div(dy, dist)
            new_head = snake[0].copy()
            new_head.x += int(snake_speed * dir_x)
            new_head.y += int(snake_speed * dir_y)
            snake.insert(0, new_head)
            if len(snake) > snake_length:
                snake.pop()

            for bullet in bullets[:]:
                if not snake:
                    continue
                dx = snake[0].x - bullet.x
                dy = snake[0].y - bullet.y
                dist = distance(bullet, snake[0])
                bullet.x += int(6 * safe_div(dx, dist))
                bullet.y += int(6 * safe_div(dy, dist))
                if snake and bullet.colliderect(snake[0]):
                    bullets.remove(bullet)
                    snake_lives -= 1
                    if snake_lives <= 0:
                        magic_item = pygame.Rect(snake[0].x, snake[0].y, 15, 15)
                        snake.clear()
                    else:
                        snake_length = max(1, snake_length - 1)
                        if len(snake) > snake_length:
                            snake.pop()

        for i, food in enumerate(food_items):
            food.x += food_velocities[i][0]
            food.y += food_velocities[i][1]
            if food.left <= 0 or food.right >= WIDTH:
                food_velocities[i] = (-food_velocities[i][0], food_velocities[i][1])
            if food.top <= 0 or food.bottom >= HEIGHT:
                food_velocities[i] = (food_velocities[i][0], -food_velocities[i][1])
            if snake and snake[0].colliderect(food):
                food_items[i] = pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 15, 15)
                food_velocities[i] = (random.choice([-1, 1]) * random.randint(1, 2), random.choice([-1, 1]) * random.randint(1, 2))
                grow_amount = 3
                snake_length += grow_amount
                snake_lives += grow_amount
                tail = snake[-1].copy()
                for _ in range(grow_amount):
                    snake.append(tail.copy())

        if snake and ludzik.colliderect(snake[0]):
            ludzik.x, ludzik.y = 100, 300
            in_arena = False

        if magic_item and ludzik.colliderect(magic_item):
            magic_item = None
            portal = pygame.Rect(10, HEIGHT // 2 - 40, 30, 80)
            ludzik.x, ludzik.y = 100, 300
            in_arena = False

    screen.fill(BLUE if not in_arena else BLACK)

    if not in_arena:
        pygame.draw.rect(screen, YELLOW, ludzik)
        pygame.draw.rect(screen, WHITE, door)
        if portal:
            pygame.draw.rect(screen, WHITE, portal)
        text = font.render("Wejście do Areny", True, BLACK)
        screen.blit(text, (door.x - 30, door.y - 30))
    else:
        offset_x, offset_y = glitch_frames[glitch_timer % len(glitch_frames)] if glitch_timer % 10 < 3 else (0, 0)

        if glitch_timer % 20 < 5:
            screen.fill((random.randint(0, 30), random.randint(0, 30), random.randint(0, 30)))

        pygame.draw.rect(screen, YELLOW, ludzik.move(offset_x, offset_y))
        for s in snake:
            pygame.draw.rect(screen, GREEN, s.move(offset_x, offset_y))
        for veggie in veggies:
            pygame.draw.rect(screen, RED, veggie.move(offset_x, offset_y))
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet.move(offset_x, offset_y))
        for food in food_items:
            mouse_frame = mouse_img_1 if (mouse_anim_timer // 10) % 2 == 0 else mouse_img_2
            screen.blit(mouse_frame, food.move(offset_x, offset_y))
        if magic_item:
            pygame.draw.rect(screen, MAGIC, magic_item.move(offset_x, offset_y))
        if glitch_timer % 15 < 3:
            pygame.draw.rect(screen, CYAN, pygame.Rect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 50, 10))

        score_text = font.render(f"Punkty: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
