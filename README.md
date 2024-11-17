# Python Wordle Desktop Game

A desktop implementation of the popular word-guessing game Wordle, built with Python and Tkinter.

![Wordle Game Screenshot](screenshot.png)

## Features

- 🎮 Complete Wordle gameplay mechanics
- 🎨 Dark mode interface
- ⌨️ Virtual keyboard with visual feedback
- 🖱️ Mouse and keyboard input support
- 📊 Statistics tracking
- 💾 Local save system
- 🔄 Play again functionality
- ✅ Word validation

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-wordle.git
2. Navigate to the project directory:
    cd python-wordle

3. Run the game:
    python wordle.py
   
**How to Play**

  -Try to guess the five-letter word
  -Type your guess using your keyboard or click the on-screen keyboard
  -Press Enter to submit your guess
  -After each guess, the colors will indicate:

🟩 Green: Letter is correct and in the right position
🟨 Yellow: Letter is in the word but in the wrong position
⬜ Gray: Letter is not in the word


You have 6 attempts to guess the word correctly

Features in Detail
Statistics Tracking

Games played
-Win percentage
-Current streak
-Maximum streak
-All statistics are automatically saved between sessions

Word Validation
  Built-in dictionary of valid words
  Invalid words are rejected with a warning message

Keyboard Support  
  Use your physical keyboard to type
  On-screen keyboard support for mouse input
  Backspace to delete letters
  Enter to submit guess

Contributing
  Contributions are welcome! Please feel free to submit a Pull Request.
License
  This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
  
  Inspired by the original Wordle game
  Built with Python and Tkinter
