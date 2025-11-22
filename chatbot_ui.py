import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import os

class ChatbotUI:
    def __init__(self, root, mooddetector, musicplayer):
        self.root = root
        self.mooddetector = mooddetector
        self.musicplayer = musicplayer
        self.language = tk.StringVar()
        self.mood = tk.StringVar()

        # Background image
        try:
            self.bg_image = Image.open("background.jpeg")
            self.bg_image = self.bg_image.resize((800, 600))
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            self.root.configure(bg="#050f1e")

        # Chatbot Area
        frame = tk.Frame(self.root, bg="#050f1e")
        frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        tk.Label(frame, text="Language", bg="#050f1e", fg="white").pack(pady=5)
        langs = [
            "English", "Japanese", "Korean",
            "Hindi", "Pahadi", "Indo-western", "South-Indian", "Haryanvi"
        ]
        self.language_dropdown = tk.OptionMenu(frame, self.language, *langs)
        self.language.set(langs[0])
        self.language_dropdown.pack(pady=5)

        tk.Label(frame, text="How do you feel? (Write mood)", bg="#050f1e", fg="white").pack(pady=5)
        self.mood_entry = tk.Entry(frame, textvariable=self.mood)
        self.mood_entry.pack(pady=5)

        tk.Button(frame, text="Play Mood Music", command=self.play_music).pack(pady=5)

        control_frame = tk.Frame(frame, bg='#050f1e')
        control_frame.pack(pady=8)

        tk.Button(control_frame, text="Play", command=self.play_music).grid(row=0, column=0, padx=4)
        tk.Button(control_frame, text="Pause", command=self.musicplayer.pause).grid(row=0, column=1, padx=4)
        tk.Button(control_frame, text="Resume", command=self.musicplayer.resume).grid(row=0, column=2, padx=4)
        tk.Button(control_frame, text="Stop", command=self.musicplayer.stop).grid(row=0, column=3, padx=4)
        tk.Button(control_frame, text="Prev", command=self.musicplayer.previous).grid(row=0, column=4, padx=4)
        tk.Button(control_frame, text="Next", command=self.musicplayer.next).grid(row=0, column=5, padx=4)

        # Favorites and Playlists
        tk.Button(frame, text="Add to Favorites", command=self.add_favorite).pack(pady=2)
        tk.Button(frame, text="Play Favorites", command=self.musicplayer.play_favorites).pack(pady=2)
        tk.Button(frame, text="Create Playlist", command=self.create_playlist).pack(pady=2)
        tk.Button(frame, text="Load Playlist", command=self.load_playlist).pack(pady=2)

        self.status = tk.Label(frame, text="", bg="#050f1e", fg="yellow")
        self.status.pack(pady=5)

    def play_music(self):
        lang = self.language.get()
        user_mood = self.mooddetector.detect(self.mood.get())
        self.musicplayer.play_music(lang, user_mood)
        self.status.config(text=f"Playing {user_mood} ({lang})")

    def add_favorite(self):
        song_path = self.musicplayer.get_current_song_path()
        if song_path:
            self.musicplayer.add_to_favorites(song_path)
            messagebox.showinfo("Added", "Song added to favorites!")

    def create_playlist(self):
        # Add song file paths one by one
        songs = []
        while True:
            song = simpledialog.askstring("Playlist", "Add song (full path), or leave empty to finish:")
            if not song:
                break
            if os.path.exists(song):
                songs.append(song)
        if songs:
            name = simpledialog.askstring("Name", "Enter playlist name:")
            if name:
                self.musicplayer.create_playlist(name, songs)
                messagebox.showinfo("Created", f"Playlist {name} created.")

    def load_playlist(self):
        plists = self.musicplayer.list_playlists()
        if not plists:
            messagebox.showinfo("No playlists", "No playlists found!")
            return
        name = simpledialog.askstring("Playlists", "Available:\n" + "\n".join(plists) + "\n\nType playlist name to play:")
        if name and name in plists:
            self.musicplayer.load_playlist(name)
            self.status.config(text=f"Playing playlist: {name}")
