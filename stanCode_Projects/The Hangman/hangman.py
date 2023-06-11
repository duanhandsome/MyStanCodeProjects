"""
File: hangman.py
Name: Duan
-----------------------------
This program plays hangman game.
Users see a dashed word, trying to
correctly figure the un-dashed word out
by inputting one character each round.
If the user input is correct, show the
updated word on console. Players have N_TURNS
chances to try and win this game.
"""


import random


# This constant controls the number of guess the player has.
N_TURNS = 7


def main():
    """
    This program plays hangman game.
    1. Users have N_TURNS chances to guess the right answer.
    2. The program will warn the user if they key in double alphabet or other symbols aside from alphabet.
    """
    ans = ""
    rdm_word = random_word()                        # Choose a random word
    tries = N_TURNS
    for i in range(len(rdm_word)):                  # initial answer == "-------"
        ans += "-"
    print("The word looks like " + ans)
    print("You have " + str(tries) + " wrong guesses left.")
    while tries > 0:                               # To see if the number of guesses has been used completely
        guess = input("Your guess: ")
        if guess.isalpha() and len(guess) == 1:     # To check if users enters the wrong format()
            new_ans = ""
            if guess.upper() in rdm_word:
                # If the user guess a right alphabet, form a new hint like ----H--
                for i in range(len(rdm_word)):
                    if rdm_word[i] == guess.upper():
                        new_ans += rdm_word[i]
                    else:
                        new_ans += ans[i]
                ans = new_ans
                print("You are correct!")
                # To check if user get the correct answer
                if ans == rdm_word:
                    print("You win!!")
                    print("The word was " + rdm_word)
                    break
                else:
                    print("The word looks like " + ans)
                    print("You have " + str(tries) + " wrong guesses left.")
            else:
                tries -= 1
                print("There is no " + str(guess).upper() + "'s in the word.")
                # To check if the user has used all the guesses
                if tries == 0:
                    print("You are completely hung : (")
                    print("The word was " + rdm_word)
                    break
                else:
                    print("The word looks like " + ans)
                    print("You have " + str(tries) + " wrong guesses left.")
        else:
            print("Illegal format.")


def random_word():
    """
    This function chooses a random word
    """
    num = random.choice(range(9))
    if num == 0:
        return "NOTORIOUS"
    elif num == 1:
        return "GLAMOROUS"
    elif num == 2:
        return "CAUTIOUS"
    elif num == 3:
        return "DEMOCRACY"
    elif num == 4:
        return "BOYCOTT"
    elif num == 5:
        return "ENTHUSIASTIC"
    elif num == 6:
        return "HOSPITALITY"
    elif num == 7:
        return "BUNDLE"
    elif num == 8:
        return "REFUND"


# DO NOT EDIT CODE BELOW THIS LINE #

if __name__ == '__main__':
    main()
