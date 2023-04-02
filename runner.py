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

This module contains a function for running a game using our pygame GUI

Copyright and Usage Information
===============================

This file was developed as part of the course project for CSC111 Winter 2023.
Feel free to test it out, but please contact us to obtain permission if you
intend to redistribute it or use it for your own work.
"""

import sys
import pygame
from game import Game
from Pygame_go import update_display, retnr_row_col
from go_gui import draw_board


def run_game() -> None:
    """Run a basic Go game

    prompts user to input the moves
    returns the newly created game
    """
    new_game = Game()
    update_display(new_game)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if the user clicks the close button
                print("Black captured:", new_game.black_captured)
                print("White captured:", new_game.white_captured)
                draw_board(new_game.board, "go2434.jpg", True)
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # if the user clicks the mouse
                x, y = event.pos
                row, col = retnr_row_col(x, y)

                if len(new_game.moves) % 2 == 0:
                    color = "Black"
                else:
                    color = "White"

                if 0 <= row < 9 and 0 <= col < 9 and (row, col) and game.board.is_valid_move(row, col, color):
                    print((len(new_game.moves) + 1, row, col))
                    print("coordinates: ", row, col)
                    new_game.play_move(row, col)
                    update_display(new_game)
                else:
                    print("Invalid move")


if __name__ == "__main__":
    game = Game()
    run_game()
