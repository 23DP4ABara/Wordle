


from flask import Flask, render_template, request, redirect, url_for
from rich.console import Console
from rich.table import Table
import random


app = Flask(__name__)
console = Console()

def select_random_word(file_path):
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

word_to_guess = select_random_word("C:\Users\A230556AB\Desktop\wordle\words\words_alpha.txt")
print("Word to guess:", word_to_guess)


correct_guesses = set()
remaining_chances = 5
