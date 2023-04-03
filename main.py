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

# from board import Board
# from sgf_reader import read_sgf
# from Pygame_go import draw_board
# from game import Game

MENU = 'Welcome! Below are possible actions you can perform using our program.' \
       '\nTo SELECT an option, please enter the corresponding number as an integer.' \
       '\n0) Exit the program' \
       '\n1)' \
       '\n2)' \
       '\n3)' \
       '\n4)' \
       '\n5)'


user_choice = - 1
while not user_choice == 0:
    print(MENU)
    user_choice = int(input('Please enter your choice below!'))

    if user_choice == 0:
        sys.exit()
    elif user_choice == 1:
        ...  # Do something
    elif user_choice == 2:
        ...  # Do something
    elif user_choice == 3:
        ...  # Do something
    elif user_choice == 4:
        ...  # Do something
    elif user_choice == 5:
        ...  # Do something
    else:
        print("ERROR: That number was not one of our options, please try again!\n")
