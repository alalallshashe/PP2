import pygame, sys, random, json, os
from db import save_score, get_top_10

pygame.init()

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "settings.json")

W, H = 800, 600
CELL = 20

win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Game - TSIS 4")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 28)
small = pygame.font.SysFont("Verdana", 20)

try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = json.load(file)
except Exception:
    config = {"snake_color": [66,165,245], "grid": True, "sound": True}

user_name = ""
state = "MENU"

class Game:
    def __init__(self, name):
        self.name = name
        self.snake = [(120,120),(100,120),(80,120)]
        self.dir = (CELL,0)
        self.score = 0
        self.level = 1
        self.speed = 10
        self.obstacles = []
        self.power = None
        self.power_type = None
        self.active_power = None
        self.power_end = 0
        self.shield = False
        self.food = self.spawn()
        self.poison = self.spawn()
        self.spawn_obstacles()

    def spawn(self):
        occupied = set(self.snake) | set(self.obstacles)
        if hasattr(self, "food") and self.food:
            occupied.add((self.food[0], self.food[1]))
        if hasattr(self, "poison") and self.poison:
            occupied.add((self.poison[0], self.poison[1]))
        if self.power:
            occupied.add(self.power)

        positions = [(x, y) for x in range(0, W, CELL) for y in range(0, H, CELL) if (x, y) not in occupied]
        if not positions:
            return (0, 0, 1)
        x, y = random.choice(positions)
        return (x, y, random.randint(1, 3))

    def spawn_obstacles(self):
        self.obstacles = []
        if self.level < 3:
            return
        occupied = set(self.snake)
        if self.food:
            occupied.add((self.food[0], self.food[1]))
        if self.poison:
            occupied.add((self.poison[0], self.poison[1]))
        if self.power:
            occupied.add(self.power)
        count = min(self.level * 3, (W // CELL) * (H // CELL) - len(occupied) - 5)
        while len(self.obstacles) < count:
            x = random.randrange(0, W, CELL)
            y = random.randrange(0, H, CELL)
            if (x, y) not in occupied and (x, y) not in self.obstacles:
                self.obstacles.append((x, y))

    def spawn_power(self):
        occupied = set(self.snake) | set(self.obstacles)
        if self.food:
            occupied.add((self.food[0], self.food[1]))
        if self.poison:
            occupied.add((self.poison[0], self.poison[1]))

        positions = [(x, y) for x in range(0, W, CELL) for y in range(0, H, CELL) if (x, y) not in occupied]
        if not positions:
            return
        self.power = random.choice(positions)
        self.power_type = random.choice(["SPEED", "SLOW", "SHIELD"])

    def update(self):
        now = pygame.time.get_ticks()

        if self.active_power and now > self.power_end:
            self.speed = 10 + self.level * 2
            self.active_power = None
            self.shield = False

        x,y = self.snake[0]
        nx,ny = x+self.dir[0], y+self.dir[1]
        new = (nx,ny)

        if nx<0 or ny<0 or nx>=W or ny>=H:
            return False

        if new in self.snake or new in self.obstacles:
            if self.shield:
                self.shield = False
            else:
                return False

        self.snake.insert(0,new)

        if new==(self.food[0],self.food[1]):
            self.score += self.food[2]
            if self.score // 5 > self.level - 1:
                self.level += 1
                self.speed += 2
                self.spawn_obstacles()
            self.food = self.spawn()

        elif new==(self.poison[0],self.poison[1]):
            if len(self.snake)<=3:
                return False
            self.snake = self.snake[:-2]
            self.poison = self.spawn()

        elif self.power and new==self.power:
            self.active_power = self.power_type
            self.power_end = now + 5000

            if self.power_type=="SPEED":
                self.speed = 20
            elif self.power_type=="SLOW":
                self.speed = 5
            elif self.power_type=="SHIELD":
                self.shield = True

            self.power = None

        else:
            self.snake.pop()

        if not self.power and random.random()<0.01:
            self.spawn_power()

        return True

game = None

PLAY_BTN = pygame.Rect(300, 250, 200, 50)
LEAD_BTN = pygame.Rect(300, 320, 200, 50)
SET_BTN = pygame.Rect(300, 390, 200, 50)
BACK_BTN = pygame.Rect(320, 500, 150, 40)


def draw_button(text, rect, hover=False):
    color = (255,220,120) if hover else (240,240,240)
    pygame.draw.rect(win, color, rect, border_radius=10)
    pygame.draw.rect(win, (0,0,0), rect, 2, border_radius=10)
    win.blit(small.render(text, True, (0,0,0)), (rect.x + 20, rect.y + 15))


def button_hover(rect):
    return rect.collidepoint(pygame.mouse.get_pos())


def button_clicked(rect, events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and rect.collidepoint(event.pos):
            return True
    return False

def menu(events):
    global state, game, user_name

    win.fill((30,30,40))
    win.blit(font.render("SNAKE GAME", True, (255,255,255)), (280,100))
    win.blit(small.render("Type your name or press PLAY to start as Player", True, (220,220,220)), (180,170))
    win.blit(small.render(f"Player: {user_name}_", True, config["snake_color"]), (320,210))

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_name = user_name[:-1]
            elif event.key == pygame.K_RETURN:
                if not user_name:
                    user_name = "Player"
                game = Game(user_name)
                state = "GAME"
            else:
                if len(user_name) < 12 and event.unicode.isprintable():
                    user_name += event.unicode

    draw_button("PLAY", PLAY_BTN, button_hover(PLAY_BTN))
    draw_button("LEADERBOARD", LEAD_BTN, button_hover(LEAD_BTN))
    draw_button("SETTINGS", SET_BTN, button_hover(SET_BTN))

    if button_clicked(PLAY_BTN, events):
        if not user_name:
            user_name = "Player"
        game = Game(user_name)
        state = "GAME"
    elif button_clicked(LEAD_BTN, events):
        state = "LEAD"
    elif button_clicked(SET_BTN, events):
        state = "SET"

def game_loop():
    global state

    win.fill((240,240,240))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and game.dir!=(0,CELL):
        game.dir=(0,-CELL)
    if keys[pygame.K_DOWN] and game.dir!=(0,-CELL):
        game.dir=(0,CELL)
    if keys[pygame.K_LEFT] and game.dir!=(CELL,0):
        game.dir=(-CELL,0)
    if keys[pygame.K_RIGHT] and game.dir!=(-CELL,0):
        game.dir=(CELL,0)

    if not game.update():
        try:
            save_score(game.name,game.score,game.level)
        except Exception:
            pass
        state="MENU"

    if config.get("grid"):
        grid_col = (200, 200, 200)
        for gx in range(0, W, CELL):
            pygame.draw.line(win, grid_col, (gx, 0), (gx, H), 1)
        for gy in range(0, H, CELL):
            pygame.draw.line(win, grid_col, (0, gy), (W, gy), 1)

    for s in game.snake:
        pygame.draw.rect(win, config["snake_color"], (s[0], s[1], CELL, CELL))

    for o in game.obstacles:
        pygame.draw.rect(win, (50,50,50), (o[0], o[1], CELL, CELL))

    if game.power:
        pygame.draw.rect(win,(255,215,0),(game.power[0],game.power[1],CELL,CELL))

    pygame.draw.rect(win,(0,200,0),(game.food[0],game.food[1],CELL,CELL))
    pygame.draw.rect(win,(150,0,0),(game.poison[0],game.poison[1],CELL,CELL))

    win.blit(font.render(f"Score: {game.score}",True,(0,0,0)),(10,10))

    if game.active_power:
        win.blit(small.render(f"{game.active_power}",True,(255,140,0)),(650,10))

def leaderboard(events):
    global state

    win.fill((10,10,10))
    win.blit(font.render("LEADERBOARD", True, (255,255,255)), (300,50))

    top = get_top_10()
    y = 120
    for i, r in enumerate(top[:10]):
        win.blit(small.render(f"{i+1}. {r[0]} - {r[1]}", True, (255,255,255)), (280,y))
        y += 30

    draw_button("BACK", BACK_BTN, button_hover(BACK_BTN))
    if button_clicked(BACK_BTN, events):
        state = "MENU"


def settings(events):
    global state, config

    win.fill((220,220,220))
    win.blit(font.render("SETTINGS", True, (0,0,0)), (330,80))

    draw_button(f"GRID: {config['grid']}", PLAY_BTN, button_hover(PLAY_BTN))
    draw_button("CHANGE COLOR", LEAD_BTN, button_hover(LEAD_BTN))
    draw_button("SAVE & BACK", SET_BTN, button_hover(SET_BTN))

    if button_clicked(PLAY_BTN, events):
        config["grid"] = not config["grid"]
    if button_clicked(LEAD_BTN, events):
        config["snake_color"] = [random.randint(50,255), random.randint(50,255), random.randint(50,255)]
    if button_clicked(SET_BTN, events):
        with open(CONFIG_PATH, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=2)
        state = "MENU"


def main():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if state == "MENU":
            menu(events)
        elif state == "GAME":
            game_loop()
        elif state == "LEAD":
            leaderboard(events)
        elif state == "SET":
            settings(events)

        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":
    main()