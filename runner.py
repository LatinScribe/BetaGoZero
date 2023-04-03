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
from Pygame_go import update_display, retnr_row_col, draw_board
from sgf_reader import sgf_to_game, read_all_sgf_in_folder, load_tree_from_file
from GoPlayer import AbstractGoPlayer, RandomGoPlayer, SlightlyBetterBlackPlayer, Fully_random


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


def part_runner_score(max_moves: int) -> Game:
    """
    Run the part of the project that calculates the score of a game
    """
    game_tree = load_tree_from_file("\completeScoreTree.txt", "tree_saves")

    game = Game()

    random_player = Fully_random(game_tree)
    ai_player = SlightlyBetterBlackPlayer(game_tree)
    for i in range(max_moves):
        guess = random_player.make_move(game)

        game.play_move(guess[0], guess[1])
        print("Random Guess: ", guess[0], guess[1])

        ai_guess = ai_player.make_move(game)
        game.play_move(ai_guess[1], ai_guess[2])
        print("AI Guess: ", ai_guess[1], ai_guess[2])
    return game

def run_gam():
    """Testting Function for the GUI"""
    # Initialize pygame
    pygame.init()

    game = sgf_to_game("2015-07-19T12_32_03.406Z_ycdor3fuul2s.sgf", "Dataset/2015-Go9/", )
    # Main game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = 0, 0
                    if game.is_valid_move(x, y):
                        game.play_move(x, y)
        clock.get_time()
        # Update the display
        update_display(game, territory=True)

        # Control the frame rate
        clock.tick(30)

    # Quit pygame
    pygame.quit()

run_gam()
#
# nwp = part_runner_score(50)
# draw_board(nwp.board, "go2434.jpg", True, True)
#

game = sgf_to_game("2015-07-19T12_32_03.406Z_ycdor3fuul2s.sgf", "Dataset/2015-Go9/")
print(game.moves)

# if __name__ == "__main__":
