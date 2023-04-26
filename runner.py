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
import random
# from typing import Tuple

import pygame
from game import Game
from Pygame_go import draw_board, retnr_row_col, update_display
# from Pygame_go import intialise_pygame
from GameTree import GameTree
from sgf_reader import load_tree_from_file, save_tree_to_file
# from sgf_reader import sgf_to_game, read_all_sgf_in_folder
from GoPlayer import FullyRandom, ProbabilityBaseGoplayer
# from GoPlayer import AbstractGoPlayer, RandomGoPlayer, SlightlyBetterBlackPlayer
import plotly.graph_objs as go


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
                win = new_game.overall_score("dfs")
                if new_game.iswinner("White"):
                    print("white wins by", win[0] - win[1])

                elif new_game.iswinner("Black"):
                    print("black wins by", win[1] - win[0])
                else:
                    print("tie")

                draw_board(new_game.board, "go2434.jpg", True, True)
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


def simulate_game(max_moves: int, game_tree: GameTree) -> tuple[Game, float]:
    """
    Similates a game of Go with the given max moves and pregenerated GameTree

    Notes:
        Black is a Random guessing AI
        White is a tree based probability AI
    """

    game = Game()

    random_player = FullyRandom(game_tree)
    ai_player = ProbabilityBaseGoplayer(game_tree)
    for _ in range(max_moves):
        if game.game_end(max_moves):
            break
        guess = random_player.make_move(game)
        game.play_move(guess[0], guess[1])

        ai_guess = ai_player.make_move(game)
        check = game.play_move(ai_guess[0], ai_guess[1])
        if not check:
            chosen_move = random.choice(game.available_moves())
            game.play_move(chosen_move[0], chosen_move[1])

    win = game.overall_score("dfs")
    if game.iswinner("White"):
        print("white wins by", win[0] - win[1])

    elif game.iswinner("Black"):
        print("black wins by", win[1] - win[0])
    else:
        print("tie")

    return game, win[1] - win[0]


def simulate_games(n: int) -> tuple[float, float]:
    """Run n AI games and print the results

    Notes:
        Black is a Random guessing AI
        White is a tree based probability AI
    """
    # wins = []
    tree = load_tree_from_file("expiremental.txt", "tree_saves/")
    white_win_rate = 0
    black_win_rate = 0
    for _ in range(n):
        # game, win = simulate_game(50, tree)
        result = simulate_game(50, tree)
        game = result[0]
        if game.iswinner("White"):
            white_win_rate += 1
        else:
            black_win_rate += 1
        tree.insert_game_into_tree_absolute(game)

    save_tree_to_file(tree, "expiremental.txt", "tree_saves/")
    print("black win rate:", black_win_rate / n)
    print("white win rate:", white_win_rate / n)

    return black_win_rate / n, white_win_rate / n


def plot_win_rate_progress(n_games: int, n_simulations: int) -> None:
    """plot the win rate (black vs white) for given number of games and simulations

    Notes:
        Black is a Random guessing AI
        White is a tree based probability AI
    """
    black_win_rates = []
    white_win_rates = []

    for _ in range(1, n_simulations + 1):
        black_win_rate, white_win_rate = simulate_games(n_games)
        black_win_rates.append(black_win_rate)
        white_win_rates.append(white_win_rate)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(range(1, n_simulations + 1)), y=black_win_rates, mode='lines+markers', name='Black Win Rate'))
    fig.add_trace(
        go.Scatter(x=list(range(1, n_simulations + 1)), y=white_win_rates, mode='lines+markers', name='White Win Rate'))

    fig.update_layout(title=f'Win Rate Progression over {n_simulations} Simulations', xaxis_title='Simulation',
                      yaxis_title='Win Rate', legend_title='Player')

    # To save the plot to a file, uncomment the following line:
    # pio.write_image(fig, 'win_rate_progression.png')

    fig.show()


if __name__ == "__main__":
    # nwp = simulate_game(30)
    # draw_board(nwp.board, "go2434.jpg", True, True)
    # simulate_games(500)
    # run_game()
    # nwp, win_score = simulate_game(50)
    # draw_board(nwp.board, "go2434.jpg", True, True)
    plot_win_rate_progress(n_games=100, n_simulations=20)

    pass
