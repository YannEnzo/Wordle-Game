import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
from pathlib import Path


class WordleGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Wordle")
        self.window.configure(bg='#121213')
        self.window.resizable(False, False)

        # Game variables
        self.current_row = 0
        self.current_col = 0
        self.word_list = [
            "APPLE", "BEACH", "CHAIR", "DANCE", "EARTH", "FLAME", "GRAPE", "HEART",
            "IMAGE", "JUICE", "KNIFE", "LEMON", "MOUSE", "NIGHT", "OCEAN", "PEACE",
            "QUEEN", "RIVER", "SMILE", "TABLE", "UNITY", "VOICE", "WORLD", "YOUTH",
            "BREAD", "CLOCK", "DREAM", "EAGLE", "FLASH", "GREEN", "HAPPY", "IVORY",
            "JUMBO", "KOALA", "LASER", "MAGIC", "NOBLE", "OLIVE", "PIANO", "QUILT",
            "RADIO", "SNAKE", "TIGER", "URBAN", "VIRUS", "WHALE", "XEROX", "YACHT"
        ]
        self.target_word = random.choice(self.word_list)
        self.game_over = False
        
        # Statistics
        self.stats = self.load_statistics()
        
        # GUI Setup
        self.setup_gui()
        
    def load_statistics(self):
        try:
            stats_file = Path("wordle_stats.json")
            if stats_file.exists():
                with open(stats_file, "r") as f:
                    return json.load(f)
            else:
                return {"games_played": 0, "games_won": 0, "current_streak": 0, "max_streak": 0}
        except Exception:
            return {"games_played": 0, "games_won": 0, "current_streak": 0, "max_streak": 0}

    def save_statistics(self):
        with open("wordle_stats.json", "w") as f:
            json.dump(self.stats, f)

    def setup_gui(self):
        # Create main frame
        self.main_frame = tk.Frame(self.window, bg='#121213')
        self.main_frame.pack(padx=20, pady=20)

        # Title
        title_label = tk.Label(self.main_frame, text="WORDLE", font=('Helvetica', 24, 'bold'),
                             fg='white', bg='#121213')
        title_label.pack(pady=(0, 20))

        # Create grid frame
        self.grid_frame = tk.Frame(self.main_frame, bg='#121213')
        self.grid_frame.pack()

        # Create grid of letter boxes
        self.letter_boxes = []
        for i in range(6):
            row = []
            for j in range(5):
                box = tk.Label(self.grid_frame, width=4, height=2,
                             relief='solid', font=('Helvetica', 20, 'bold'),
                             bg='#121213', fg='white')
                box.grid(row=i, column=j, padx=2, pady=2)
                row.append(box)
            self.letter_boxes.append(row)

        # Create keyboard frame
        self.keyboard_frame = tk.Frame(self.main_frame, bg='#121213')
        self.keyboard_frame.pack(pady=20)

        # Keyboard layout
        keyboard_layout = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫']
        ]

        # Create keyboard buttons
        self.key_buttons = {}
        for i, row in enumerate(keyboard_layout):
            frame = tk.Frame(self.keyboard_frame, bg='#121213')
            frame.pack(pady=2)
            for letter in row:
                if letter in ['ENTER', '⌫']:
                    width = 8
                else:
                    width = 4
                btn = tk.Button(frame, text=letter, width=width, height=2,
                              font=('Helvetica', 10, 'bold'),
                              command=lambda l=letter: self.handle_key_press(l),
                              bg='#818384', fg='white')
                btn.pack(side=tk.LEFT, padx=2)
                self.key_buttons[letter] = btn

        # Bind keyboard events
        self.window.bind('<Key>', self.handle_keyboard_input)
        self.window.bind('<Return>', lambda e: self.handle_key_press('ENTER'))
        self.window.bind('<BackSpace>', lambda e: self.handle_key_press('⌫'))

    def handle_keyboard_input(self, event):
        if not self.game_over:
            key = event.char.upper()
            if key.isalpha() and len(key) == 1:
                self.handle_key_press(key)

    def handle_key_press(self, key):
        if self.game_over:
            return

        if key == '⌫':
            if self.current_col > 0:
                self.current_col -= 1
                self.letter_boxes[self.current_row][self.current_col].config(text='')
        elif key == 'ENTER':
            if self.current_col == 5:
                self.check_word()
        elif key.isalpha() and self.current_col < 5:
            self.letter_boxes[self.current_row][self.current_col].config(text=key)
            self.current_col += 1

    def check_word(self):
        guess = ''.join(box.cget('text') for box in self.letter_boxes[self.current_row])
        if guess not in self.word_list:
            messagebox.showwarning("Invalid Word", "Word not in list!")
            return

        # Check letters
        for i, (guess_letter, target_letter) in enumerate(zip(guess, self.target_word)):
            box = self.letter_boxes[self.current_row][i]
            key_button = self.key_buttons.get(guess_letter)
            
            if guess_letter == target_letter:
                box.config(bg='#538d4e')  # Green
                if key_button:
                    key_button.config(bg='#538d4e')
            elif guess_letter in self.target_word:
                box.config(bg='#b59f3b')  # Yellow
                if key_button and key_button.cget('bg') != '#538d4e':
                    key_button.config(bg='#b59f3b')
            else:
                box.config(bg='#3a3a3c')  # Gray
                if key_button and key_button.cget('bg') not in ['#538d4e', '#b59f3b']:
                    key_button.config(bg='#3a3a3c')

        if guess == self.target_word:
            self.game_over = True
            self.update_statistics(won=True)
            messagebox.showinfo("Congratulations!", f"You won! The word was {self.target_word}")
            self.show_play_again()
        elif self.current_row == 5:
            self.game_over = True
            self.update_statistics(won=False)
            messagebox.showinfo("Game Over", f"You lost! The word was {self.target_word}")
            self.show_play_again()
        else:
            self.current_row += 1
            self.current_col = 0

    def update_statistics(self, won):
        self.stats["games_played"] += 1
        if won:
            self.stats["games_won"] += 1
            self.stats["current_streak"] += 1
            self.stats["max_streak"] = max(self.stats["max_streak"], self.stats["current_streak"])
        else:
            self.stats["current_streak"] = 0
        self.save_statistics()

    def show_play_again(self):
        play_again = messagebox.askyesno("Play Again", "Would you like to play again?")
        if play_again:
            self.reset_game()
        else:
            self.window.quit()

    def reset_game(self):
        # Reset game variables
        self.current_row = 0
        self.current_col = 0
        self.target_word = random.choice(self.word_list)
        self.game_over = False

        # Reset GUI
        for row in self.letter_boxes:
            for box in row:
                box.config(text='', bg='#121213')

        # Reset keyboard
        for button in self.key_buttons.values():
            button.config(bg='#818384')

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = WordleGame()
    game.run()
