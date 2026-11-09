
import pygame
import random
import math

pygame.init()

# Pengaturan layar
WIDTH = 900
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON BREAKER - Galaxy Mission")

clock = pygame.time.Clock()
FPS = 60

# Warna
BLACK = (8, 10, 30)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
PURPLE = (170, 0, 255)
PINK = (255, 40, 150)
YELLOW = (255, 220, 50)
GREEN = (50, 255, 130)

# Font
font = pygame.font.Font(None, 35)
big_font = pygame.font.Font(None, 75)

# Status game
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"
VICTORY = "victory"

state = MENU

score = 0
lives = 3
level = 1

# Bintang latar belakang
stars = []

for i in range(80):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])


# Paddle
class Paddle:

    def __init__(self):
        self.width = 120
        self.height = 15
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 60
        self.speed = 8

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        self.x = max(0, min(WIDTH - self.width, self.x))

    def draw(self):
        pygame.draw.rect(
            screen, CYAN,
            (self.x, self.y, self.width, self.height),
            border_radius=10
        )

        pygame.draw.rect(
            screen, WHITE,
            (self.x, self.y, self.width, self.height),
            2, border_radius=10
        )

    def get_rect(self):
        return pygame.Rect(
            self.x, self.y,
            self.width, self.height
        )


# Ball
class Ball:

    def __init__(self):
        self.radius = 9
        self.x = WIDTH // 2
        self.y = HEIGHT - 85
        self.speed_x = 4
        self.speed_y = -5
        self.active = False

    def move(self, paddle):

        if not self.active:
            self.x = paddle.x + paddle.width // 2
            self.y = paddle.y - self.radius
            return False

        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.speed_x *= -1

        if self.y <= self.radius:
            self.speed_y *= -1

        # Tabrakan dengan paddle
        ball_rect = self.get_rect()

        if ball_rect.colliderect(paddle.get_rect()):
            self.speed_y = -abs(self.speed_y)

            # Mengubah arah bola berdasarkan posisi benturan
            tengah = paddle.x + paddle.width / 2
            jarak = (self.x - tengah) / (paddle.width / 2)

            self.speed_x = jarak * 6

        # Bola jatuh
        if self.y > HEIGHT:
            return True

        return False

    def draw(self):
        pygame.draw.circle(
            screen, WHITE,
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            screen, CYAN,
            (int(self.x), int(self.y)),
            self.radius + 4, 2
        )

    def get_rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )


# Block
class Block:

    def __init__(self, x, y, color, health):
        self.rect = pygame.Rect(x, y, 75, 25)
        self.color = color
        self.health = health

    def draw(self):

        if self.health > 0:
            pygame.draw.rect(
                screen, self.color,
                self.rect, border_radius=5
            )

            pygame.draw.rect(
                screen, WHITE,
                self.rect, 1, border_radius=5
            )

    def hit(self):
        self.health -= 1


# Power Up
class PowerUp:

    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.rect = pygame.Rect(x, y, 25, 25)

    def move(self):
        self.y += 3
        self.rect.y = self.y

    def draw(self):
        color = GREEN if self.kind == "wide" else YELLOW

        pygame.draw.circle(
            screen, color,
            (self.x + 12, self.y + 12), 12
        )

    def apply(self, paddle):
        if self.kind == "wide":
            paddle.width = 180


# Membuat balok
def create_blocks(level):

    blocks = []

    colors = [CYAN, PURPLE, PINK, GREEN]

    for row in range(4 + level):

        for col in range(10):

            x = 35 + col * 83
            y = 70 + row * 38

            health = 1

            if row % 2 == 0:
                health = level

            block = Block(
                x, y,
                colors[row % len(colors)],
                health
            )

            blocks.append(block)

    return blocks


# Menggambar teks
def draw_text(text, font_type, color, x, y):
    image = font_type.render(text, True, color)
    rect = image.get_rect(center=(x, y))
    screen.blit(image, rect)


# Menggambar latar
def draw_background():

    screen.fill(BLACK)

    for star in stars:
        pygame.draw.circle(
            screen, WHITE,
            (star[0], star[1]),
            star[2]
        )


# Reset game
def reset_game():

    global score, lives, level
    global paddle, ball, blocks, powerups, state

    score = 0
    lives = 3
    level = 1

    paddle = Paddle()
    ball = Ball()
    blocks = create_blocks(level)
    powerups = []

    state = PLAYING


# Inisialisasi
paddle = Paddle()
ball = Ball()
blocks = create_blocks(level)
powerups = []


# Game utama
running = True

while running:

    clock.tick(FPS)

    draw_background()

    # Event
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if state == MENU:
                if event.key == pygame.K_SPACE:
                    reset_game()

            elif state == PLAYING:

                if event.key == pygame.K_SPACE:
                    ball.active = True

                if event.key == pygame.K_ESCAPE:
                    state = PAUSED

            elif state == PAUSED:

                if event.key == pygame.K_ESCAPE:
                    state = PLAYING

            elif state == GAME_OVER or state == VICTORY:

                if event.key == pygame.K_SPACE:
                    reset_game()

    # MENU
    if state == MENU:

        draw_text(
            "NEON BREAKER",
            big_font, CYAN,
            WIDTH // 2, 220
        )

        draw_text(
            "GALAXY MISSION",
            font, PURPLE,
            WIDTH // 2, 280
        )

        draw_text(
            "PRESS SPACE TO START",
            font, WHITE,
            WIDTH // 2, 400
        )

        draw_text(
            "LEFT / RIGHT = MOVE",
            font, GREEN,
            WIDTH // 2, 460
        )

    # PLAYING
    elif state == PLAYING:

        paddle.move()

        lost = ball.move(paddle)

        # Jika bola jatuh
        if lost:

            lives -= 1
            ball = Ball()

            if lives <= 0:
                state = GAME_OVER

        # Tabrakan bola dengan block
        for block in blocks[:]:

            if ball.get_rect().colliderect(block.rect):

                ball.speed_y *= -1
                block.hit()

                if block.health <= 0:

                    blocks.remove(block)
                    score += 10

                    if random.random() < 0.2:
                        powerups.append(
                            PowerUp(
                                block.rect.x,
                                block.rect.y,
                                random.choice(["wide", "life"])
                            )
                        )

                break

        # Power up
        for power in powerups[:]:

            power.move()

            if power.rect.colliderect(paddle.get_rect()):

                if power.kind == "wide":
                    paddle.width = 180

                else:
                    lives += 1

                powerups.remove(power)

            elif power.y > HEIGHT:
                powerups.remove(power)

        # Level selesai
        if len(blocks) == 0:

            level += 1

            if level > 3:
                state = VICTORY

            else:
                blocks = create_blocks(level)
                ball = Ball()
                paddle = Paddle()
                powerups = []

        # Gambar paddle dan bola
        paddle.draw()
        ball.draw()

        # Gambar balok
        for block in blocks:
            block.draw()

        # Gambar power up
        for power in powerups:
            power.draw()

        # Informasi game
        draw_text(
            "SCORE: " + str(score),
            font, CYAN, 110, 25
        )

        draw_text(
            "LIVES: " + str(lives),
            font, PINK, 300, 25
        )

        draw_text(
            "LEVEL: " + str(level),
            font, GREEN, 500, 25
        )

        draw_text(
            "SPACE: LAUNCH",
            font, WHITE, 740, 25
        )

    # PAUSE
    elif state == PAUSED:

        draw_text(
            "GAME PAUSED",
            big_font, YELLOW,
            WIDTH // 2, 280
        )

        draw_text(
            "PRESS ESC TO CONTINUE",
            font, WHITE,
            WIDTH // 2, 370
        )

    # GAME OVER
    elif state == GAME_OVER:

        draw_text(
            "GAME OVER",
            big_font, PINK,
            WIDTH // 2, 260
        )

        draw_text(
            "FINAL SCORE: " + str(score),
            font, WHITE,
            WIDTH // 2, 340
        )

        draw_text(
            "PRESS SPACE TO RESTART",
            font, CYAN,
            WIDTH // 2, 420
        )

    # VICTORY
    elif state == VICTORY:

        draw_text(
            "YOU WIN!",
            big_font, GREEN,
            WIDTH // 2, 260
        )

        draw_text(
            "GALAXY SAVED!",
            font, WHITE,
            WIDTH // 2, 340
        )

        draw_text(
            "FINAL SCORE: " + str(score),
            font, CYAN,
            WIDTH // 2, 390
        )

        draw_text(
            "PRESS SPACE TO PLAY AGAIN",
            font, WHITE,
            WIDTH // 2, 450
        )

    pygame.display.update()


pygame.quit()
