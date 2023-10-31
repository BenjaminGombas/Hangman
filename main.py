#!/usr/bin/env python
# Program name: midterm_hangman.py
"""
This program emulates a game of hangman by making use of tkinter and turtle. Tkinter is used to make a window with which
the player will interact with. Turtle is used to draw the hangman.
"""

# Libraries to be imported
# tkinter is a cool library that allows me to make buttons :3
import tkinter as tk
# turtle library to draw the hangedman
import turtle
# random to randomly choose a word
import random

# Global variables
# These variables are mostly ones that I don't want to pass to a function just to pass them to another function
# Attempts represents the number of wrong guesses a person can make before the game ends
attempts = 6
# Represents the turtle. Called hangman_drawer since all it does is draw the hanged man
hangman_drawer = turtle.Turtle()
# Will be a dictionary containing words from words.txt containing easy, medium and hard as keys and the values being the
# words from the file sorted by the length
word_lists = {"Easy": [], "Medium": [], "Hard": []}
# The randomly chosen word for the player to guess
word_to_guess = ""
# A list of letters the player has guessed
guessed_letters = []
# The current difficulty of the game. Default to Easy
current_difficulty = "Easy"
# In order to not pass labels and other tkinter elements to functions, I will initiate them here and use them as globals
# Because of this, most of these will have warnings like "Cannot find reference 'config' in 'None'" but it does not
# impact how the program functions
word_display_label = guess_entry = difficulty_var = difficulty_menu = guessed_letters_label = notification_label = None


# Functions
def read_words():
    """
    Reads words from the "words.txt" file and categorizes them into "easy," "medium," and "hard" based on word length.
    The words are stored in a dictionary, with the values being a list of words meeting that difficulty's length.
    """
    # Using the global keyword will allow for word_lists to be edited globally rather than just within this function
    global word_lists

    # Open the text file for reading
    with open('words.txt', 'r') as file:
        # Read words line by line
        for line in file:
            # Make sure there is no whitespace
            word = line.strip()

            # Determine the word length and add it to the appropriate list
            # If the word is 8 or more characters, add it to the hard list
            if len(word) >= 8:
                word_lists["Hard"].append(word)
            # If the word is 4-7 characters, add it to the medium list
            elif len(word) >= 4:
                word_lists["Medium"].append(word)
            # If the word is 1-3 characters, add it to the easy list
            elif len(word) >= 1:
                word_lists["Easy"].append(word)


def setup_labels(root):
    """
    Configure the gui elements of a Hangman game. It sets up labels, input field, and an option menu for displaying the
    word to guess, allowing letter input, showing guessed letters, providing notifications, and selecting the game's
    difficulty level

    :param root: Represents the window used for taking in text input and displaying information to the player
    """

    global word_display_label, guess_entry, difficulty_var, difficulty_menu, guessed_letters_label, notification_label

    # Create a label for the word display
    word_display_label = tk.Label(root, text="", font=("Arial", 24))
    # Pack() will automatically adjust the sizes of the labels and other gui elements and stack them vertically
    word_display_label.pack()

    # Create an entry widget for guessing letters
    guess_entry = tk.Entry(root, font=("Arial", 18))
    guess_entry.pack()
    # Start the entry widget as disabled until someone selects a difficulty
    guess_entry.config(state="disabled")

    # Create a label for guessed letters
    guessed_letters_label = tk.Label(root, text="", font=("Arial", 16))
    guessed_letters_label.pack()

    # Create a label for notifications
    notification_label = tk.Label(root, text="", fg='#f00', font=("Arial", 16))
    notification_label.pack()

    # Create a difficulty selection menu
    difficulty_var = tk.StringVar(root)
    difficulty_var.set("Choose a difficulty")

    difficulty_menu = tk.OptionMenu(root, difficulty_var, "Easy", "Medium", "Hard")
    difficulty_menu.pack()

    # Create a button to change difficulty
    difficulty_button = tk.Button(root, text="Change Difficulty", command=lambda: change_difficulty())
    difficulty_button.pack()


def update_word_display():
    """
    Update the word display label. This is where the letters (or blanks) of the word that must be guessed will be
    displayed
    """
    # Display will be a string that will be used to display the player's progress towards guessing the word
    display = ""

    # Loop through the letters of the word
    for letter in word_to_guess:
        # If the word has a letter that has been guessed, display it
        if letter in guessed_letters:
            display += letter + " "
        # If the letter has not been guessed, display a _ instead
        else:
            display += "_ "
    # Set the text of the label to the display string
    word_display_label.config(text=display)


def guess_letter():
    """
    This function takes in the player's guess and checks to see if the input is valid. If the input is not valid, a
    proper notification will be displayed. If the input is valid, see if the guess is correct. If correct, decrease the
    number of attempts remaining by 1 and draw a portion of the hangman
    """
    # Using the global keyword will allow for attempts to be edited globally rather than just within this function
    global attempts

    # Convert the player's guess to uppercase
    guess = guess_entry.get().upper()

    # Clear the entry box
    guess_entry.delete(0, "end")

    # Make sure the player's guess is a letter and just 1 letter
    if guess.isalpha() and len(guess) == 1:
        # Make sure the letter has not been guessed yet by seeing if the letter is in guessed_letters
        if guess not in guessed_letters:
            # At this point, the guess has been accepted as valid
            # Make sure no notifications are showing in the notification label
            notification_label.config(text="")

            # Add the guess to the list of guessed letters
            guessed_letters.append(guess)

            # Check to see if the word contains the player's guess
            if guess not in word_to_guess:
                # Decrease the number of attempts left by 1
                attempts -= 1

                # Draw the next portion of the hanged man
                draw_hangman()

            # Update the word display to include this guess
            update_word_display()
            # Update the guessed letters display to include the guess
            guessed_letters_label.config(text=f"Guessed letters: {' '.join(guessed_letters)}")

            # Check to see if the game is over
            check_game_over()

        # If the letter has been guessed already, the player needs to be told
        else:
            # Edit the notification label to let the player know they guessed the letter already
            notification_label.config(text="You already guessed that letter.")
    # If the entry is not a valid input (is not a single letter), the player needs to be told
    else:
        # Edit the notification label to let the player know guesses must be only a single letter
        notification_label.config(text="Please enter a single letter.")


def change_difficulty():
    """
    Due changing the difficulty of the game having the same functionality as resetting the game, this function will serve
    as both. This function will reset the game state to its original state and change the difficulty when needed.
    """
    # Using the global keyword will allow for these variable to be edited globally rather than just within this function
    global attempts, current_difficulty, word_to_guess, guessed_letters

    # The difficulty var starts as "Choose a difficulty" so we need to make sure its not that
    # If difficulty_var is not equal to "Choose a difficulty", set the current difficulty to that difficulty. Otherwise,
    # set the current difficulty to easy
    current_difficulty = difficulty_var.get() if difficulty_var.get() != "Choose a difficulty" else "Easy"

    # Clear the list of guessed letters
    guessed_letters.clear()

    # Clear any text that the labels may contain
    guessed_letters_label.config(text="")
    notification_label.config(text="")

    # Choose a new random word and cast it to uppercase
    word_to_guess = random.choice(word_lists[current_difficulty]).upper()
    # Update the word label to fit the new word
    update_word_display()
    print(word_to_guess)

    # Set remaining attempts back to its starting value (6)
    attempts = 6

    # Clear the hangman drawing
    hangman_drawer.clear()

    # Redraw the gallow image and put the turtle back in starting position
    draw_hangman()

    # Enable the guess entry widget
    guess_entry.config(state="normal")


def draw_hangman():
    """
    This function draws the hangman using turtle based on how many attempts are remaining
    """
    # This function is only called if 6 attempts remain when restarting the game
    if attempts == 6:
        # Add the gallow to the turtle window
        turtle.Screen().bgpic("gallow.gif")
        hangman_drawer.penup()
        hangman_drawer.goto(40, 90)
        # Use turtle's set heading to always point towards the left at the start of drawing the hangman.
        # Using left/right 180 would cause the circle/head to be drawn upwards instead of downwards every other reset
        hangman_drawer.seth(180)
    # Draw the head
    elif attempts == 5:
        hangman_drawer.pendown()
        hangman_drawer.circle(20)
    # Draw the body
    elif attempts == 4:
        hangman_drawer.penup()
        hangman_drawer.goto(40, 50)
        hangman_drawer.seth(270)
        hangman_drawer.pendown()
        hangman_drawer.forward(100)
    # Draw the left arm
    elif attempts == 3:
        hangman_drawer.penup()
        hangman_drawer.goto(40, 30)
        hangman_drawer.seth(225)
        hangman_drawer.pendown()
        hangman_drawer.forward(35)
    # Draw the right arm
    elif attempts == 2:
        hangman_drawer.penup()
        hangman_drawer.goto(40, 30)
        hangman_drawer.seth(315)
        hangman_drawer.pendown()
        hangman_drawer.forward(35)
    # Draw the right leg
    elif attempts == 1:
        hangman_drawer.penup()
        hangman_drawer.goto(40, -50)
        hangman_drawer.pendown()
        hangman_drawer.forward(30)
    # Draw the left leg
    elif attempts == 0:
        hangman_drawer.penup()
        hangman_drawer.goto(40, -50)
        hangman_drawer.seth(225)
        hangman_drawer.pendown()
        hangman_drawer.forward(30)


def check_game_over():
    """
    This function checks to see if the game is over, whether because the player won or because they ran out of lives
    """
    # If there are no attempts remaining, end the game
    if attempts == 0:
        # Display a notification that the game is over and prompt the player to play again
        word_display_label.config(text=f"You lost! The word was: {word_to_guess}\nChoose a difficulty to play again!")

        # Disable the entry box to prevent the player from entering more letters in after the game has ended
        guess_entry.config(state="disabled")
    # If there are no more blanks in the word label, that means the user has guessed all of the letters in the word
    elif "_" not in word_display_label["text"]:
        # Display a notification that the player guessed the word and prompt the player to play again
        word_display_label.config(
            text=f"Congratulations! You guessed the word: {word_to_guess}\nChoose a difficulty to play again!"
        )

        # Disable the entry box to prevent the player from entering more letters in after the game has ended
        guess_entry.config(state="disabled")


# Program Starts Here
# main()
def main():
    """
    Start the hangman game. Begin by modifying settings of the turtle. Then, create a tkinter window to use as the GUI.
    Read the words from word.txt. Set up the labels and other widgets for the GUI. Bind the enter key to the
    guess_letter function and use root.mainloop() to keep the game running until the user closes the game.
    """
    # Initialize some turtle settings
    # I think pensize 5 looks the best when drawing the hangman
    hangman_drawer.pensize(5)
    # Hide the turtle icon
    hangman_drawer.hideturtle()

    # Initialize the guessing window
    root = tk.Tk()
    root.title("Hangman")

    # Load the words from words.txt
    read_words()

    # Initialize all of the labels and other Tkinter widgets
    setup_labels(root)

    # Bind the guess_letter function to the enter key
    guess_entry.bind("<Return>", lambda event: guess_letter())

    # root.mainloop() will keep the input window open until the player closes it
    root.mainloop()


# ===============================
# No extra Code beyond this point
if __name__ == '__main__':
    main()
# EOF #
