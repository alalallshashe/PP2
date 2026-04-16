import pygame
import os
import random

class MusicPlayer:
    def __init__(self, music_dir):
        pygame.mixer.init()
        self.music_dir = music_dir
        # Create music directory if it doesn't exist
        if not os.path.exists(music_dir):
            os.makedirs(music_dir)
        try:
            self.playlist = sorted([f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav', '.flac', '.ogg'))])
        except Exception as e:
            print(f"Error loading music directory: {e}")
            self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.7
        self.track_length = 0
        self.shuffle = False
        self.loop = 0  # 0: no loop, 1: loop all, 2: loop one
        pygame.mixer.music.set_volume(self.volume)

    def play(self):
        if self.playlist:
            track_path = os.path.join(self.music_dir, self.playlist[self.current_index])
            try:
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()
                self.is_playing = True
                self.is_paused = False
                self.track_length = pygame.mixer.Sound(track_path).get_length()
            except:
                self.skip_to_next()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False

    def pause_unpause(self):
        if self.is_playing:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.is_paused = True
            else:
                pygame.mixer.music.unpause()
                self.is_paused = False

    def next(self):
        if self.playlist:
            if self.shuffle:
                self.current_index = random.randint(0, len(self.playlist) - 1)
            else:
                self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play()

    def prev(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play()

    def skip_to_next(self):
        """Skip to next track on error"""
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            if self.is_playing:
                self.play()

    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    def get_current_track(self):
        if self.playlist:
            track_name = self.playlist[self.current_index]
            return track_name.rsplit('.', 1)[0]  # Remove extension
        return "No tracks found"

    def get_current_time(self):
        """Get current playback time in seconds"""
        if pygame.mixer.music.get_busy() and not self.is_paused:
            return pygame.mixer.music.get_pos() / 1000.0
        return 0

    def get_track_length(self):
        """Get total track length in seconds"""
        return self.track_length

    def set_position(self, position):
        """Set playback position (0.0 to 1.0)"""
        if self.playlist and self.track_length > 0:
            pos_sec = position * self.track_length
            try:
                pygame.mixer.music.set_pos(pos_sec)
            except:
                pass

    def get_playlist(self):
        """Return full playlist"""
        return self.playlist

    def get_current_index(self):
        return self.current_index

    def get_playlist_count(self):
        return len(self.playlist)

    def is_playing_now(self):
        """Check if music is actually playing (not paused)"""
        return self.is_playing and pygame.mixer.music.get_busy() and not self.is_paused

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        return self.shuffle

    def toggle_loop(self):
        self.loop = (self.loop + 1) % 3
        return self.loop

    def format_time(self, seconds):
        """Format seconds to MM:SS"""
        mins = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{mins:02d}:{secs:02d}"