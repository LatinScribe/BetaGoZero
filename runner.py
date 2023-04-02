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
from sgf_reader import sgf_to_game, read_all_sgf_in_folder


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

                if 0 <= row < 9 and 0 <= col < 9 and (row, col) and new_game.board.is_valid_move(row, col, color):
                    print((len(new_game.moves) + 1, row, col))
                    print("coordinates: ", row, col)
                    new_game.play_move(row, col)
                    update_display(new_game)
                else:
                    print("Invalid move")



count = 5
for board in read_all_sgf_in_folder("DataSet/2015-Go9-super-small/"):
    count += 1
    print(board.calculate_score("dfs"))
    draw_board(board, format(f"hello{count}.jpg"), territory=True)

    print(board)

if __name__ == "__main__":
    sgf_reader = sgf_to_game("/2015-07-25T13_10_48.748Z_seowzegj5utb.sgf", "DataSet/2015-Go9")
    # draw_board(sgf_reader.board, "hello.jpg", True, True)
    # print(sgf_reader.board)
    # print(sgf_reader.board.calculate_score())
    # run_game(sgf_reader)
