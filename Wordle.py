import tkinter as tk
from wordle_gui import WordleGUI  
if __name__ == "__main__":
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()