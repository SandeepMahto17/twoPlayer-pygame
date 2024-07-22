import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 600
BACKGROUND_COLOR = (0, 128, 0)  # Green field
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 100
PLAYER_SPEED = 5
BALL_RADIUS = 15
GOAL_WIDTH, GOAL_HEIGHT = 150, 10
GOAL_X_LEFT, GOAL_X_RIGHT = 20, WIDTH - GOAL_WIDTH - 20
GOAL_Y = HEIGHT // 2 - GOAL_HEIGHT // 2
GRAVITY = 0.3
BALL_SPEED = 20
SCORE_FONT_SIZE = 32
PLAYER1_START = (WIDTH // 4, HEIGHT // 2 - PLAYER_HEIGHT // 2)
PLAYER2_START = (WIDTH * 3 // 4 - PLAYER_WIDTH, HEIGHT // 2 - PLAYER_HEIGHT // 2)
AIM_LINE_LENGTH = 150

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Detailed Football Game')

# Load fonts
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

# Player class
class Player:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = color
        self.controls = controls
        self.score = 0
        self.jumping = False
        self.vel_y = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']]:
            self.rect.x -= PLAYER_SPEED
        if keys[self.controls['right']]:
            self.rect.x += PLAYER_SPEED
        if keys[self.controls['up']] and not self.jumping:
            self.jumping = True
            self.vel_y = -10
        if keys[self.controls['down']]:
            self.rect.y += PLAYER_SPEED

        # Apply gravity
        if self.jumping:
            self.rect.y += self.vel_y
            self.vel_y += GRAVITY
            if self.rect.y >= HEIGHT - PLAYER_HEIGHT:
                self.rect.y = HEIGHT - PLAYER_HEIGHT
                self.jumping = False
                self.vel_y = 0

        # Prevent the player from going out of bounds
        self.rect.x = max(0, min(WIDTH - PLAYER_WIDTH, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - PLAYER_HEIGHT, self.rect.y))

    def draw(self):
        # Draw body
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw head
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.y - 15), 15)
        # Draw arms
        pygame.draw.rect(screen, self.color, (self.rect.x - 10, self.rect.y + 20, 10, 60))
        pygame.draw.rect(screen, self.color, (self.rect.right, self.rect.y + 20, 10, 60))
        # Draw legs
        pygame.draw.rect(screen, self.color, (self.rect.x + 10, self.rect.bottom, 10, 40))
        pygame.draw.rect(screen, self.color, (self.rect.right - 20, self.rect.bottom, 10, 40))

# Football class
class Football:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.color = (255, 165, 0)
        self.vel_x = 0
        self.vel_y = 0
        self.held_by = None

    def move(self):
        if self.held_by is None:
            self.vel_y += GRAVITY
            self.x += self.vel_x
            self.y += self.vel_y
            # Collision with ground
            if self.y + self.radius > HEIGHT:
                self.y = HEIGHT - self.radius
                self.vel_y *= -0.5
            # Collision with walls
            if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
                self.vel_x *= -0.5
        else:
            self.x = self.held_by.rect.centerx
            self.y = self.held_by.rect.top - self.radius

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def draw_aim_line(self):
        if self.held_by is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.x
            dy = mouse_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance == 0:
                return
            dx /= distance
            dy /= distance
            end_x = self.x + dx * AIM_LINE_LENGTH
            end_y = self.y + dy * AIM_LINE_LENGTH
            pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (end_x, end_y), 2)

# Initialize players and football
player1 = Player(*PLAYER1_START, (0, 0, 255), {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
player2 = Player(*PLAYER2_START, (255, 0, 0), {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN})
football = Football(WIDTH // 2, HEIGHT // 2)

# Function to check if the ball is in the goal
def check_goal(ball):
    if ball.x < GOAL_X_LEFT + GOAL_WIDTH and GOAL_Y < ball.y < GOAL_Y + GOAL_HEIGHT:
        return "left"
    if ball.x > GOAL_X_RIGHT - GOAL_WIDTH and GOAL_Y < ball.y < GOAL_Y + GOAL_HEIGHT:
        return "right"
    return None

# Function to reset the ball and players
def reset():
    player1.rect.topleft = PLAYER1_START
    player2.rect.topleft = PLAYER2_START
    football.x, football.y = WIDTH // 2, HEIGHT // 2
    football.vel_x = football.vel_y = 0
    football.held_by = None

# Function to draw the football field
def draw_field():
    # Fill the background
    screen.fill(BACKGROUND_COLOR)
    # Draw the field lines
    pygame.draw.rect(screen, (255, 255, 255), (50, 50, WIDTH - 100, HEIGHT - 100), 5)
    pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2, 50), (WIDTH // 2, HEIGHT - 50), 5)
    pygame.draw.circle(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2), 75, 5)
    pygame.draw.rect(screen, (255, 255, 255), (GOAL_X_LEFT, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (GOAL_X_RIGHT, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and football.held_by is not None:
                football.held_by = None
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - football.x
                dy = mouse_y - football.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance != 0:
                    football.vel_x = dx / distance * BALL_SPEED
                    football.vel_y = dy / distance * BALL_SPEED

    # Move players
    player1.move()
    player2.move()

    # Move football
    football.move()

    # Check collisions
    if football.held_by is None:
        if player1.rect.colliderect(pygame.Rect(football.x - football.radius, football.y - football.radius, 2 * football.radius, 2 * football.radius)):
            football.held_by = player1
        elif player2.rect.colliderect(pygame.Rect(football.x - football.radius, football.y - football.radius, 2 * football.radius, 2 * football.radius)):
            football.held_by = player2

    # Check scoring
    goal = check_goal(football)
    if goal:
        if goal == "left":
            player2.score += 1
        elif goal == "right":
            player1.score += 1
        reset()

    # Draw the field
    draw_field()

    # Draw the players and football
    player1.draw()
    player2.draw()
    football.draw()
    football.draw_aim_line()

    # Draw scores
    player1_score_text = score_font.render(f"Player 1: {player1.score}", True, (255, 255, 255))
    player2_score_text = score_font.render(f"Player 2: {player2.score}", True, (255, 255, 255))
    screen.blit(player1_score_text, (20, 20))
    screen.blit(player2_score_text, (WIDTH - player2_score_text.get_width() - 20, 20))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
