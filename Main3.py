import pygame
import random

pygame.init()

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

# Czcionka
font = pygame.font.SysFont(None, 36)

# Postacie
ludzik = pygame.Rect(100, 300, 20, 20)
ludzik_speed = 5

# Tryb gry
in_arena = False
score = 0

# Drzwi wejściowe na arenę
door = pygame.Rect(WIDTH - 40, HEIGHT // 2 - 40, 30, 80)

# Snake
snake = []
snake_speed = 2
snake_length = 20

# Warzywa i pociski
veggies = [pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 15, 15) for _ in range(5)]
bullets = []

clock = pygame.time.Clock()

# Funkcja bezpiecznej odległości
def safe_div(a, b):
    return a / b if b != 0 else 0

def distance(a, b):
    return max(abs(a.x - b.x), abs(a.y - b.y))

def spawn_snake():
    global snake
    start_x = random.randint(100, WIDTH - 100)
    start_y = random.randint(100, HEIGHT - 100)
    snake = [pygame.Rect(start_x, start_y, 20, 20) for _ in range(snake_length)]

# Główna pętla gry
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Poruszanie się ludzikiem
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ludzik.x > 0: ludzik.x -= ludzik_speed
    if keys[pygame.K_RIGHT] and ludzik.x < WIDTH - ludzik.width: ludzik.x += ludzik_speed
    if keys[pygame.K_UP] and ludzik.y > 0: ludzik.y -= ludzik_speed
    if keys[pygame.K_DOWN] and ludzik.y < HEIGHT - ludzik.height: ludzik.y += ludzik_speed

    if not in_arena:
        # Przejście przez drzwi
        if ludzik.colliderect(door):
            in_arena = True
            ludzik.x, ludzik.y = WIDTH // 2, HEIGHT // 2
            spawn_snake()
            veggies = [pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 15, 15) for _ in range(5)]
    else:
        # Zbieranie warzyw
        for veggie in veggies[:]:
            if ludzik.colliderect(veggie):
                veggies.remove(veggie)
                bullets.append(pygame.Rect(ludzik.x, ludzik.y, 8, 8))
                veggies.append(pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 15, 15))
                score += 1

        # Warzywa gonią węża
        for veggie in veggies:
            dx = snake[0].x - veggie.x
            dy = snake[0].y - veggie.y
            dist = distance(veggie, snake[0])
            veggie.x += int(2 * safe_div(dx, dist))
            veggie.y += int(2 * safe_div(dy, dist))

        # Wąż goni ludzika
        dx = ludzik.x - snake[0].x
        dy = ludzik.y - snake[0].y
        dist = distance(snake[0], ludzik)
        dir_x = safe_div(dx, dist)
        dir_y = safe_div(dy, dist)
        new_head = snake[0].copy()
        new_head.x += int(snake_speed * dir_x)
        new_head.y += int(snake_speed * dir_y)
        snake.insert(0, new_head)
        if len(snake) > snake_length:
            snake.pop()

        # Pociski lecą do węża
        for bullet in bullets[:]:
            dx = snake[0].x - bullet.x
            dy = snake[0].y - bullet.y
            dist = distance(bullet, snake[0])
            bullet.x += int(6 * safe_div(dx, dist))
            bullet.y += int(6 * safe_div(dy, dist))
            if bullet.colliderect(snake[0]):
                bullets.remove(bullet)
                if snake_length > 3:
                    snake_length -= 1

        # Koniec gry, gdy wąż złapie ludzika
        if ludzik.colliderect(snake[0]):
            print("Game Over!")
            running = False

    # Rysowanie
    screen.fill(BLUE if not in_arena else BLACK)

    if not in_arena:
        pygame.draw.rect(screen, YELLOW, ludzik)
        pygame.draw.rect(screen, WHITE, door)
        text = font.render("Wejście do Areny", True, BLACK)
        screen.blit(text, (door.x - 30, door.y - 30))
    else:
        pygame.draw.rect(screen, YELLOW, ludzik)
        for s in snake:
            pygame.draw.rect(screen, GREEN, s)
        for veggie in veggies:
            pygame.draw.rect(screen, RED, veggie)
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Wyświetlanie punktów
        score_text = font.render(f"Punkty: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
