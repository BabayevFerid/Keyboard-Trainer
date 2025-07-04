import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from threading import Thread

class KeyboardTrainerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Master Game")
        self.root.geometry("900x700")
        self.root.configure(bg="#2e2e2e")
        
        # Game variables
        self.words = self.load_words()
        self.current_word = ""
        self.user_input = ""
        self.start_time = 0
        self.time_limit = 60
        self.game_active = False
        self.freestyle_mode = False
        self.correct_chars = 0
        self.total_chars = 0
        self.completed_words = 0
        
        # Color theme
        self.bg_color = "#2e2e2e"
        self.text_color = "#ffffff"
        self.accent_color = "#4CAF50"
        self.error_color = "#F44336"
        self.highlight_color = "#FFC107"
        
        # Main frame
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header = tk.Label(self.main_frame, text="⌨️ Keyboard Master", 
                             font=("Arial", 24, "bold"), 
                             fg=self.highlight_color, bg=self.bg_color)
        self.header.pack(pady=10)
        
        # Game mode selection
        self.mode_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.mode_frame.pack(pady=10)
        
        self.mode_var = tk.StringVar(value="timed")
        tk.Radiobutton(self.mode_frame, text="Timed Challenge", variable=self.mode_var, 
                      value="timed", command=self.toggle_mode, font=("Arial", 11),
                      fg=self.text_color, bg=self.bg_color, selectcolor=self.bg_color,
                      activebackground=self.bg_color, activeforeground=self.text_color).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(self.mode_frame, text="Freestyle Practice", variable=self.mode_var, 
                      value="freestyle", command=self.toggle_mode, font=("Arial", 11),
                      fg=self.text_color, bg=self.bg_color, selectcolor=self.bg_color,
                      activebackground=self.bg_color, activeforeground=self.text_color).pack(side=tk.LEFT, padx=10)
        
        # Time selection (only visible in timed mode)
        self.time_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.time_frame.pack(pady=5)
        
        tk.Label(self.time_frame, text="Time Limit (sec):", font=("Arial", 11), 
                fg=self.text_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.time_slider = tk.Scale(self.time_frame, from_=30, to=300, orient=tk.HORIZONTAL,
                                  bg=self.bg_color, fg=self.text_color, highlightthickness=0,
                                  troughcolor="#424242", activebackground=self.accent_color)
        self.time_slider.set(60)
        self.time_slider.pack(side=tk.LEFT)
        
        # Difficulty selection
        self.diff_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.diff_frame.pack(pady=10)
        
        tk.Label(self.diff_frame, text="Difficulty:", font=("Arial", 11), 
                fg=self.text_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.difficulty = tk.StringVar(value="medium")
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        for text, value in difficulties:
            tk.Radiobutton(self.diff_frame, text=text, variable=self.difficulty, 
                         value=value, command=self.change_difficulty, font=("Arial", 11),
                         fg=self.text_color, bg=self.bg_color, selectcolor=self.bg_color,
                         activebackground=self.bg_color, activeforeground=self.text_color).pack(side=tk.LEFT, padx=5)
        
        # Word display
        self.word_display = tk.Text(self.main_frame, height=3, font=("Consolas", 28), 
                                  wrap=tk.WORD, padx=15, pady=15, bg="#1e1e1e", fg=self.text_color,
                                  insertbackground=self.text_color, selectbackground=self.highlight_color)
        self.word_display.pack(fill=tk.BOTH, expand=True, pady=20)
        self.word_display.tag_config("correct", foreground=self.accent_color)
        self.word_display.tag_config("wrong", foreground=self.error_color)
        self.word_display.config(state=tk.DISABLED)
        
        # Input field
        self.input_entry = tk.Entry(self.main_frame, font=("Consolas", 20), 
                                  bg="#1e1e1e", fg=self.text_color, insertbackground=self.text_color)
        self.input_entry.pack(fill=tk.X, pady=10, ipady=8)
        self.input_entry.bind("<KeyRelease>", self.check_input)
        
        # Stats frame
        self.stats_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.stats_frame.pack(fill=tk.X, pady=10)
        
        self.wpm_label = tk.Label(self.stats_frame, text="WPM: 0", font=("Arial", 12),
                                 fg=self.text_color, bg=self.bg_color)
        self.wpm_label.pack(side=tk.LEFT, padx=15)
        
        self.accuracy_label = tk.Label(self.stats_frame, text="Accuracy: 0%", font=("Arial", 12),
                                      fg=self.text_color, bg=self.bg_color)
        self.accuracy_label.pack(side=tk.LEFT, padx=15)
        
        self.time_label = tk.Label(self.stats_frame, text="Time Left: 60s", font=("Arial", 12),
                                  fg=self.text_color, bg=self.bg_color)
        self.time_label.pack(side=tk.LEFT, padx=15)
        
        self.words_label = tk.Label(self.stats_frame, text="Words: 0", font=("Arial", 12),
                                   fg=self.text_color, bg=self.bg_color)
        self.words_label.pack(side=tk.LEFT, padx=15)
        
        # Control buttons
        self.button_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.button_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.button_frame, text="Start Game", command=self.start_game,
                                    font=("Arial", 12), bg=self.accent_color, fg="white",
                                    activebackground="#3e8e41", activeforeground="white",
                                    relief=tk.FLAT, padx=20, pady=8)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_game,
                                    font=("Arial", 12), bg="#424242", fg="white",
                                    activebackground="#525252", activeforeground="white",
                                    relief=tk.FLAT, padx=20, pady=8)
        self.reset_button.pack(side=tk.LEFT, padx=10)
        
        # Initialize
        self.change_difficulty()
        self.toggle_mode()
        self.reset_game()
    
    def load_words(self):
        return {
            "easy": ["cat", "dog", "sun", "code", "game", "fun", "key", "map", "art", "joy"],
            "medium": ["python", "keyboard", "developer", "challenge", "practice",
                      "program", "typing", "speed", "accuracy", "skill"],
            "hard": ["algorithm", "asynchronous", "repository", "quintessential",
                    "extravaganza", "juxtaposition", "mnemonic", "paradigm",
                    "xylophone", "quasar"]
        }
    
    def toggle_mode(self):
        self.freestyle_mode = self.mode_var.get() == "freestyle"
        if self.freestyle_mode:
            self.time_frame.pack_forget()
            self.time_label.config(text="Practice Mode")
        else:
            self.time_frame.pack(pady=5)
            self.time_label.config(text=f"Time Left: {self.time_slider.get()}s")
    
    def change_difficulty(self):
        self.words = self.load_words()
    
    def start_game(self):
        if not self.game_active:
            self.game_active = True
            self.start_time = time.time()
            self.time_limit = self.time_slider.get()
            self.correct_chars = 0
            self.total_chars = 0
            self.completed_words = 0
            
            self.start_button.config(state=tk.DISABLED)
            self.input_entry.config(state=tk.NORMAL)
            self.input_entry.focus()
            
            if not self.freestyle_mode:
                self.update_timer()
            
            self.new_word()
    
    def update_timer(self):
        if self.game_active and not self.freestyle_mode:
            elapsed = time.time() - self.start_time
            remaining = max(0, self.time_limit - int(elapsed))
            self.time_label.config(text=f"Time Left: {remaining}s")
            
            # Update WPM
            if elapsed > 0:
                wpm = int((self.correct_chars / 5) / (elapsed / 60))
                self.wpm_label.config(text=f"WPM: {wpm}")
            
            # Check if time's up
            if remaining <= 0:
                self.end_game()
            else:
                self.root.after(1000, self.update_timer)
    
    def new_word(self):
        if self.game_active:
            word_list = self.words[self.difficulty.get()]
            self.current_word = random.choice(word_list)
            self.user_input = ""
            
            self.word_display.config(state=tk.NORMAL)
            self.word_display.delete(1.0, tk.END)
            self.word_display.insert(tk.END, self.current_word)
            self.word_display.config(state=tk.DISABLED)
            
            self.input_entry.delete(0, tk.END)
    
    def check_input(self, event):
        if not self.game_active:
            return
            
        self.user_input = self.input_entry.get()
        self.word_display.config(state=tk.NORMAL)
        self.word_display.delete(1.0, tk.END)
        
        correct = True
        for i, (input_char, word_char) in enumerate(zip(self.user_input, self.current_word)):
            if input_char == word_char:
                self.word_display.insert(tk.END, word_char, "correct")
                self.correct_chars += 1
            else:
                self.word_display.insert(tk.END, word_char, "wrong")
                correct = False
            self.total_chars += 1
        
        # Add remaining characters
        for char in self.current_word[len(self.user_input):]:
            self.word_display.insert(tk.END, char)
        
        self.word_display.config(state=tk.DISABLED)
        
        # Update stats
        if self.total_chars > 0:
            accuracy = int((self.correct_chars / self.total_chars) * 100)
            self.accuracy_label.config(text=f"Accuracy: {accuracy}%")
        
        # In freestyle mode, update WPM continuously
        if self.freestyle_mode:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                wpm = int((self.correct_chars / 5) / (elapsed / 60))
                self.wpm_label.config(text=f"WPM: {wpm}")
        
        # Check if word completed
        if self.user_input == self.current_word:
            self.completed_words += 1
            self.words_label.config(text=f"Words: {self.completed_words}")
            self.new_word()
    
    def end_game(self):
        self.game_active = False
        self.input_entry.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        
        # Calculate final stats
        elapsed = time.time() - self.start_time
        wpm = int((self.correct_chars / 5) / (elapsed / 60)) if elapsed > 0 else 0
        accuracy = int((self.correct_chars / self.total_chars) * 100) if self.total_chars > 0 else 0
        
        # Show results
        result_text = f"Game Over!\n\nWPM: {wpm}\nAccuracy: {accuracy}%\nWords: {self.completed_words}"
        if not self.freestyle_mode:
            result_text += f"\nTime: {self.time_limit} seconds"
        
        messagebox.showinfo("Results", result_text)
    
    def reset_game(self):
        self.game_active = False
        self.start_time = 0
        self.correct_chars = 0
        self.total_chars = 0
        self.completed_words = 0
        
        self.start_button.config(state=tk.NORMAL)
        self.input_entry.config(state=tk.NORMAL)
        self.input_entry.delete(0, tk.END)
        
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")
        self.words_label.config(text="Words: 0")
        
        if self.freestyle_mode:
            self.time_label.config(text="Practice Mode")
        else:
            self.time_label.config(text=f"Time Left: {self.time_slider.get()}s")
        
        self.word_display.config(state=tk.NORMAL)
        self.word_display.delete(1.0, tk.END)
        self.word_display.insert(tk.END, "Press Start to begin")
        self.word_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardTrainerGame(root)
    root.mainloop()
