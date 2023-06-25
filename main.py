"""Beta-Go-Zero: AI for playing Go built with python

Author:
Henry "TJ" Chen

Original project by:
Henry "TJ" Chen
Dmitrii Vlasov
Ming Yau (Oscar) Lam
Duain Chhabra

Version: 1.3

Module Description
==================

This module contains the main runner for or program. Simply RUN this file in the python
console, and follow the instructions.

Warning: Read the prompts carefully to ensure that you are inputting values in the
expected format

For full instructions, please see the README file

Copyright and Usage Information
===============================

This project was originaly developed by students as part of CSC111 at the University of Toronto
See README file for full details
"""
import sys

import runner_solo
from sgf_reader import print_misc_stats, load_tree_from_file
from runner import run_game
from runner import simulate_game, simulate_games, plot_win_rate_progress

# from board import Board
# from sgf_reader import read_sgf
# from Pygame_go import draw_board
# from game import Game

MENU = '\n\nWelcome! Below are possible actions you can perform using our program.' \
       '\nTo SELECT an option, please enter the corresponding number as an integer.' \
       '\n0) Exit the program' \
       '\n1) Run a basic solo game' \
       '\n2) Run a simulation of one game of tree AI (white) against a random guesser (black)'\
       '\n3) Simulate n games of tree AI (white) against a random guesser (black)' \
       '\n4) simulates m trials of n games of tree AI (white) against a random guesser (black) and plots the data ' \
       '\n5) Some misc. stats about our data set' \
       '\n6) Experimental options'

EXPERIMENTAL_MENU = '\n\nBelow are some EXPERIMENTAL options you can perform.' \
                    '\nThese are provided for you to try out, but they may not be fully implemented'\
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
            max_game_len = int(
                input('Please enter your choice of max number of moves per game (50-67 is recommended):'))
            simulate_game(max_game_len, load_tree_from_file("completeScoreTree.txt", "tree_saves/"))
        elif user_choice == 3:
            n = int(input('Please enter your choice of the number of games simulated:'))
            simulate_games(n)
        elif user_choice == 4:
            n_games = int(input('Please enter your choice of the number of games simulated per trial:'))
            n_simulations = int(input('Please enter your choice of the number of trials simulated:'))
            plot_win_rate_progress(n_games, n_simulations)
        elif user_choice == 5:
            print("Please wait for a moment...")
            print_misc_stats()
        elif user_choice == 6:
            sub_menu()
        else:
            print("ERROR: That number was not one of our options, please try again!\n")


def sub_menu() -> None:
    """sub menu containing some experimental functions"""
    user_choice = - 1
    while not user_choice == 0:
        print(EXPERIMENTAL_MENU)
        user_choice = int(input('Please enter your choice below!'))

        if user_choice == 0:
            main_menu()
        elif user_choice == 1:
            runner_solo.run_game()
            print("Ran solo game sucessfully!")
        else:
            print("ERROR: That number was not one of our options, please try again!\n")


if __name__ == '__main__':
    main_menu()
