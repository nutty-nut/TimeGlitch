import pygame
import random
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TETRIS - Spadające Klocki")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
LIME = (0, 255, 0)
GRAY = (128, 128, 128)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Klocki Tetrisa - kształty i kolory
BLOCK_SIZE = 20  # Rozmiar klocków
SHAPES = [
    # I shape
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    # T shape
    [(0, 0), (1, 0), (2, 0), (1, 1)],
    # L shape
    [(0, 0), (0, 1), (0, 2), (1, 2)],
    # Z shape
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    # O shape
    [(0, 0), (0, 1), (1, 0), (1, 1)]
]

SHAPE_COLORS = [RED, MAGENTA, LIME, (0, 128, 255), (255, 165, 0)]

# Klocki spadające
falling_blocks = []
block_speed = 5

# Funkcja tworzenia nowego klocka
def create_tetris_block():
    shape = random.choice(SHAPES)
    color = random.choice(SHAPE_COLORS)
    # Klocki będą zaczynały w górnej części ekranu w odpowiednich pozycjach (wielokrotności BLOCK_SIZE)
    x_pos = WIDTH // 2 - BLOCK_SIZE * 2  # Środek ekranu, ale dostosowany do klocków
    y_pos = 0
    return {"shape": shape, "color": color, "x": x_pos, "y": y_pos, "stuck": False}

# Funkcja aktualizująca klocki
def update():
    global falling_blocks

    # Zaktualizuj klocki
    for block in falling_blocks:
        if not block["stuck"]:
            # Spadanie klocków
            block["y"] += block_speed

            # Klocki przyklejają się do podłoża
            if block["y"] >= HEIGHT - BLOCK_SIZE * 2:  # Sprawdzamy czy klocek dotknął ziemi
                block["stuck"] = True
                block["y"] = HEIGHT - BLOCK_SIZE * 2  # Ustawiamy klocek na dnie

    # Dodawanie nowych klocków co jakiś czas
    if random.randint(0, 60) == 0:  # Co 60 klatek
        falling_blocks.append(create_tetris_block())

# Funkcja rysująca obiekty
def draw():
    WIN.fill(BLACK)

    # Rysowanie klocków Tetrisa
    for block in falling_blocks:
        block_rects = [pygame.Rect(block["x"] + x * BLOCK_SIZE, block["y"] + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                       for x, y in block["shape"]]
        for rect in block_rects:
            pygame.draw.rect(WIN, block["color"], rect)

    pygame.display.update()

# Główna pętla gry
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        update()
        draw()
        clock.tick(FPS)

main()
