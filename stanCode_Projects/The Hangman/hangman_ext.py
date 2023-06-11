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
    3. The program will deploy a picture of a hangman.
    """
    ans = ""
    rdm_word = random_word()
    tries = N_TURNS
    # initial answer == "-------"
    for i in range(len(rdm_word)):
        ans += "-"
    print(image_hangman(N_TURNS - tries))
    print("You have total of " + str(tries) + " guesses.")
    while tries > 0:                               # To see if the number of guesses has been used completely
        guess = input("Your guess: ")
        # To check if users enters the wrong format
        if guess.isalpha() and len(guess) == 1:
            new_ans = ""
            if guess.upper() in rdm_word:
                for i in range(len(rdm_word)):
                    if rdm_word[i] == guess.upper():
                        new_ans += rdm_word[i]
                    else:
                        new_ans += ans[i]
                ans = new_ans
                print(image_hangman(N_TURNS - tries))
                # To check if the user gets the correct answer
                if ans == rdm_word:
                    print("You win!!")
                    print("The word was " + rdm_word)
                    break
                else:
                    print("The word looks like " + ans)
            else:
                tries -= 1
                # Completely using the number of guesses
                if tries == 0:
                    print(image_hangman(N_TURNS - tries))
                    print("You are completely hung : (")
                    print("The word was " + rdm_word)
                    break
                else:
                    print(image_hangman(N_TURNS - tries))
                    print("The word looks like " + ans)
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


def image_hangman(tries):
    """
    This function plots every possible condition of the hangman!
    """
    pictures = ["""
                   ------
                   |    
                   |    
                   |   
                   |   
                   |
                """,
                """
                   ------
                   |    |
                   |    
                   |   
                   |   
                   |
                """,
                """
                   ------
                   |    |
                   |    o
                   |   
                   |    
                   |
                """,
                """
                   ------
                   |    |
                   |    o
                   |    |
                   |      
                   |
                """,
                """
                   ------
                   |    |
                   |    o
                   |   /|
                   |     
                   |
                """,
                """
                   ------
                   |    |
                   |    o
                   |   /|\\
                   |      
                   |     
                """,
                """
                   ------
                   |    |
                   |    o
                   |   /|\\
                   |   / 
                   |     
                """,
                """
                   ------
                   |    |
                   |    o
                   |   /|\\
                   |   / \\
                   |
                """]
    return pictures[tries]


# DO NOT EDIT CODE BELOW THIS LINE #


if __name__ == '__main__':
    main()
