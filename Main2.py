import pygame
import sys

# Inicjalizacja pygame
pygame.init()

# Ustawienia okna gry
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Mini Gry")

# Kolory retro
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)

# Font retro
FONT = pygame.font.SysFont("Courier New", 40)
SMALL_FONT = pygame.font.SysFont("Courier New", 20)

# Klasa bazowa dla mini gier
class MiniGame:
    def __init__(self):
        self.completed = False

    def run(self, screen):
        pass

# Przykładowa mini gra 1
class PongGame(MiniGame):
    def run(self, screen):
        clock = pygame.time.Clock()
        ball = pygame.Rect(WIDTH//2, HEIGHT//2, 15, 15)
        ball_speed = [5, 5]
        paddle = pygame.Rect(WIDTH//2-50, HEIGHT-20, 100, 10)
        paddle_speed = 7

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.move_ip(-paddle_speed, 0)
            if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
                paddle.move_ip(paddle_speed, 0)

            ball.x += ball_speed[0]
            ball.y += ball_speed[1]

            if ball.left <= 0 or ball.right >= WIDTH:
                ball_speed[0] = -ball_speed[0]
            if ball.top <= 0 or ball.colliderect(paddle):
                ball_speed[1] = -ball_speed[1]
            if ball.bottom >= HEIGHT:
                running = False

            screen.fill(BLACK)
            pygame.draw.ellipse(screen, CYAN, ball)
            pygame.draw.rect(screen, WHITE, paddle)
            pygame.display.flip()
            clock.tick(60)

        self.completed = True

# Główna klasa gry zarządzająca menu i levelami
class Game:
    def __init__(self):
        self.levels = [PongGame()]  # Tutaj możesz dodawać nowe mini gry
        self.current_level = 0

    def main_menu(self):
        while True:
            screen.fill(BLACK)
            title = FONT.render("Retro Mini Gry", True, CYAN)
            start_text = SMALL_FONT.render("Naciśnij ENTER, aby zacząć", True, WHITE)

            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
            screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.run_levels()

    def run_levels(self):
        for level in self.levels:
            level.run(screen)
            if level.completed:
                continue

        self.game_over()

    def game_over(self):
        screen.fill(BLACK)
        over_text = FONT.render("Koniec Gry!", True, CYAN)
        restart_text = SMALL_FONT.render("Naciśnij R, aby zagrać ponownie", True, WHITE)
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//3))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.main_menu()

# Uruchomienie gry
if __name__ == "__main__":
    game = Game()
    game.main_menu()