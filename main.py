from chatbot_ui import ChatbotUI
from mood_detector import MoodDetector
from music_player import MusicPlayer
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Moodify Chatbot Music Player")
    root.geometry("800x600")
    root.resizable(False, False)
    music_dir = "music"
    music_player = MusicPlayer(music_dir)
    mood_detector = MoodDetector()
    ui = ChatbotUI(root, mood_detector, music_player)
    root.mainloop()
