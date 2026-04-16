import pygame
import sys
from player import MusicPlayer

# Инициализация Pygame
pygame.init()

# Получение информации об экране
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Music Player")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (20, 20, 20)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
ACCENT = (0, 150, 255)
GREEN = (0, 200, 100)
RED = (255, 50, 80)

# Шрифты
font_title = pygame.font.SysFont("Arial", 48, bold=True)
font_large = pygame.font.SysFont("Arial", 32)
font_normal = pygame.font.SysFont("Arial", 20)
font_small = pygame.font.SysFont("Arial", 14)

# Создаем плеер с правильным путем
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
music_dir = os.path.join(script_dir, "music")
player = MusicPlayer(music_dir)

# UI State
show_playlist = False
visualization_bars = [0] * 20  # For animation

def draw_button(surface, rect, text, active=False, hover=False):
    """Draw a button"""
    color = ACCENT if active else (LIGHT_GRAY if hover else GRAY)
    pygame.draw.rect(surface, color, rect, border_radius=5)
    pygame.draw.rect(surface, WHITE if active else LIGHT_GRAY, rect, 2, border_radius=5)
    text_surf = font_normal.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)
    return rect

def draw_slider(surface, rect, value, label=""):
    """Draw a horizontal slider"""
    pygame.draw.rect(surface, LIGHT_GRAY, rect, border_radius=5)
    value_width = rect.width * max(0, min(1, value))
    pygame.draw.rect(surface, ACCENT, (rect.x, rect.y, value_width, rect.height), border_radius=5)
    # Draw slider knob
    knob_x = rect.x + value_width
    pygame.draw.circle(surface, WHITE, (int(knob_x), rect.y + rect.height // 2), 8)
    if label:
        label_surf = font_small.render(label, True, WHITE)
        surface.blit(label_surf, (rect.x, rect.y - 25))

def draw_progress_bar(surface, rect, current, total):
    """Draw progress bar with time indicator"""
    progress = current / total if total > 0 else 0
    pygame.draw.rect(surface, LIGHT_GRAY, rect, border_radius=3)
    pygame.draw.rect(surface, ACCENT, (rect.x, rect.y, rect.width * progress, rect.height), border_radius=3)
    
    # Draw time text
    time_text = f"{player.format_time(current)} / {player.format_time(total)}"
    time_surf = font_small.render(time_text, True, WHITE)
    surface.blit(time_surf, (rect.x, rect.y + rect.height + 5))

def draw_visualization(surface, x, y, width, height):
    """Draw animated visualization bars"""
    global visualization_bars
    bar_width = width // len(visualization_bars)
    
    # Animate bars
    for i in range(len(visualization_bars)):
        if player.is_playing_now():
            visualization_bars[i] = min(height, visualization_bars[i] + 3)
            if visualization_bars[i] > height * 0.7:
                visualization_bars[i] = height * 0.3
        else:
            visualization_bars[i] = max(0, visualization_bars[i] - 5)
    
    # Draw bars
    for i in range(len(visualization_bars)):
        bar_x = x + i * bar_width + 2
        bar_height = visualization_bars[i]
        pygame.draw.rect(surface, ACCENT, (bar_x, y + height - bar_height, bar_width - 4, bar_height))

def draw_playlist_panel(surface):
    """Draw playlist panel on the right side"""
    panel_width = 300
    panel_x = WIDTH - panel_width
    pygame.draw.rect(surface, GRAY, (panel_x, 0, panel_width, HEIGHT))
    pygame.draw.line(surface, LIGHT_GRAY, (panel_x, 0), (panel_x, HEIGHT), 2)
    
    # Title
    title_surf = font_large.render("Playlist", True, WHITE)
    surface.blit(title_surf, (panel_x + 10, 10))
    
    # Playlist items
    item_height = 40
    start_y = 60
    tracks = player.get_playlist()
    
    for i, track in enumerate(tracks[:min(15, len(tracks))]):  # Show max 15 items
        item_y = start_y + i * item_height
        if item_y + item_height > HEIGHT:
            break
        
        # Draw background
        if i == player.get_current_index():
            pygame.draw.rect(surface, ACCENT, (panel_x, item_y, panel_width, item_height))
        
        # Draw text
        track_name = track.rsplit('.', 1)[0][:25]  # Truncate long names
        track_surf = font_small.render(f"{i+1}. {track_name}", True, WHITE)
        surface.blit(track_surf, (panel_x + 10, item_y + 10))

# Main loop
running = True
mouse_over_volume = False

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    screen.fill(DARK_GRAY)
    
    # Calculate layout
    center_x = WIDTH // 2 if not show_playlist else (WIDTH - 150) // 2
    center_y = HEIGHT // 2
    button_spacing = 80
    
    # 1. Header - Current track info
    header_y = 40
    if player.playlist:
        current_track = player.get_current_track()
        track_surf = font_title.render(current_track, True, ACCENT)
        track_rect = track_surf.get_rect(center=(center_x, header_y))
        screen.blit(track_surf, track_rect)
        
        # Track counter
        counter_text = f"Track {player.get_current_index() + 1} / {player.get_playlist_count()}"
        counter_surf = font_normal.render(counter_text, True, LIGHT_GRAY)
        counter_rect = counter_surf.get_rect(center=(center_x, header_y + 50))
        screen.blit(counter_surf, counter_rect)
    else:
        no_music = font_title.render("No music files found", True, RED)
        no_music_rect = no_music.get_rect(center=(center_x, header_y))
        screen.blit(no_music, no_music_rect)
        
        help_text = font_normal.render(f"Add MP3, WAV, FLAC or OGG files to: {music_dir}", True, LIGHT_GRAY)
        help_rect = help_text.get_rect(center=(center_x, header_y + 60))
        screen.blit(help_text, help_rect)
    
    # 2. Visualization bars
    vis_y = header_y + 120
    vis_height = 60
    draw_visualization(screen, center_x - 150, vis_y, 300, vis_height)
    
    # 3. Progress bar
    progress_y = vis_y + vis_height + 30
    progress_rect = pygame.Rect(center_x - 200, progress_y, 400, 10)
    current_time = player.get_current_time()
    total_time = player.get_track_length()
    draw_progress_bar(screen, progress_rect, current_time, total_time)
    
    # 4. Control buttons
    buttons_y = progress_y + 60
    
    # Previous button
    prev_btn = pygame.Rect(center_x - button_spacing * 2, buttons_y, 60, 60)
    mouse_over_prev = prev_btn.collidepoint(mouse_pos)
    draw_button(screen, prev_btn, "<<", hover=mouse_over_prev)
    
    # Play/Pause button
    play_btn = pygame.Rect(center_x - button_spacing, buttons_y, 60, 60)
    mouse_over_play = play_btn.collidepoint(mouse_pos)
    play_text = "⏸" if player.is_playing_now() else "▶"
    draw_button(screen, play_btn, play_text, active=player.is_playing_now(), hover=mouse_over_play)
    
    # Stop button
    stop_btn = pygame.Rect(center_x, buttons_y, 60, 60)
    mouse_over_stop = stop_btn.collidepoint(mouse_pos)
    draw_button(screen, stop_btn, "⏹", hover=mouse_over_stop)
    
    # Next button
    next_btn = pygame.Rect(center_x + button_spacing, buttons_y, 60, 60)
    mouse_over_next = next_btn.collidepoint(mouse_pos)
    draw_button(screen, next_btn, ">>", hover=mouse_over_next)
    
    # Shuffle button
    shuffle_btn = pygame.Rect(center_x + button_spacing * 2, buttons_y, 60, 60)
    mouse_over_shuffle = shuffle_btn.collidepoint(mouse_pos)
    draw_button(screen, shuffle_btn, "🔀", active=player.shuffle, hover=mouse_over_shuffle)
    
    # 5. Volume control
    volume_y = buttons_y + 100
    volume_label = font_normal.render("Volume", True, WHITE)
    screen.blit(volume_label, (center_x - 100, volume_y - 30))
    
    volume_slider = pygame.Rect(center_x - 100, volume_y, 200, 10)
    draw_slider(screen, volume_slider, player.volume)
    mouse_over_volume = volume_slider.collidepoint(mouse_pos)
    
    # 6. Playlist toggle
    playlist_btn = pygame.Rect(center_x - 200, volume_y + 60, 80, 40)
    mouse_over_playlist = playlist_btn.collidepoint(mouse_pos)
    btn_text = "Hide" if show_playlist else "Show"
    draw_button(screen, playlist_btn, f"{btn_text} List", active=show_playlist, hover=mouse_over_playlist)
    
    # Help text
    help_y = HEIGHT - 100
    help_texts = [
        "KEYBOARD: P=Play/Pause | S=Stop | N=Next | B=Previous | +/-=Volume | L=Loop | U=Shuffle | Q=Quit | ESC=Exit"
    ]
    for i, text in enumerate(help_texts):
        help_surf = font_small.render(text, True, LIGHT_GRAY)
        screen.blit(help_surf, (20, help_y + i * 25))
    
    # Draw playlist panel if active
    if show_playlist:
        draw_playlist_panel(screen)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                if not player.is_playing:
                    player.play()
                else:
                    player.pause_unpause()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_UP or event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                player.set_volume(player.volume + 0.05)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_MINUS:
                player.set_volume(player.volume - 0.05)
            elif event.key == pygame.K_l:
                player.toggle_loop()
            elif event.key == pygame.K_u:
                player.toggle_shuffle()
            elif event.key == pygame.K_SPACE:
                show_playlist = not show_playlist
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Previous track
            if prev_btn.collidepoint(mouse_pos):
                player.prev()
            # Play/Pause
            elif play_btn.collidepoint(mouse_pos):
                if not player.is_playing:
                    player.play()
                else:
                    player.pause_unpause()
            # Stop
            elif stop_btn.collidepoint(mouse_pos):
                player.stop()
            # Next track
            elif next_btn.collidepoint(mouse_pos):
                player.next()
            # Shuffle
            elif shuffle_btn.collidepoint(mouse_pos):
                player.toggle_shuffle()
            # Playlist toggle
            elif playlist_btn.collidepoint(mouse_pos):
                show_playlist = not show_playlist
            # Volume slider
            elif volume_slider.collidepoint(mouse_pos):
                volume_value = (mouse_pos[0] - volume_slider.x) / volume_slider.width
                player.set_volume(volume_value)
            # Progress bar seek
            elif progress_rect.collidepoint(mouse_pos):
                seek_value = (mouse_pos[0] - progress_rect.x) / progress_rect.width
                player.set_position(seek_value)
            # Playlist item selection
            elif show_playlist and mouse_pos[0] > WIDTH - 300:
                panel_x = WIDTH - 300
                item_height = 40
                item_index = (mouse_pos[1] - 60) // item_height
                if 0 <= item_index < len(player.get_playlist()):
                    player.current_index = item_index
                    player.play()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()