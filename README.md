# Wordle

**Wordle** is a word guessing game, made using graphical (GUI) interfaces. Your goal is to guess the hidden word within a limited number of attempts. Before the game starts, you can customize three settings: the number of guesses, the number of hints (tips), and the length of the word to guess. The game uses a dictionary text file to validate guesses.

## How to Play

- After each guess:
  - If a letter is in the correct position, it is shown in **green**.
  - If a letter is in the word but in the wrong position, it is shown in **yellow**.
  - If a letter is not in the word, it is shown in **gray**.

- You can use a tip (hint) by clicking the "Tip" button. Hints will reveal a letter in the word that hasn't already been revealed as green or yellow. If there are no more unrevealed letters, the game will notify you in the tip area.

- The game continues until you guess the word or run out of attempts. At the end, the correct word is displayed if you didn't guess it.

- Game history is saved to `game_history.txt` after each game, including the word, result, attempts, and tips used.

## Requirements

- Python 3.x
- Tkinter (Included with Python)

## Dictionary

The game uses `words/words_alpha.txt` as its dictionary. You can replace this file with any word list you prefer.

---

Enjoy playing!






