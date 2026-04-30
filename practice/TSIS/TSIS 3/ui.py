import pygame
from pygame.locals import *

W, H = 700, 700
WHITE=(255,255,255); GRAY=(100,100,100); DARK=(30,30,30)
YELLOW=(255,220,0); GREEN=(50,200,80); RED=(220,50,50)
BLUE=(50,130,220); ORANGE=(255,140,0)

def font(s): return pygame.font.SysFont("Verdana", s)
def btn(surf, text, rect, color):
    pygame.draw.rect(surf, color, rect, border_radius=10)
    pygame.draw.rect(surf, WHITE, rect, 2, border_radius=10)
    t = font(26).render(text, True, WHITE)
    surf.blit(t, t.get_rect(center=rect.center))
def panel(surf, title):
    surf.fill(DARK)
    t = font(46).render(title, True, YELLOW)
    surf.blit(t, t.get_rect(center=(W//2, 70)))

DIFFICULTIES = ["easy","normal","hard"]

class MainMenu:
    LABELS = ["Play","Leaderboard","Settings","Quit"]
    COLORS = {"Play":GREEN,"Leaderboard":BLUE,"Settings":ORANGE,"Quit":RED}
    def __init__(self, surf):
        self.surf = surf
        self.buttons = {l: pygame.Rect(W//2-130, 220+i*70, 260, 54) for i,l in enumerate(self.LABELS)}
    def draw(self):
        panel(self.surf, "RACER")
        for l,r in self.buttons.items(): btn(self.surf, l, r, self.COLORS[l])
    def handle(self, event):
        if event.type == MOUSEBUTTONDOWN:
            for l,r in self.buttons.items():
                if r.collidepoint(event.pos): return l
        return None

class NameEntry:
    def __init__(self, surf):
        self.surf = surf; self.name = ""; self.done = False
        self.go_btn = pygame.Rect(W//2-100, 380, 200, 50)
    def draw(self):
        panel(self.surf, "Enter Name")
        t = font(22).render("Type your name and press Enter:", True, WHITE)
        self.surf.blit(t, t.get_rect(center=(W//2, 200)))
        box = pygame.Rect(W//2-160, 280, 320, 54)
        pygame.draw.rect(self.surf, GRAY, box, border_radius=8)
        pygame.draw.rect(self.surf, YELLOW, box, 2, border_radius=8)
        nt = font(30).render(self.name+"|", True, WHITE)
        self.surf.blit(nt, nt.get_rect(center=box.center))
        btn(self.surf, "GO!", self.go_btn, GREEN)
    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN and self.name.strip(): self.done = True
            elif event.key == K_BACKSPACE: self.name = self.name[:-1]
            elif len(self.name)<16 and event.unicode.isprintable(): self.name += event.unicode
        if event.type == MOUSEBUTTONDOWN:
            if self.go_btn.collidepoint(event.pos) and self.name.strip(): self.done = True
    def get_name(self): return self.name.strip() or "Player"

class SettingsScreen:
    def __init__(self, surf, settings):
        self.surf = surf; self.settings = dict(settings)
        self.back = pygame.Rect(W//2-110, 420, 220, 50)
    def draw(self):
        panel(self.surf, "Settings")
        f = font(24)
        self.surf.blit(f.render(f"Sound:       {'ON' if self.settings['sound'] else 'OFF'}", True, WHITE), (W//2-200, 200))
        self.surf.blit(f.render(f"Difficulty:  {self.settings['difficulty'].capitalize()}", True, WHITE), (W//2-200, 300))
        btn(self.surf, "Toggle", pygame.Rect(W//2+80, 192, 120, 40), GREEN if self.settings["sound"] else RED)
        btn(self.surf, "<", pygame.Rect(W//2+60,  292, 46, 40), ORANGE)
        btn(self.surf, ">", pygame.Rect(W//2+116, 292, 46, 40), ORANGE)
        btn(self.surf, "Back", self.back, GRAY)
    def handle(self, event):
        if event.type == MOUSEBUTTONDOWN:
            p = event.pos
            if pygame.Rect(W//2+80, 192, 120, 40).collidepoint(p):
                self.settings["sound"] = not self.settings["sound"]
            if pygame.Rect(W//2+60, 292, 46, 40).collidepoint(p):
                i = DIFFICULTIES.index(self.settings["difficulty"])
                self.settings["difficulty"] = DIFFICULTIES[(i-1) % len(DIFFICULTIES)]
            if pygame.Rect(W//2+116, 292, 46, 40).collidepoint(p):
                i = DIFFICULTIES.index(self.settings["difficulty"])
                self.settings["difficulty"] = DIFFICULTIES[(i+1) % len(DIFFICULTIES)]
            if self.back.collidepoint(p): return "back"
        return None

class GameOverScreen:
    def __init__(self, surf, score, distance, coins):
        self.surf=surf; self.score=score; self.distance=distance; self.coins=coins
        self.retry = pygame.Rect(W//2-140, 460, 120, 50)
        self.menu  = pygame.Rect(W//2+20,  460, 120, 50)
    def draw(self):
        panel(self.surf, "Game Over")
        f = font(26)
        for i,(l,v) in enumerate([("Score",self.score),("Distance",f"{self.distance}m"),("Coins",self.coins)]):
            t = f.render(f"{l}: {v}", True, WHITE)
            self.surf.blit(t, t.get_rect(center=(W//2, 220+i*70)))
        btn(self.surf, "Retry",     self.retry, GREEN)
        btn(self.surf, "Main Menu", self.menu,  BLUE)
    def handle(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.retry.collidepoint(event.pos): return "retry"
            if self.menu.collidepoint(event.pos):  return "menu"
        return None

class LeaderboardScreen:
    def __init__(self, surf, board):
        self.surf=surf; self.board=board
        self.back = pygame.Rect(W//2-90, 620, 180, 48)
    def draw(self):
        panel(self.surf, "Top 10")
        self.surf.blit(font(18).render(f"{'#':<4}{'Name':<16}{'Score':>8}{'Dist':>8}{'Coins':>7}", True, YELLOW), (60, 120))
        pygame.draw.line(self.surf, YELLOW, (60,144), (640,144), 1)
        for i,e in enumerate(self.board[:10]):
            c = WHITE if i%2==0 else (200,200,200)
            line = f"{i+1:<4}{e['name'][:14]:<16}{e['score']:>8}{e['distance']:>8}{e['coins']:>7}"
            self.surf.blit(font(17).render(line, True, c), (60, 154+i*44))
        if not self.board:
            t = font(20).render("No scores yet!", True, GRAY)
            self.surf.blit(t, t.get_rect(center=(W//2, 350)))
        btn(self.surf, "Back", self.back, GRAY)
    def handle(self, event):
        if event.type == MOUSEBUTTONDOWN and self.back.collidepoint(event.pos): return "back"
        return None