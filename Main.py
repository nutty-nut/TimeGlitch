import pygame
import random
import sys

pygame.init()

# --- Ustawienia okna ---
WIDTH, HEIGHT = 800, 600
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time Glitch: Pixel Paradox")

# --- Sprite gracza (poziom 2) ---
player_sprite = None
use_sprite = False
try:
    player_sprite = pygame.image.load("player_8bit.png").convert_alpha()
    player_sprite = pygame.transform.scale(player_sprite, (40, 40))
except:
    print("Brak pliku 'player_8bit.png', gracz będzie kwadratem.")


# --- Nowe elementy: Monety ---
coins = [pygame.Rect(random.randint(50, 750), random.randint(100, 500), 20, 20) for _ in range(5)]
coin_color = (255, 215, 0)
coins_collected = 0

level = 1

# --- Nowe platformy poziom 1 ---
platforms_level1 = [
    pygame.Rect(0, 550, 200, 30),
    pygame.Rect(250, 480, 150, 30),
    pygame.Rect(450, 400, 200, 30),
    pygame.Rect(700, 320, 100, 30),
    pygame.Rect(100, 240, 150, 30)
]

platforms_level2 = [
    pygame.Rect(0, 550, 300, 30),
    pygame.Rect(350, 450, 300, 30),
    pygame.Rect(200, 350, 200, 30),
    pygame.Rect(600, 300, 150, 30)
]

bg_level2 = None

try:
    bg_level2 = pygame.image.load("bg_level2.png").convert()
    bg_level2 = pygame.transform.scale(bg_level2, (WIDTH, HEIGHT))
except:
    print("Brak pliku 'bg_level2.png', używane będzie domyślne tło.")



# --- Palety kolorów ---
PALETTES = {
    "8bit": [(0, 0, 0), (255, 255, 255), (255, 0, 0)],
    "16bit": [(34, 32, 52), (69, 40, 60), (102, 57, 49)],
    "GB": [(15, 56, 15), (48, 98, 48), (139, 172, 15)],
}
current_palette = "8bit"

# --- Gracz i platformy ---
player = pygame.Rect(100, 500, 40, 40)
player_velocity_y = 0
gravity = 1
on_ground = True
platforms = [pygame.Rect(0, 550, 800, 50)]

# --- Glitch efekt i boss ---
glitch_timer = 0
glitching = False
boss = None
boss_direction = -1

# --- Licznik epok ---
epochs_survived = 0

# --- Muzyka ---
try:
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)
except:
    print("Brak pliku muzycznego 'music.wav'")

# --- Czcionka ---
font = pygame.font.SysFont("Courier New", 32)
big_font = pygame.font.SysFont("Courier New", 48)

# --- Menu startowe ---
in_menu = True

# --- Zegar ---
clock = pygame.time.Clock()

def draw_menu():
    WIN.fill(PALETTES["8bit"][0])
    title = big_font.render("TIME GLITCH: PIXEL PARADOX", True, PALETTES["8bit"][1])
    prompt = font.render("ENTER = Start | R = Reset postępu", True, PALETTES["8bit"][2])
    level_info = font.render(f"Poziom zapisany: {level}", True, PALETTES["8bit"][1])
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    WIN.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))
    WIN.blit(level_info, (WIDTH // 2 - level_info.get_width() // 2, HEIGHT // 1.5))
    pygame.display.update()


def draw():
    x_offset = random.randint(-5, 5) if glitching else 0
    y_offset = random.randint(-5, 5) if glitching else 0

    if level == 2 and bg_level2:
        WIN.blit(bg_level2, (0, 0))
    else:
        WIN.fill(PALETTES[current_palette][0])

    if use_sprite and player_sprite:
        WIN.blit(player_sprite, player.move(x_offset, y_offset))
    else:
        pygame.draw.rect(WIN, PALETTES[current_palette][1], player.move(x_offset, y_offset))

    for plat in platforms:
        pygame.draw.rect(WIN, PALETTES[current_palette][2], plat.move(x_offset, y_offset))

    if boss:
        pygame.draw.rect(WIN, (255, 0, 255), boss.move(x_offset, y_offset))

    draw_coins()

    if glitching:
        for _ in range(10):
            pygame.draw.rect(WIN, random.choice(PALETTES[current_palette]),
                             pygame.Rect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 5, 5))

    score = font.render(f"Epoki: {epochs_survived} | Monety: {coins_collected}", True, PALETTES[current_palette][1])
    WIN.blit(score, (10, 10))
    pygame.display.update()



def handle_input(keys):
    global player_velocity_y
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += 5
    if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and on_ground:
        player_velocity_y = -15


def apply_gravity():
    global player_velocity_y, on_ground
    player_velocity_y += gravity
    player.y += player_velocity_y
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and player_velocity_y >= 0:
            player.y = plat.y - player.height
            player_velocity_y = 0
            on_ground = True

def glitch_palette():
    global current_palette, epochs_survived, boss, level, platforms, use_sprite
    current_palette = random.choice(list(PALETTES.keys()))
    epochs_survived += 1
    if level == 1:
        spawn_boss()
    if epochs_survived == 5:
        level = 2
        platforms = platforms_level2
        boss = None
        use_sprite = True
        print("Awans do poziomu 2!")


# --- Zmodyfikowane zachowanie bossa ---
def spawn_boss():
    global boss
    if level == 1:
        boss = pygame.Rect(random.randint(600, 750), 200, 60, 60)

boss_velocity_y = 3

def update_boss():
    global boss, boss_direction, boss_velocity_y
    if boss:
        boss.x += boss_direction * 3
        boss.y += boss_velocity_y

        if boss.x <= 0 or boss.x >= WIDTH - boss.width:
            boss_direction *= -1

        if boss.y <= 100 or boss.y >= 400:
            boss_velocity_y *= -1


def check_collision_with_boss():
    if boss and player.colliderect(boss):
        save_score()
        game_over_screen()
        pygame.quit()
        sys.exit()

def save_score():
    with open("score.txt", "w") as f:
        f.write(f"Przetrwane epoki: {epochs_survived}\n")

def game_over_screen():
    global in_menu, player, player_velocity_y, epochs_survived, boss, frame_count
    save_score()
    save_progress()

    WIN.fill((0, 0, 0))
    text = big_font.render("Koniec gry!", True, (255, 0, 0))
    score = font.render(f"Epoki: {epochs_survived}", True, (255, 255, 255))
    prompt = font.render("ENTER = zagraj ponownie | ESC = wyjście", True, (200, 200, 200))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
    WIN.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2))
    WIN.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 1.5))
    pygame.display.update()

    # Czekanie na decyzję gracza
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Reset gry
                    player = pygame.Rect(100, 500, 40, 40)
                    player_velocity_y = 0
                    epochs_survived = 0
                    boss = None
                    frame_count = 0
                    waiting = False
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                    
                    
def draw_coins():
    for coin in coins:
        pygame.draw.circle(WIN, coin_color, coin.center, 10)

def check_coin_collection():
    global coins_collected
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            coins_collected += 1


def save_progress():
    with open("progress.txt", "w") as f:
        f.write(f"{level}\n{epochs_survived}")

def load_progress():
    global level, epochs_survived
    try:
        with open("progress.txt", "r") as f:
            data = f.read().splitlines()
            level = int(data[0])
            epochs_survived = int(data[1])
    except:
        level = 1
        epochs_survived = 0

def reset_progress():
    with open("progress.txt", "w") as f:
        f.write("1\n0")


load_progress()

# --- Główna pętla gry ---
frame_count = 0
running = True

# --- Zmodyfikowana główna pętla gry ---
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_score()
            running = False

    if in_menu:
        draw_menu()
        if keys[pygame.K_RETURN]:
            in_menu = False
        if keys[pygame.K_r]:
            reset_progress()
            load_progress()
        continue

    handle_input(keys)
    apply_gravity()
    update_boss()
    check_collision_with_boss()
    check_coin_collection()

    if player.y > HEIGHT + 100:
        save_score()
        game_over_screen()

    frame_count += 1
    if frame_count % (FPS * 5) == 0:
        glitch_palette()
        glitching = True
        glitch_timer = FPS // 2

    if glitch_timer > 0:
        glitch_timer -= 1
    else:
        glitching = False

    draw()

pygame.quit()
sys.exit()
