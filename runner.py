"""Beta-Go-Zero: AI for playing Go built with python

Author:
Henry "TJ" Chen

Original project by:
Henry "TJ" Chen, Dmitrii Vlasov, Ming Yau (Oscar) Lam, Duain Chhabra

Version: 1.3

Module Description
==================

This module contains a function for running a game using our pygame GUI

See README file for instructions, project details, and the relevant copyright and usage information
"""

import random
from game import Game
from pygame_go import initialise_display, update_display
from gametree import GameTree
from sgf_reader import load_tree_from_file, save_tree_to_file
from go_player import ProbabilityBaseGoplayer, GoPlayer, FullyRandom, UserGoPlayer
import plotly.graph_objs as g_obj

# import sys
# from typing import Tuple
# import pygame
# from Pygame_go import draw_board, return_row_col, update_display
# from sgf_reader import sgf_to_game, read_all_sgf_in_folder
# from GoPlayer import SlightlyBetterBlackPlayer


def run_game() -> None:
    """Run a basic Go game

    prompts user to input the moves
    returns the newly created game
    """
    print("Please wait for a moment...")
    tree = load_tree_from_file("RecalcScoreTree.txt", "tree_saves/")

    size = int(input('Please select a board size! Enter 9, 13, or 19'))

    if not (size == 9 or size == 13 or size == 19):
        print('Defaulting to size 9')
        size = 9

    user_selection = input('\n\nNow, select a setting for the BLACK player'
                           '\nTo SELECT an option, please enter the corresponding number as an integer.'
                           '\n0) UserPlayer: YOU play as the player'
                           '\n1) TreeAI: Play against our tree AI'
                           '\n2) RandomAI: Play against an AI that guesses randomly'
                           )
    if user_selection == '0':
        black_player = UserGoPlayer(tree)
    elif user_selection == '1':
        black_player = ProbabilityBaseGoplayer(tree)
    elif user_selection == '2':
        black_player = FullyRandom(tree)
    else:
        print('This was not a valid choice. Defaulting to UserPlayer')
        black_player = UserGoPlayer(tree)

    user_selection = input('\n\nNow, select a setting for the WHITE player'
                           '\nTo SELECT an option, please enter the corresponding number as an integer.'
                           '\n0) UserPlayer: YOU play as the player'
                           '\n1) TreeAI: Play against our tree AI'
                           '\n2) RandomAI: Play against an AI that guesses randomly'
                           )

    if user_selection == '0':
        white_player = UserGoPlayer(tree)
    elif user_selection == '1':
        white_player = ProbabilityBaseGoplayer(tree)
    elif user_selection == '2':
        white_player = FullyRandom(tree)
    else:
        print('This was not a valid choice. Defaulting to UserPlayer')
        white_player = UserGoPlayer(tree)

    run_game_players(black_player, white_player, size)


def run_game_players(b_player: GoPlayer, w_player: GoPlayer, board_size: int = 9) -> None:
    """Runs a game of Go using the selected players types and board_size"""
    new_game = Game(size=board_size)
    display = initialise_display(new_game)

    if isinstance(b_player, UserGoPlayer) or isinstance(w_player, UserGoPlayer):
        while True:
            if len(new_game.moves) % 2 == 0:
                x, y = b_player.make_move(new_game)
                new_game.play_move(x, y)
                update_display(display, new_game)
            else:
                x, y = w_player.make_move(new_game)
                new_game.play_move(x, y)
                update_display(display, new_game)

    else:
        while len(new_game.moves) <= 65:
            if len(new_game.moves) % 2 == 0:
                x, y = b_player.make_move(new_game)
                new_game.play_move(x, y)

                update_display(display, new_game, pause=True)
            else:
                x, y = w_player.make_move(new_game)
                new_game.play_move(x, y)
                update_display(display, new_game, pause=True)

        update_display(display, new_game, territory=True, pause=True)


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
    tree = load_tree_from_file("experimental.txt", "tree_saves/")
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

    save_tree_to_file(tree, "experimental.txt", "tree_saves/")
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

    fig = g_obj.Figure()
    fig.add_trace(
        g_obj.Scatter(x=list(range(1, n_simulations + 1)), y=black_win_rates, mode='lines+markers',
                      name='Black Win Rate'))
    fig.add_trace(
        g_obj.Scatter(x=list(range(1, n_simulations + 1)), y=white_win_rates, mode='lines+markers',
                      name='White Win Rate'))

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
