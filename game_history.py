import datetime

class GameHistory:
    def __init__(self, filename="game_history.txt"):
        self.filename = filename

    def save_result(self, word, won, attempts, max_attempts, tips_used, max_tips):

        #Save the result of a game to the history file.

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = "WON" if won else "LOST"
        line = (
            f"{now} | Word: {word.upper()} | Result: {result} | "
            f"Attempts: {attempts}/{max_attempts} | Tips: {tips_used}/{max_tips}\n"
        )
        with open(self.filename, "a") as file:
            file.write(line)

    def get_history(self):

        #Return all saved game results as a list of strings.

        try:
            with open(self.filename, "r") as file:
                return file.readlines()
        except FileNotFoundError:
            return []