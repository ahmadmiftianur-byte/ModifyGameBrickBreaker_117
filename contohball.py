
import pygame
import random

pygame.init()

# Dimensions of the screen
WIDTH, HEIGHT = 600, 500

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 20)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker")

clock = pygame.time.Clock()
FPS = 30


# Striker class
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    def display(self):
        pygame.draw.rect(screen, self.color, self.strikerRect)

    def update(self, xFac):
        self.posx += self.speed * xFac

        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    def getRect(self):
        return self.strikerRect


# Block class
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100

        if color == WHITE:
            self.health = 200
        else:
            self.health = 100

        self.blockRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    def display(self):
        if self.health > 0:
            pygame.draw.rect(screen, self.color, self.blockRect)

    def hit(self):
        self.health -= self.damage

    def getRect(self):
        return self.blockRect

    def getHealth(self):
        return self.health


# Ball class
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1

        self.ball = pygame.Rect(
            self.posx - radius,
            self.posy - radius,
            radius * 2,
            radius * 2
        )

    def display(self):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.posx), int(self.posy)),
            self.radius
        )

    def update(self):
        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        # Ball collision with left and right walls
        if self.posx - self.radius <= 0:
            self.posx = self.radius
            self.xFac *= -1

        elif self.posx + self.radius >= WIDTH:
            self.posx = WIDTH - self.radius
            self.xFac *= -1

        # Ball collision with top wall
        if self.posy - self.radius <= 0:
            self.posy = self.radius
            self.yFac *= -1

        self.ball = pygame.Rect(
            int(self.posx - self.radius),
            int(self.posy - self.radius),
            self.radius * 2,
            self.radius * 2
        )

        # Check if ball falls below screen
        if self.posy - self.radius >= HEIGHT:
            return True

        return False

    def reset(self):
        # Reset ball to center
        self.posx = WIDTH // 2
        self.posy = HEIGHT - 150
        self.xFac, self.yFac = 1, -1

        self.ball = pygame.Rect(
            int(self.posx - self.radius),
            int(self.posy - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def hit(self):
        self.yFac *= -1

    def getRect(self):
        return self.ball


# Helper Functions
def collisionChecker(rect, ball):
    return pygame.Rect.colliderect(rect, ball)


def populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap):
    listOfBlocks = []

    for i in range(0, WIDTH, blockWidth + horizontalGap):
        for j in range(0, HEIGHT // 2, blockHeight + verticalGap):
            listOfBlocks.append(
                Block(
                    i,
                    j,
                    blockWidth,
                    blockHeight,
                    random.choice([WHITE, GREEN])
                )
            )

    return listOfBlocks


def gameOver():
    waiting = True

    while waiting:
        screen.fill(BLACK)

        text = pygame.font.Font(None, 50).render(
            "GAME OVER", True, RED
        )

        restart = font.render(
            "Press SPACE to restart", True, WHITE
        )

        screen.blit(
            text,
            text.get_rect(center=(WIDTH // 2, 220))
        )

        screen.blit(
            restart,
            restart.get_rect(center=(WIDTH // 2, 280))
        )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

        clock.tick(FPS)

    return False


# Game Manager
def main():
    running = True
    lives = 3
    score = 0

    striker = Striker(
        WIDTH // 2 - 50,
        HEIGHT - 50,
        100,
        20,
        10,
        WHITE
    )

    strikerXFac = 0

    # Ball starts at the center
    ball = Ball(
        WIDTH // 2,
        HEIGHT - 150,
        7,
        5,
        WHITE
    )

    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20

    listOfBlocks = populateBlocks(
        blockWidth,
        blockHeight,
        horizontalGap,
        verticalGap
    )

    while running:
        screen.fill(BLACK)

        # Display score and lives
        scoreText = font.render(
            "Score : " + str(score), True, WHITE
        )

        livesText = font.render(
            "Lives : " + str(lives), True, WHITE
        )

        screen.blit(scoreText, (20, HEIGHT - 25))
        screen.blit(livesText, (120, HEIGHT - 25))

        # Repopulate blocks
        if not listOfBlocks:
            listOfBlocks = populateBlocks(
                blockWidth,
                blockHeight,
                horizontalGap,
                verticalGap
            )

        # Game over
        if lives <= 0:
            running = gameOver()

            if not running:
                break

            lives = 3
            score = 0

            striker = Striker(
                WIDTH // 2 - 50,
                HEIGHT - 50,
                100,
                20,
                10,
                WHITE
            )

            ball = Ball(
                WIDTH // 2,
                HEIGHT - 150,
                7,
                5,
                WHITE
            )

            strikerXFac = 0

            listOfBlocks = populateBlocks(
                blockWidth,
                blockHeight,
                horizontalGap,
                verticalGap
            )

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1

                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            if event.type == pygame.KEYUP:
                if event.key in (
                    pygame.K_LEFT,
                    pygame.K_RIGHT
                ):
                    strikerXFac = 0

        # Collision check with striker
        if collisionChecker(striker.getRect(), ball.getRect()):
            if ball.yFac > 0:
                ball.hit()

        # Collision check with blocks
        for block in listOfBlocks[:]:
            if collisionChecker(block.getRect(), ball.getRect()):
                ball.hit()
                block.hit()

                if block.getHealth() <= 0:
                    listOfBlocks.remove(block)
                    score += 5

        # Update striker position
        striker.update(strikerXFac)

        # Update ball position
        lifeLost = ball.update()

        if lifeLost:
            lives -= 1
            ball.reset()
            print("Lives:", lives)

        # Display striker and ball
        striker.display()
        ball.display()

        # Display blocks
        for block in listOfBlocks:
            block.display()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
