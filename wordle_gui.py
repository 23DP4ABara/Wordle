import tkinter as tk
from tkinter import messagebox
from Game_Session import GameSession
from game_history import GameHistory
import random

WORD_FILE = "words/words_alpha.txt"

def load_words(filepath, word_length):
    with open(filepath, 'r') as file:
        return [w.strip().lower() for w in file if len(w.strip()) == word_length and w.strip().isalpha()]

class WordleGUI:
    def __init__(self, master):
        self.master = master
        master.title("Wordle GUI")

        self.tip_label = None

        #Settings Frame
        self.settings_frame = tk.Frame(master)
        self.settings_frame.pack(pady=10)

        tk.Label(self.settings_frame, text="Word Length:").grid(row=0, column=0)
        self.word_length_var = tk.IntVar(value=5)
        tk.Entry(self.settings_frame, textvariable=self.word_length_var, width=5).grid(row=0, column=1)

        tk.Label(self.settings_frame, text="Max Tries:").grid(row=0, column=2)
        self.max_tries_var = tk.IntVar(value=6)
        tk.Entry(self.settings_frame, textvariable=self.max_tries_var, width=5).grid(row=0, column=3)

        tk.Label(self.settings_frame, text="Max Tips:").grid(row=0, column=4)
        self.max_tips_var = tk.IntVar(value=2)
        tk.Entry(self.settings_frame, textvariable=self.max_tips_var, width=5).grid(row=0, column=5)

        self.start_button = tk.Button(self.settings_frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=0, column=6, padx=10)

        #Game Widgets 
        self.letter_entries = []
        self.guess_button = None
        self.tip_button = None
        self.output = None
        self.status = None
        self.answer_label = None
        self.alphabet_frame = None

        #Game State
        self.words = []
        self.hidden_word = ""
        self.session = None
        self.history = None

    def start_game(self):
        word_length = self.word_length_var.get()
        max_tries = self.max_tries_var.get()
        max_tips = self.max_tips_var.get()

        self.words = load_words(WORD_FILE, word_length)
        print(f"Loaded {len(self.words)} words of length {word_length}")
        print(f"First 10 loaded words: {self.words[:10]}")
        if not self.words:
            messagebox.showerror("Error", f"No words of length {word_length} found.")
            return

        self.hidden_word = random.choice(self.words)
        print(f"Chosen word: {self.hidden_word}")
        assert self.hidden_word in self.words, f"Chosen word {self.hidden_word} not in loaded words list!"

        self.session = GameSession(self.hidden_word, max_tries, max_tips)
        self.history = GameHistory()  # <-- Make sure this line is present!

        #Remove settings widgets
        self.settings_frame.pack_forget()

        #Game Frame
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack()

        self.label = tk.Label(self.game_frame, text=f"Guess the {word_length}-letter word!")
        self.label.pack()

        #Letter Entry Spaces
        self.letter_entries = []
        entry_frame = tk.Frame(self.game_frame)
        entry_frame.pack(pady=10)
        for i in range(word_length):
            e = tk.Entry(entry_frame, width=2, font=("Arial", 20, "bold"), justify="center")
            e.pack(side=tk.LEFT, padx=2)
            e.bind("<KeyRelease>", lambda event, idx=i: self.focus_next_entry(event, idx))
            self.letter_entries.append(e)
        self.letter_entries[0].focus_set()

        #Buttons Frame
        self.buttons_frame = tk.Frame(self.game_frame)
        self.buttons_frame.pack(pady=5)

        self.guess_button = tk.Button(self.buttons_frame, text="Guess", command=self.make_guess)
        self.guess_button.pack(side=tk.LEFT, padx=5)

        self.tip_button = tk.Button(self.buttons_frame, text="Tip", command=self.use_tip)
        self.tip_button.pack(side=tk.LEFT, padx=5)

        #Output for result
        self.output = tk.Label(self.game_frame, text="", font=("Arial", 16), justify="center")
        self.output.pack(pady=10)

        self.status = tk.Label(self.game_frame, text=f"Tries left: {max_tries}")
        self.status.pack()

        #Tip display
        self.tip_label = tk.Label(self.game_frame, text="", font=("Arial", 14), fg="blue")
        self.tip_label.pack()

        #Alphabet display
        self.alphabet_frame = tk.Frame(self.game_frame)
        self.alphabet_frame.pack(pady=5)
        self.update_alphabet_display()

    def focus_next_entry(self, event, idx):
        #Move to next entry on letter input, or previous on backspace
        if event.keysym == "BackSpace":
            if idx > 0 and not self.letter_entries[idx].get():
                self.letter_entries[idx-1].focus_set()
        elif len(self.letter_entries[idx].get()) == 1 and idx < len(self.letter_entries)-1:
            self.letter_entries[idx+1].focus_set()

    def make_guess(self, event=None):
        guess = ''.join(e.get().lower() for e in self.letter_entries)
        feedback = self.session.make_guess(guess, self.words, self.get_colored_feedback_str)
        self.status.config(text=f"Tries left: {self.session.max_tries - self.session.attempts}")
        self.update_alphabet_display()
        #Show feedback 
        if isinstance(feedback, str) and (feedback.startswith("Invalid") or feedback.startswith("Word not in dictionary")):
            self.output.config(text=feedback, fg="red")
            return
        #Show colored feedback
        self.show_colored_feedback(None)
        if self.session.is_won:
            messagebox.showinfo("Wordle", f"Congratulations! The word was {self.hidden_word.upper()}")
            self.history.save_result(self.hidden_word, True, self.session.attempts, self.session.max_tries, self.session.tips_used, self.session.max_tips)
            self.master.quit()
        elif self.session.is_over():
            messagebox.showinfo("Wordle", f"Game Over! The word was {self.hidden_word.upper()}")
            self.history.save_result(self.hidden_word, False, self.session.attempts, self.session.max_tries, self.session.tips_used, self.session.max_tips)
            self.master.quit()

    def show_colored_feedback(self, _):
        #Remove previous widgets
        for widget in self.output.winfo_children():
            widget.destroy()
        #Show all feedbacks in history
        for feedback in self.session.history:
            frame = tk.Frame(self.output)
            frame.pack()
            for letter, color in feedback:
                lbl = tk.Label(frame, text=letter, fg="white", bg=color, width=2, font=("Arial", 16, "bold"))
                lbl.pack(side=tk.LEFT, padx=2)
        self.output.config(text="")  

    def use_tip(self):
        if self.session.can_use_tip():
            hint = self.session.use_tip()
            if hint:
                self.tip_label.config(text=f"Tip: The letter '{hint.upper()}' is in the word.")
            else:
                self.tip_label.config(text="No more hints available.")
        else:
            self.tip_label.config(text="No more tips left.")

    def get_colored_feedback_str(self, guess, hidden_word):
        feedback = []
        used = [False] * len(hidden_word)
        #First pass: correct position (green)
        for i, c in enumerate(guess):
            if i < len(hidden_word) and c == hidden_word[i]:
                feedback.append((c.upper(), "green"))
                used[i] = True
            else:
                feedback.append(None)
        #Second pass: present but wrong position (yellow) or absent (gray)
        for i, c in enumerate(guess):
            if feedback[i] is not None:
                continue
            found = False
            for j, hc in enumerate(hidden_word):
                if not used[j] and c == hc:
                    found = True
                    used[j] = True
                    break
            if found:
                feedback[i] = (c.upper(), "gold")
            else:
                feedback[i] = (c.upper(), "gray")
        return feedback

    def update_alphabet_display(self):
        #Clear previous
        for widget in self.alphabet_frame.winfo_children():
            widget.destroy()
        guessed = self.session.guessed_letters if self.session else set()
        for letter in "abcdefghijklmnopqrstuvwxyz":
            color = "gray" if letter in guessed else "black"
            lbl = tk.Label(self.alphabet_frame, text=letter.upper(), fg=color, font=("Arial", 10, "bold"))
            lbl.pack(side=tk.LEFT, padx=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()