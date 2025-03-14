


from flask import Flask, render_template, request, redirect, url_for
from rich.console import Console
from rich.table import Table
import random


app = Flask(__name__)
console = Console()

def get_random_word(file_path):
    try:
        with open(file_path, 'r') as file:
            words = [word.strip() for word in file if len(word.strip()) == 5]
        if words:
            return random.choice(words)
        else:
            print("No 5-letter words found.")
            return None
    except FileNotFoundError:
        print("File not found.")
        return None

word_to_guess = get_random_word("words\words_alpha.txt")



correct_guesses = set()
remaining_chances = 5


def Displayed_word(word, correct_guess):
    Display_word = ""
    for letter in word:
        Display_word += letter
    else:
        Display_word += "_"
        return Display_word
    
def Guess(word, guess, correct_guess):
    if guess.lower() ==word.lower():
        correct_guess.update(word)
        return True
    return False