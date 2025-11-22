import pygame
import os
import json

class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        self.current_songs = []
        self.current_index = 0
        self.current_language = ""
        self.current_mood = ""
        pygame.mixer.init()
        self.load_favorites()

    def play_music(self, language, mood):
        folder = os.path.join(self.music_dir, language, mood)
        if not os.path.exists(folder):
            print(f"ERROR: Folder {folder} does not exist.")
            self.current_songs = []
            return
        self.current_songs = [f for f in os.listdir(folder) if f.endswith('.mp3')]
        if not self.current_songs:
            print("ERROR: No songs found.")
            return
        self.current_index = 0
        self.current_language = language
        self.current_mood = mood
        self.play_current_song()

    def play_current_song(self):
        if not self.current_songs:
            return
        song_name = self.current_songs[self.current_index]
        if self.current_language and self.current_mood:
            path = os.path.join(self.music_dir, self.current_language, self.current_mood, song_name)
        else:
            path = song_name  # This is for playlists/favorites containing full paths
        if not os.path.exists(path):
            print(f"ERROR: Song file does not exist at {path}")
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        if self.current_index < len(self.current_songs) - 1:
            self.current_index += 1
        else:
            self.current_index = 0
        self.play_current_song()

    def previous(self):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = len(self.current_songs) - 1
        self.play_current_song()

    def get_current_song_path(self):
        if not self.current_songs:
            return None
        song_name = self.current_songs[self.current_index]
        if self.current_language and self.current_mood:
            return os.path.join(self.music_dir, self.current_language, self.current_mood, song_name)
        else:
            return song_name  # When songs contain full paths (as in playlists/favorites)

    # Favorites Management (Corrected & Robust)
    def load_favorites(self):
        try:
            with open('favorites.json', 'r') as f:
                self.favorites = json.load(f)
            if not isinstance(self.favorites, list):
                self.favorites = []
        except Exception:
            self.favorites = []

    def save_favorites(self):
        with open('favorites.json', 'w') as f:
            json.dump(self.favorites, f)

    def add_to_favorites(self, song_path):
        if song_path and os.path.exists(song_path):
            # Avoid duplicates
            if song_path not in self.favorites:
                self.favorites.append(song_path)
                self.save_favorites()
            else:
                print("Song already in favorites.")
        else:
            print("ERROR: Song path for favorite is invalid or does not exist.")

    def remove_from_favorites(self, song_path):
        if song_path in self.favorites:
            self.favorites.remove(song_path)
            self.save_favorites()

    def play_favorites(self):
        self.load_favorites()
        # Ensure all paths exist and are mp3 files
        self.current_songs = [sp for sp in self.favorites if sp and os.path.exists(sp) and sp.endswith('.mp3')]
        self.current_index = 0
        self.current_language = ""
        self.current_mood = ""
        if self.current_songs:
            pygame.mixer.music.load(self.current_songs[0])
            pygame.mixer.music.play()
        else:
            print("No playable favorites found.")

    # Playlist management
    def create_playlist(self, name, songs):
        plist = f"{name}_playlist.json"
        with open(plist, 'w') as f:
            json.dump(songs, f)

    def load_playlist(self, name):
        plist = f"{name}_playlist.json"
        with open(plist, 'r') as f:
            self.current_songs = json.load(f)
        self.current_songs = [s for s in self.current_songs if s and os.path.exists(s) and s.endswith('.mp3')]
        self.current_index = 0
        self.current_language = ""
        self.current_mood = ""
        self.play_current_song()

    def list_playlists(self):
        return [f[:-13] for f in os.listdir() if f.endswith("_playlist.json")]
