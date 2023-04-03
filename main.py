"""Beta-Go: Course project for CSC111 Winter 2023

Authors:
Henry "TJ" Chen
Dmitrii Vlasov
Ming Yau (Oscar) Lam
Duain Chhabra

Date: April 3, 2023

Version: pre-Alpha

Module Description
==================

This module contains the main runner for or program. Simply RUN this file in the python
console, and follow the instructions.

Warning: Read the prompts carefully to ensure that you are inputting values in the
expected format

Copyright and Usage Information
===============================

This file was developed as part of the course project for CSC111 Winter 2023.
Feel free to test it out, but please contact us to obtain permission if you
intend to redistribute it or use it for your own work.
"""
import sys

import Runner_solo
from sgf_reader import print_misc_stats
from runner import run_game

# from board import Board
# from sgf_reader import read_sgf
# from Pygame_go import draw_board
# from game import Game

MENU = 'Welcome! Below are possible actions you can perform using our program.' \
       '\nTo SELECT an option, please enter the corresponding number as an integer.' \
       '\n0) Exit the program' \
       '\n1) Run a basic solo game' \
       '\n2)' \
       '\n3)' \
       '\n4)' \
       '\n5) Some misc. stats about our data set' \
       '\n6) Experimental options'

EXPERIMENTAL_MENU = 'Welcome! Below are some EXPERIMENTAL options you can perform.' \
                    '\nTo SELECT an option, please enter the corresponding number as an integer.' \
                    '\n0) Return to Main Menu' \
                    '\n1) Run a basic 9x9 solo game using keyboard input' \



def main_menu() -> None:
    """the main menu of our program"""
    user_choice = - 1
    while not user_choice == 0:
        print(MENU)
        user_choice = int(input('Please enter your choice below!'))

        if user_choice == 0:
            sys.exit()
        elif user_choice == 1:
            run_game()
            print("Ran solo game sucessfully!")
        elif user_choice == 2:
            ...  # Do something
        elif user_choice == 3:
            ...  # Do something
        elif user_choice == 4:
            ...  # Do something
        elif user_choice == 5:
            print("Please wait for a moment...")
            print_misc_stats()
        elif user_choice == 6:
            sub_menu()
        else:
            print("ERROR: That number was not one of our options, please try again!\n")


def sub_menu() -> None:
    """sub menu containing so experimental functions"""
    user_choice = - 1
    while not user_choice == 0:
        print(MENU)
        user_choice = int(input('Please enter your choice below!'))

        if user_choice == 0:
            main_menu()
        elif user_choice == 1:
            Runner_solo.run_game()
            print("Ran solo game sucessfully!")
        else:
            print("ERROR: That number was not one of our options, please try again!\n")


if __name__ == '__main__':
    main_menu()
