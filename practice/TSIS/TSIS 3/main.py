import pygame, sys
from pygame.locals import *
import persistence, ui
from racer import GameSession

pygame.init()
W, H = 700, 700
SURF  = pygame.display.set_mode((W,H))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Racer — TSIS3")

def main():
    settings    = persistence.load_settings()
    leaderboard = persistence.load_leaderboard()
    player_name = "Player"
    state       = "menu"

    menu = ui.MainMenu(SURF)
    name = ui.NameEntry(SURF)
    lb   = ui.LeaderboardScreen(SURF, leaderboard)
    cfg  = ui.SettingsScreen(SURF, settings)
    over = None

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                persistence.save_settings(settings)
                pygame.quit(); sys.exit()

        if state == "menu":
            menu.draw()
            for e in events:
                a = menu.handle(e)
                if a == "Play":         name=ui.NameEntry(SURF); state="name"
                elif a == "Leaderboard":leaderboard=persistence.load_leaderboard(); lb=ui.LeaderboardScreen(SURF,leaderboard); state="lb"
                elif a == "Settings":   cfg=ui.SettingsScreen(SURF,settings); state="cfg"
                elif a == "Quit":       persistence.save_settings(settings); pygame.quit(); sys.exit()

        elif state == "name":
            name.draw()
            for e in events: name.handle(e)
            if name.done: player_name=name.get_name(); state="game"

        elif state == "game":
            score,dist,coins = GameSession(SURF,CLOCK,settings).run()
            leaderboard = persistence.save_score(player_name,score,dist,coins)
            over  = ui.GameOverScreen(SURF,score,dist,coins)
            state = "over"
            continue

        elif state == "over":
            over.draw()
            for e in events:
                a = over.handle(e)
                if a == "retry": state="game"
                elif a == "menu": menu=ui.MainMenu(SURF); state="menu"

        elif state == "lb":
            lb.draw()
            for e in events:
                if lb.handle(e)=="back": state="menu"

        elif state == "cfg":
            cfg.draw()
            for e in events:
                if cfg.handle(e)=="back":
                    settings=cfg.settings
                    persistence.save_settings(settings)
                    state="menu"

        pygame.display.flip()
        CLOCK.tick(60)

if __name__=="__main__":
    main()