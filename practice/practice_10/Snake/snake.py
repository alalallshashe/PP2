import pygame
import sys
import random

# Initializing Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Level Up Edition")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Fonts for UI
font = pygame.font.SysFont("Verdana", 24)

# Snake initialization: starting positions as a list of tuples
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0) # Moving Right initially

# Variables for Game Logic
score = 0
level = 1
foods_collected_in_level = 0
LEVEL_UP_THRESHOLD = 3  # Increase level every 3 foods
speed = 10

def generate_food():
    """Generates random position for food that is not inside the snake body."""
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        # Check if the generated position overlaps with any part of the snake
        if (x, y) not in snake:
            return (x, y)

# Initial food generation
food = generate_food()

def draw_snake():
    """Draws each segment of the snake on the screen."""
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], CELL_SIZE, CELL_SIZE))

def draw_food():
    """Draws the food item on the screen."""
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

def check_wall_collision(head):
    """Returns True if the snake head is outside the boundaries."""
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        return True
    return False

def check_self_collision(head):
    """Returns True if the snake head hits any part of its body."""
    if head in snake:
        return True
    return False

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Handling direction changes (preventing 180-degree turns)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    # Calculate new position for the head
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # 1. Checking for border (wall) collision
    if check_wall_collision(new_head):
        print(f"Game Over! Final Score: {score}")
        pygame.quit()
        sys.exit()

    # Checking for self collision
    if check_self_collision(new_head):
        print("Game Over: Self Collision")
        pygame.quit()
        sys.exit()

    # Move snake: Add new head
    snake.insert(0, new_head)

    # Check if snake ate the food
    if new_head == food:
        score += 1
        foods_collected_in_level += 1
        
        # 2. Generate random position for food (validated against snake body)
        food = generate_food()
        
        # 3. Add levels & 4. Increase speed
        if foods_collected_in_level >= LEVEL_UP_THRESHOLD:
            level += 1
            foods_collected_in_level = 0
            speed += 3 # Make the game faster
            print(f"Level Up! Current Level: {level}")
    else:
        # If no food eaten, remove the last tail segment to simulate movement
        snake.pop()

    # --- Drawing Section ---
    screen.fill(BLACK)
    
    draw_snake()
    draw_food()

    # 5. Add counter to score and level on screen
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 120, 10)) # Top right corner

    pygame.display.update()
    
    # Control the game speed based on current level
    clock.tick(speed)