# Carson Redlich and Maison Carheel
# May 3rd, 2026

# Imports
import random
from graphics import *


#                                 ------- GAME FUNCTIONS -------
# Load text file, handle if the words.txt file isn't found
def load_words():
    try:
       with open('words.txt') as file:
           content = file.read()
           words = content.strip().split()
           return words
    except FileNotFoundError:
       print("File 'words.txt' is not found.")
       game_active = False
       return game_active


# Computer chooses random word from file
def pick_word():
   word_list = load_words()
   return random.choice(word_list)

# Hides the word from the user's view
def hide_word():
   word = pick_word().lower()
   hidden_word = []
   for i in range(len(word)):
       hidden_word.append("_")
   return word, hidden_word

# Checks if the user wants to restart the game
def check_restart():
   restart = input("\nWould you like to restart the game (Y/N): ").lower()
   if restart == "y":
       return True
   else:
       return False

# Clears/resets all variables and generates a new word
def restart_game():
   global word, guessed_word, guesses, guessed_letters
   word, guessed_word = hide_word()
   guesses = 6
   guessed_letters = []

def display_menu():
   print("Welcome to the Word Guessing Game. You have 6 attempts to choose the right word by guessing "
         "ONE letter each attempt.\nOnce the hangman is drawn, it is game over.")

# Graphics that will display when user losses
def graphics_lose():
# Creating the graphics window, setting background to black, making image display bottom right corner.
    win = GraphWin("Lose", 400, 400)
    win.setBackground("black")
    win.master.geometry("+1100+500")

# Test size, location, color, and display You Lost.
    lose_message = Text(Point(200, 200), "You Lost")
    lose_message.setSize(36)
    lose_message.setTextColor("red")

# Display the message and allow it to show till user closes it.
    lose_message.draw(win)
    win.getMouse()
    win.close()

# Graphics that will display when user wins
def graphics_win():
    # Creating the graphics window, setting background to black, making image display bottom right corner.
    win = GraphWin("Win", 400, 400)
    win.setBackground("pink")
    # win.master.geometry("+1100+500")

    # Test size, location, color, and display You Won.
    win_message = Text(Point(200, 200), "You Won")
    win_message.setSize(36)
    win_message.setTextColor("white")

    # Display the message and allow it to show till user closes it.
    win_message.draw(win)
    win.getMouse()
    win.close()


#                                 ------- MAIN FUNCTION --------
def main():
   global guesses

   # Print the guessing display
   print(f"\n{guessed_word}")
   print(f"Wrong Attempts: {guesses}")
   # Print the guessed letters if the user guessed any
   if len(guessed_letters) > 0:
       print(f"Guesses Letters: {guessed_letters}")

   # Check if the guess is a letter
   while True:
       try:
           guess = str(input("Guess: ")).lower()
           if guess.isalpha() == True and len(guess) > 1:
               print("Please type only one letter.")
           elif guess.isalpha():
               break
           else:
               print("Please type a letter.")
       except ValueError:
           print("Please type a valid letter")

   # Check if the guess is in the word
   if guess in word:
       # Check if the letter was already guessed
       if guess in guessed_letters:
           print("This letter was already guessed")
       else:
           # Add the letter to the display based on its position the word
           print(f"The letter {guess} was in the word.")
           for i in range(len(word)):
               if word[i] == guess:
                   guessed_word[i] = guess
   # Check if the guess isn't in the word
   elif guess is not word:
       print(f"{guess} was not in the word.")
       # Remove the available incorrect guesses
       guesses -= 1
       # Print the hangman
       if guesses < 6:
           print(f"\n{hangman[6 - guesses]}")

   # Add the letter to the guessed letters if it wasn't already guessed
   if guess not in guessed_letters:
       guessed_letters.append(guess)

   # Check if the user won
   if guessed_word == list(word):
       print(f"\nYou Win! The character was {word.capitalize()}\nClick on the win screen to continue.")
       # Open the graphics window
       graphics_win()

       # Check if the user wants to restart the game
       restart = check_restart()
       if restart:
           restart_game()
           return True
       elif not restart:
           return False
       return None

   # Check if the user lost
   elif guesses == 0:
       print(f"\nGame Over! The character was {word.capitalize()}\nClick on the loss screen to continue.")
       # Open the graphics window
       graphics_lose()

       # Check if the user wants to restart the game
       restart = check_restart()
       if restart:
           restart_game()
           return True
       elif not restart:
           return False
       return None
   # Game is still running
   else:
       return True


#                         ------- VARIABLES -------=
# All the states the hangman can be in
hangman = ["",
          " O",
          " O\n |",
          " O\n/|",
          " O\n/|\\",
          " O\n/|\\\n/",
          " O\n/|\\\n/ \\\n",]

# Check if the P5R.txt file exists, if so continue the code
game_active = load_words()
if game_active:
    # Create the main game variables
    word, guessed_word = hide_word()
    guesses = 6
    guessed_letters = []


    #                         ------- GAME LOOP -------
    # Welcome message
    display_menu()
    # Game loop
    while game_active:
       game_active = main()

# Print a terminating message once the loop ends
print("Thanks for playing! Program Terminating.")

