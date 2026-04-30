import pygame, random, math, os
from pygame.locals import *

BASE_DIR = os.path.dirname(__file__)
W, H = 700, 700
WHITE=(255,255,255); BLACK=(0,0,0); GRAY=(80,80,80)
YELLOW=(255,220,0); GREEN=(50,200,80); RED=(220,50,50)
BLUE=(50,130,220); ORANGE=(255,140,0); CYAN=(0,220,220)

LANE_X  = [117,210,303,396,489,582]
ROAD_L, ROAD_R = 80, 620
LINE_COL = (220,220,60)

DIFF = {
    "easy":   {"speed":4, "t_rate":180, "o_rate":240},
    "normal": {"speed":5, "t_rate":130, "o_rate":180},
    "hard":   {"speed":7, "t_rate":80,  "o_rate":120},
}

def load(path, size):
    image_path = os.path.join(BASE_DIR, path)
    img = pygame.image.load(image_path)
    return pygame.transform.smoothscale(img, size)

class Road:
    def __init__(self):
        self.off = 0
    def update(self, spd):
        self.off = (self.off + spd) % 100
    def draw(self, surf):
        surf.fill((35,35,35))
        pygame.draw.rect(surf, (55,55,55), (ROAD_L,0,ROAD_R-ROAD_L,H))
        pygame.draw.rect(surf, (180,140,60), (ROAD_L-10,0,10,H))
        pygame.draw.rect(surf, (180,140,60), (ROAD_R,0,10,H))
        for lx in LANE_X[:-1]:
            x = lx + (LANE_X[1]-LANE_X[0])//2
            y = -60 + self.off
            while y < H:
                pygame.draw.rect(surf, LINE_COL, (x-2,y,4,50))
                y += 100

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load("images/car.png", (70,110))
        self.rect  = self.image.get_rect(center=(W//2, H-120))
        self.nitro = False; self.shield = False
        self.nitro_t = 0.0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        spd  = 7 + (4 if self.nitro else 0)
        if keys[K_LEFT]  and self.rect.left  > ROAD_L+4: self.rect.x -= spd
        if keys[K_RIGHT] and self.rect.right < ROAD_R-4: self.rect.x += spd
        if self.nitro:
            self.nitro_t -= dt
            if self.nitro_t <= 0: self.nitro = False

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        if self.shield:
            pygame.draw.ellipse(surf, CYAN, self.rect.inflate(20,20), 3)
        if self.nitro:
            for _ in range(5):
                fx = self.rect.centerx + random.randint(-12,12)
                fy = self.rect.bottom  + random.randint(0,16)
                pygame.draw.circle(surf, ORANGE, (fx,fy), random.randint(3,8))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, spd):
        super().__init__()
        self.image = load("images/enemy.png", (70,110))
        self.rect  = self.image.get_rect()
        self.spd   = spd + random.uniform(-0.5,1.5)
        self.rect.centerx = random.choice(LANE_X)
        self.rect.bottom  = random.randint(-200,-50)
    def update(self): self.rect.y += self.spd; return self.rect.top > H
    def draw(self, surf): surf.blit(self.image, self.rect)

OBS_TYPES = [
    ("oil",     (20,20,80),   70,30),
    ("barrier", (220,80,30),  80,20),
    ("pothole", (30,30,30),   50,28),
    ("bump",    (100,80,60),  80,18),
]
OBS_SLOW = {"oil":2.0,"pothole":1.0,"bump":0.5,"barrier":0}

class Obstacle:
    def __init__(self, spd):
        self.kind,self.col,w,h = random.choice(OBS_TYPES)
        self.spd  = spd + random.uniform(0,1)
        self.rect = pygame.Rect(random.choice(LANE_X)-w//2, random.randint(-300,-60), w, h)
    def update(self): self.rect.y += self.spd; return self.rect.top > H
    def draw(self, surf):
        pygame.draw.rect(surf, self.col, self.rect, border_radius=5)
        f = pygame.font.SysFont("Verdana",12)
        surf.blit(f.render(self.kind.upper(),True,WHITE), f.render(self.kind.upper(),True,WHITE).get_rect(center=self.rect.center))
    def slow(self): return OBS_SLOW.get(self.kind,0)

class RoadEvent:
    def __init__(self, spd):
        self.kind = random.choice(["nitro","slow"])
        self.col  = CYAN if self.kind=="nitro" else RED
        self.spd  = spd
        self.rect = pygame.Rect(ROAD_L, -40, ROAD_R-ROAD_L, 20)
        self.life = 300
    def update(self): self.rect.y += self.spd; self.life-=1; return self.rect.top>H or self.life<=0
    def draw(self, surf):
        pygame.draw.rect(surf, self.col, self.rect)
        lbl = "NITRO BOOST" if self.kind=="nitro" else "SLOW ZONE"
        f = pygame.font.SysFont("Verdana",13,bold=True)
        surf.blit(f.render(lbl,True,WHITE), f.render(lbl,True,WHITE).get_rect(center=self.rect.center))

PU_INFO = {
    "nitro":  (ORANGE,"N"),
    "shield": (CYAN,  "S"),
    "repair": (GREEN, "R"),
}

class PowerUp:
    SZ = 34; LIFE = 8.0
    def __init__(self, spd):
        self.kind = random.choice(["nitro","shield","repair"])
        self.col, self.lbl = PU_INFO[self.kind]
        self.spd  = spd; self.life = self.LIFE; self.anim = 0.0
        self.rect = pygame.Rect(random.choice(LANE_X)-self.SZ//2, random.randint(-200,-60), self.SZ, self.SZ)
    def update(self, dt): self.rect.y+=self.spd; self.life-=dt; self.anim=(self.anim+3)%360; return self.rect.top>H or self.life<=0
    def draw(self, surf):
        r = self.SZ//2 + int(3*math.sin(math.radians(self.anim)))
        cx,cy = self.rect.center
        pygame.draw.circle(surf, self.col, (cx,cy), r)
        pygame.draw.circle(surf, WHITE, (cx,cy), r, 2)
        f = pygame.font.SysFont("Verdana",18,bold=True)
        surf.blit(f.render(self.lbl,True,WHITE), f.render(self.lbl,True,WHITE).get_rect(center=(cx,cy)))

class Coin:
    SIZES={1:28,2:36,3:44}; COLORS={1:YELLOW,2:ORANGE,3:(220,80,220)}
    def __init__(self, spd):
        self.w = random.choices([1,2,3],weights=[60,30,10])[0]
        sz = self.SIZES[self.w]
        self.image = load("images/coin.png", (sz,sz))
        self.spd  = spd; self.anim=random.randint(0,360)
        self.rect = pygame.Rect(random.choice(LANE_X)-sz//2, random.randint(-350,-60), sz, sz)
    def update(self): self.rect.y+=self.spd; self.anim=(self.anim+4)%360; return self.rect.top>H
    def draw(self, surf): surf.blit(self.image, self.rect)

def draw_hud(surf, score, coins, dist, active_pu, pu_t, slow_t):
    f = pygame.font.SysFont("Verdana",22)
    surf.blit(f.render(f"Score: {score}",  True,WHITE),  (ROAD_L+4,10))
    surf.blit(f.render(f"Coins: {coins}",  True,YELLOW), (ROAD_L+4,38))
    surf.blit(f.render(f"Dist:  {dist}m",  True,CYAN),   (ROAD_L+4,66))
    if active_pu:
        col = PU_INFO[active_pu][0]
        lbl = active_pu.upper() + (f" {max(0,pu_t):.1f}s" if active_pu=="nitro" else "")
        t = pygame.font.SysFont("Verdana",18).render(lbl,True,col)
        surf.blit(t, t.get_rect(center=(W//2,22)))
    if slow_t > 0:
        t = pygame.font.SysFont("Verdana",17).render(f"SLOW {slow_t:.1f}s",True,RED)
        surf.blit(t, t.get_rect(center=(W//2,50)))

class GameSession:
    COINS_FOR_SPEED = 5
    def __init__(self, surf, clock, settings):
        self.surf=surf; self.clock=clock
        p = DIFF.get(settings.get("difficulty","normal"), DIFF["normal"])
        self.base_spd=p["speed"]; self.t_rate=p["t_rate"]; self.o_rate=p["o_rate"]
        self.road=Road(); self.player=Player()
        self.enemies=[]; self.obs=[]; self.events=[]; self.pups=[]; self.coins=[]
        self.et=0; self.ot=0; self.evt=0; self.put=0; self.ct=0
        self.score=0; self.coins_total=0; self.coins_ctr=0
        self.spd=float(self.base_spd); self.dist=0; self.frame=0
        self.active_pu=None; self.pu_t=0.0
        self.slow_t=0.0; self.is_slow=False

    def _safe(self, r):
        return not self.player.rect.inflate(60,200).colliderect(r)

    def _spawn(self):
        self.et+=1; self.ot+=1; self.evt+=1; self.put+=1; self.ct+=1
        rate_t = max(40, self.t_rate - self.frame//600)
        rate_o = max(60, self.o_rate - self.frame//400)
        if self.et>=rate_t:
            self.et=0
            e=Enemy(self.spd)
            if self._safe(e.rect): self.enemies.append(e)
        if self.ot>=rate_o:
            self.ot=0
            o=Obstacle(self.spd)
            if self._safe(o.rect): self.obs.append(o)
        if self.evt>=300:
            self.evt=0
            if random.random()<0.5: self.events.append(RoadEvent(self.spd))
        if self.put>=200:
            self.put=0
            if random.random()<0.4:
                pu=PowerUp(self.spd)
                if self._safe(pu.rect): self.pups.append(pu)
        if self.ct>=60:
            self.ct=0
            c=Coin(self.spd)
            if self._safe(c.rect): self.coins.append(c)

    def _collide(self):
        ph = self.player.rect.inflate(-16,-20)
        for e in self.enemies[:]:
            if ph.colliderect(e.rect.inflate(-16,-20)):
                if self.player.shield: self.player.shield=False; self.enemies.remove(e)
                else: return True
        for o in self.obs[:]:
            if ph.colliderect(o.rect):
                if self.player.shield: self.player.shield=False; self.obs.remove(o)
                elif o.kind=="barrier": return True
                else:
                    s=o.slow(); self.slow_t=max(self.slow_t,s); self.is_slow=s>0
                    self.obs.remove(o)
        for ev in self.events:
            if ph.colliderect(ev.rect):
                if ev.kind=="nitro":
                    self.player.nitro=True; self.player.nitro_t=3.0
                    self.active_pu="nitro"; self.pu_t=3.0
                else: self.slow_t=max(self.slow_t,2.0); self.is_slow=True
        for pu in self.pups[:]:
            if ph.colliderect(pu.rect):
                if pu.kind=="nitro":
                    self.player.nitro=True; self.player.nitro_t=4.0
                    self.active_pu="nitro"; self.pu_t=4.0
                elif pu.kind=="shield":
                    self.player.shield=True; self.active_pu="shield"
                elif pu.kind=="repair":
                    self.is_slow=False; self.slow_t=0
                    if self.obs: self.obs.pop(0)
                    self.active_pu="repair"
                self.score+=20; self.pups.remove(pu)
        for c in self.coins[:]:
            if ph.colliderect(c.rect):
                self.coins_total+=c.w; self.coins_ctr+=c.w
                self.score+=c.w*10; self.coins.remove(c)
                if self.coins_ctr>=self.COINS_FOR_SPEED:
                    self.spd+=0.5; self.coins_ctr=0
        return False

    def run(self):
        while True:
            dt = self.clock.tick(60)/1000.0
            for ev in pygame.event.get():
                if ev.type==QUIT: pygame.quit(); import sys; sys.exit()
                if ev.type==KEYDOWN and ev.key==K_ESCAPE: return self.score, self.dist//60, self.coins_total
            self.frame+=1
            cs = self.spd+(4 if self.player.nitro else 0)-(3 if self.is_slow else 0)
            cs = max(2, cs)
            if self.is_slow:
                self.slow_t-=dt
                if self.slow_t<=0: self.is_slow=False
            if self.active_pu=="nitro":
                self.pu_t-=dt
                if self.pu_t<=0: self.active_pu=None
            elif self.active_pu in("shield","repair") and not self.player.shield:
                self.active_pu=None
            self._spawn()
            self.road.update(cs); self.player.update(dt)
            self.dist+=int(cs); self.score+=1
            self.enemies=[e for e in self.enemies if not e.update()]
            self.obs    =[o for o in self.obs     if not o.update()]
            self.events =[e for e in self.events  if not e.update()]
            self.pups   =[p for p in self.pups    if not p.update(dt)]
            self.coins  =[c for c in self.coins   if not c.update()]
            if self._collide(): return self.score, self.dist//60, self.coins_total
            self.road.draw(self.surf)
            for e in self.events:  e.draw(self.surf)
            for o in self.obs:     o.draw(self.surf)
            for e in self.enemies: e.draw(self.surf)
            for p in self.pups:    p.draw(self.surf)
            for c in self.coins:   c.draw(self.surf)
            self.player.draw(self.surf)
            draw_hud(self.surf, self.score, self.coins_total, self.dist//60,
                     self.active_pu, self.pu_t, self.slow_t)
            pygame.display.flip()