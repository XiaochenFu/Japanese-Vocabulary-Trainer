import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
import json
import os
from gtts import gTTS
from playsound import playsound
import threading
import hashlib
from pathlib import Path

STATE_FILE = "vocab_state.json"
CSV_FILE = "all_N1_N5.csv"
TEMP_MP3 = "temp.mp3"
INITIAL_COUNT = 3
SAVE_INTERVAL = 5

class Word:
    def __init__(self, word, reading, meaning):
        self.word = word
        self.reading = reading
        self.meaning = meaning
        self.appear_count = INITIAL_COUNT
        self.read_count = 0
        self.meaning_count = 0

    def to_dict(self):
        return {
            "word": self.word,
            "reading": self.reading,
            "meaning": self.meaning,
            "appear_count": self.appear_count,
            "read_count": self.read_count,
            "meaning_count": self.meaning_count
        }

    @classmethod
    def from_dict(cls, data):
        w = cls(data["word"], data["reading"], data["meaning"])
        w.appear_count = data["appear_count"]
        w.read_count = data["read_count"]
        w.meaning_count = data["meaning_count"]
        return w

class VocabTrainer:
    def __init__(self, master):
        self.master = master
        self.master.title("Japanese Vocabulary Trainer")

        self.words = self.load_words()
        self.current_word = None
        self.interaction_count = 0

        self.label = tk.Label(master, text="", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.meaning_label = tk.Label(master, text="", font=("Helvetica", 16))
        self.meaning_label.pack()

        self.play_button = tk.Button(master, text="Play Reading (r)", command=self.play_reading)
        self.play_button.pack(pady=5)

        self.show_button = tk.Button(master, text="Show Meaning (m)", command=self.show_meaning)
        self.show_button.pack(pady=5)

        self.next_button = tk.Button(master, text="Next Word (n)", command=self.next_word)
        self.next_button.pack(pady=10)

        self.master.bind("<r>", lambda e: self.play_reading())
        self.master.bind("<m>", lambda e: self.show_meaning())
        self.master.bind("<n>", lambda e: self.next_word())

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.next_word()

    def load_words(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Word.from_dict(d) for d in data]

        df = pd.read_csv(CSV_FILE)
        words = []
        for _, row in df.iterrows():
            words.append(Word(row.iloc[0], row.iloc[1], row.iloc[2]))
        return words

    def save_words(self):
        data = [w.to_dict() for w in self.words]
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def choose_word(self):
        candidates = [w for w in self.words if (
            w.appear_count > 0 or w.read_count > 0 or w.meaning_count > 0)]
        if not candidates:
            messagebox.showinfo("Done!", "You have reviewed all the words!")
            return None
        return random.choice(candidates)

    def next_word(self):
        if self.current_word:
            self.current_word.appear_count = max(0, self.current_word.appear_count - 1)
            if not self.revealed_reading:
                self.current_word.read_count = max(0, self.current_word.read_count - 1)
            if not self.revealed_meaning:
                self.current_word.meaning_count = max(0, self.current_word.meaning_count - 1)

        word = self.choose_word()
        if word is None:
            self.label.config(text="🎉 Done!")
            self.meaning_label.config(text="")
            return

        self.current_word = word
        self.revealed_reading = False
        self.revealed_meaning = False
        self.label.config(text=word.word)
        self.meaning_label.config(text="")

        self.interaction_count += 1
        if self.interaction_count % SAVE_INTERVAL == 0:
            self.save_words()

    def play_reading(self):
        if not self.current_word:
            return
        self.revealed_reading = True
        self.current_word.read_count += 2

        def tts_play():
            try:
                cache_dir = Path(".cache/tts_audio")
                cache_dir.mkdir(parents=True, exist_ok=True)
                hashname = hashlib.md5(self.current_word.reading.encode('utf-8')).hexdigest()
                filename = cache_dir / f"{hashname}.mp3"

                if not filename.exists():
                    tts = gTTS(self.current_word.reading, lang="ja")
                    tts.save(str(filename))

                playsound(str(filename))

            except Exception as e:
                print("TTS playback error:", e)

        threading.Thread(target=tts_play).start()

    def show_meaning(self):
        if not self.current_word:
            return
        self.revealed_meaning = True
        self.current_word.meaning_count += 2
        self.meaning_label.config(text=self.current_word.meaning)

    def on_closing(self):
        self.save_words()
        if os.path.exists(TEMP_MP3):
            try:
                os.remove(TEMP_MP3)
            except:
                pass
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = VocabTrainer(root)
    root.mainloop()
