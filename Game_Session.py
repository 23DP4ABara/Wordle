import random
import string

class GameSession:
    def __init__(self, hidden_word, max_tries, max_tips):
        self.hidden_word = hidden_word
        self.word_length = len(hidden_word)
        self.max_tries = max_tries
        self.max_tips = max_tips
        self.attempts = 0
        self.tips_used = 0
        self.history = []  
        self.guessed_letters = set()
        self.revealed_letters = set()
        self.is_won = False

    def make_guess(self, guess, valid_words, get_colored_feedback_str):
        if len(guess) != self.word_length or not guess.isalpha():
            return "Invalid guess. Enter a {}-letter word.".format(self.word_length)
        if guess not in valid_words:
            return "Word not in dictionary. Try another word."
        self.guessed_letters.update(guess)
        feedback_str = get_colored_feedback_str(guess, self.hidden_word)
        self.history.append(feedback_str)
        for i, letter in enumerate(guess):
            if letter == self.hidden_word[i]:
                self.revealed_letters.add(letter)
        self.attempts += 1
        if guess == self.hidden_word:
            self.is_won = True
        return feedback_str

    def can_use_tip(self):
        return self.tips_used < self.max_tips

    def use_tip(self):
        #Reveal a random unrevealed letter from the hidden word
        unrevealed = [c for c in set(self.hidden_word) if c not in self.revealed_letters]
        if unrevealed:
            hint = random.choice(unrevealed)
            self.revealed_letters.add(hint)
            self.tips_used += 1
            return hint
        return None

    def is_over(self):
        return self.is_won or self.attempts >= self.max_tries

    def get_status(self):
        return {
            "attempts": self.attempts,
            "max_tries": self.max_tries,
            "tips_used": self.tips_used,
            "max_tips": self.max_tips,
            "history": self.history,
            "guessed_letters": self.guessed_letters,
            "revealed_letters": self.revealed_letters,
            "is_won": self.is_won,
            "hidden_word": self.hidden_word if self.is_over() else None
        }