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

This module contains python function to run a basic Go game on a 9x9 board game
This is a solo mode, where the user places stones on the board, the finished game
is saved as a png and outputted to the user

See README file for instructions, project details, and the relevant copyright and usage information
"""
from game import Game
from pygame_go import draw_board


def run_game() -> Game:
    """Run a basic Go game on a 9x9 board game

    prompts user to input the moves they would like to make
    returns the newly created game
    """
    new_game = Game()
    next_move = ''

    while next_move != 'STOP':
        # used for creating a new line in f-string
        n1 = '\n'

        # get input from user
        next_move = input(
            f'It is currently {new_game.current_player}\'s turn. Please enter your next move as a coordinate'
            f'in the form: x,y.{n1}If you would like to end the game, enter \"STOP\" without qoutation marks!')

        # convert to upper case to avoid case sensitivity
        next_move.upper()

        if not next_move == 'STOP':
            coords = next_move.split(",")
            x = int(coords[0])
            y = int(coords[1])

            new_game.play_move(x, y)
    draw_board(new_game.board, "Game_result/runner_example.jpg", True)

    return new_game

# def run_ai_game
