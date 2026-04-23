import pygame, sys
from pygame.locals import *
import random, os

pygame.init()

# Get script directory for image paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HIGH_SCORE_FILE = os.path.join(SCRIPT_DIR, "high_score.txt")

# Load high score
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read())
        except:
            return 0
    return 0

# Save high score
def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(score))
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
font_large = pygame.font.SysFont("Verdana", 40, bold=True)
font = pygame.font.SysFont("Verdana", 24)
score = 0        
coins_collected = 0 
speed = 5
high_score = load_high_score()  # Load best score
grace_period_frames = 120  # 2 seconds at 60 FPS
frames_passed = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(os.path.join(SCRIPT_DIR, "images/enemy.png"))
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect()
        self.reset()
    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
    def move(self):
        global score, speed
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            speed += 0.2
            self.reset()
    def draw(self, surface):
        surface.blit(self.image, self.rect)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(os.path.join(SCRIPT_DIR, "images/car.png"))
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-7, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(7, 0)
    def draw(self, surface):
        surface.blit(self.image, self.rect)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(os.path.join(SCRIPT_DIR, "images/coin.png"))
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()
        self.reset()
    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-300, -50) 
    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()
    def draw(self, surface):
        surface.blit(self.image, self.rect)
P1 = Player()
enemies = []
coins = []

# Create initial enemies and coins
for i in range(3):
    E = Enemy()
    E.rect.center = (random.choice([50, 120, 190, 260, 330]), random.randint(-400, -100))
    enemies.append(E)

for i in range(2):
    C = Coin()
    C.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(-400, -200))
    coins.append(C)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    P1.update()
    
    # Update enemies
    for enemy in enemies:
        enemy.move()
        # Respawn far from player
        if enemy.rect.top > SCREEN_HEIGHT:
            enemy.rect.center = (random.choice([50, 120, 190, 260, 330]), -50)
    
    # Update coins
    for coin in coins:
        coin.move()
        if coin.rect.top > SCREEN_HEIGHT:
            coin.reset()
    
    # Add more enemies as score increases
    if score > 0 and score % 5 == 0 and len(enemies) < 3 + (score // 5):
        E = Enemy()
        E.rect.center = (random.choice([50, 120, 190, 260, 330]), -100)
        enemies.append(E)
    
    # Add more coins occasionally
    if coins_collected > 0 and coins_collected % 3 == 0 and len(coins) < 2 + (coins_collected // 3):
        C = Coin()
        C.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)
        coins.append(C)
    
    # Collision with coins
    for coin in coins[:]:
        if pygame.sprite.collide_rect(P1, coin):
            coins_collected += 1
            coins.remove(coin)
    
    # Collision with enemies (after grace period)
    if frames_passed > grace_period_frames:
        for enemy in enemies:
            if pygame.sprite.collide_rect(P1, enemy):
                # Update high score if needed
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                
                # Game over screen
                DISPLAYSURF.fill((0, 0, 0))
                
                game_over_font = pygame.font.SysFont("Verdana", 50, bold=True)
                text = game_over_font.render("GAME OVER", True, (255, 0, 0))
                rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
                DISPLAYSURF.blit(text, rect)
                
                score_font = pygame.font.SysFont("Verdana", 36)
                score_text = score_font.render(f"Score: {score}", True, (0, 255, 0))
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10))
                DISPLAYSURF.blit(score_text, score_rect)
                
                coins_text = score_font.render(f"Coins: {coins_collected}", True, (255, 215, 0))
                coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 35))
                DISPLAYSURF.blit(coins_text, coins_rect)
                
                best_text = score_font.render(f"Best Score: {high_score}", True, (255, 100, 100))
                best_rect = best_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
                DISPLAYSURF.blit(best_text, best_rect)
                
                pygame.display.update()
                pygame.time.delay(3000)
                pygame.quit()
                sys.exit()
    
    DISPLAYSURF.fill((50, 50, 50))  
    P1.draw(DISPLAYSURF)
    for enemy in enemies:
        enemy.draw(DISPLAYSURF)
    for coin in coins:
        coin.draw(DISPLAYSURF)
    
    # Draw semi-transparent background for stats
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (5, 5, SCREEN_WIDTH - 10, 60))
    pygame.draw.rect(DISPLAYSURF, (100, 100, 100), (5, 5, SCREEN_WIDTH - 10, 60), 2)
    
    # Display stats
    score_text = font_large.render(f"Score: {score}", True, (0, 255, 0))
    DISPLAYSURF.blit(score_text, (15, 12))
    
    coin_text = font.render(f"Coins: {coins_collected}", True, (255, 215, 0))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 150, 22))
    
    high_score_text = font.render(f"Best: {high_score}", True, (255, 100, 100))
    DISPLAYSURF.blit(high_score_text, (SCREEN_WIDTH // 2 - 60, 35))
    
    frames_passed += 1
    pygame.display.update()
    FramePerSec.tick(FPS)