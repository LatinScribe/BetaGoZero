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

This module contains a function for running a game using our pygame GUI

See README file for instructions, project details, and the relevant copyright and usage information
"""

import random
<<<<<<< Updated upstream
# from typing import Tuple

import pygame
from game import Game
from Pygame_go import draw_board, retnr_row_col, update_display
# from Pygame_go import intialise_pygame
from GameTree import GameTree
=======
from game import Game
from pygame_go import initialise_display, update_display
from gametree import GameTree
>>>>>>> Stashed changes
from sgf_reader import load_tree_from_file, save_tree_to_file
from go_player import FullyRandom, ProbabilityBaseGoplayer, GoPlayer, BetterRandomGoPlayer, UserGoPlayer
import plotly.graph_objs as g_obj

# import sys
# from typing import Tuple
# import pygame
# from Pygame_go import draw_board, return_row_col, update_display
# from sgf_reader import sgf_to_game, read_all_sgf_in_folder
<<<<<<< Updated upstream
from GoPlayer import FullyRandom, ProbabilityBaseGoplayer
# from GoPlayer import AbstractGoPlayer, RandomGoPlayer, SlightlyBetterBlackPlayer
import plotly.graph_objs as go
=======
# from GoPlayer import SlightlyBetterBlackPlayer
>>>>>>> Stashed changes


def run_game() -> None:
    """Run a game of Go.

    Prompts user to select the settings to set up the game.

    Currently recommended settings: board size 9
    """
<<<<<<< Updated upstream
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
=======
    # load the pregenerated game tree from save file
    print("Please wait for a moment...")
    tree = load_tree_from_file("RecalcScoreTree.txt", "tree_saves/")

    # get the users choice of board size
    size = int(input('Please select a board size! Enter 9, 13, or 19'))

    # default to size 9 for other input
    if not (size == 9 or size == 13 or size == 19):
        print('Defaulting to size 9')
        size = 9

    # get user selection for black player and set it accordingly
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

    # get user selection for white player and set it accordingly
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

    # if at least one player is the user, run without a pause
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
        # since both players are AI, run with a slight pause to prevent rapid flashing
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
>>>>>>> Stashed changes


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


<<<<<<< Updated upstream
=======
def old_run_game() -> None:
    """Run a basic Go game

    prompts user to input the moves and returns the newly created game

    DEFUNCT: NO LONGER IN USE
    """
    # new_game = Game()

    # update_display(new_game)
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:  # if the user clicks the close button
    #             print("Black captured:", new_game.black_captured)
    #             print("White captured:", new_game.white_captured)
    #             win = new_game.overall_score("dfs")
    #             if new_game.iswinner("White"):
    #                 print("white wins by", win[0] - win[1])
    #
    #             elif new_game.iswinner("Black"):
    #                 print("black wins by", win[1] - win[0])
    #             else:
    #                 print("tie")
    #
    #             draw_board(new_game.board, "go2434.jpg", True, True)
    #             sys.exit()
    #         elif event.type == pygame.MOUSEBUTTONDOWN:  # if the user clicks the mouse
    #             x, y = event.pos
    #             row, col = return_row_col(x, y)
    #
    #             if len(new_game.moves) % 2 == 0:
    #                 color = "Black"
    #             else:
    #                 color = "White"
    #
    #             if 0 <= row < 9 and 0 <= col < 9 and (row, col) and new_game.board.is_valid_move(row, col, color):
    #                 print((len(new_game.moves) + 1, row, col))
    #                 print("coordinates: ", row, col)
    #                 new_game.play_move(row, col)
    #                 update_display(new_game)
    #             else:
    #                 print("Invalid move")


>>>>>>> Stashed changes
if __name__ == "__main__":
    # nwp = simulate_game(30)
    # draw_board(nwp.board, "go2434.jpg", True, True)
    # simulate_games(500)
    # run_game()
    # nwp, win_score = simulate_game(50)
    # draw_board(nwp.board, "go2434.jpg", True, True)
    plot_win_rate_progress(n_games=100, n_simulations=20)

    pass
