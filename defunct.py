"""Beta-Go-Zero: AI for playing Go built with python

Author:
Henry "TJ" Chen

Version: 1.3

Module Description
==================

This module contains many defunct functions/material that is no longer in use

See README file for instructions, project details, and the relevant copyright and usage information"""

from game import Game
import pygame
from pygame import Surface
from pygame_go import intialise_pygame

################################################################################
# original constants
################################################################################
# Constants
BOARD_SIZE = 9
CELL_SIZE = 50
LETTER_OFFSET = 20
NUMBER_OFFSET = 20
MARGIN = 50

# edit this as nesscary for waiting when both players are AI
WAIT_TIME = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (240, 230, 200)

# Screen size calculation
WIDTH = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * MARGIN


################################################################################
# main.py
################################################################################


################################################################################
# runner.py
################################################################################
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


################################################################################
# game.py
################################################################################
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

    return new_game


# class Game():
#
#     def is_valid_move(self, x: int, y: int) -> bool:
#         """
#         Return True if the move at (x, y) is valid, False otherwise
#
#         NOTE: IMPORTANT - THIS IS AN OLD FUNCTION, USE THE NEWER FUNCTION UNDER BOARD
#
#         Preconditions:
#             - x < self.board.size
#             - y < self.board.size
#         """
#         return self.board.get_stone(x, y).color == "Neither"
################################################################################
# board.py
################################################################################

################################################################################
# gametree.py
################################################################################

################################################################################
# go_player.py
################################################################################

################################################################################
# sgf_reader.py
################################################################################

################################################################################
# pygame_go.py
################################################################################

def old_update_display(screen: Surface, game: Game, territory: bool = False, technique: str = "flood_fill",
                       pause: bool = False) -> Surface:
    """ Generate and Update the display
        We can use this function to update the display after each move
        Also Change the display to show the number of stones captured by each player
        Attributes can be changed later for better representation

    CURRENTLY DEFUNCT
    """

    if pause:
        pygame.time.wait(2000)

    # screen, font = intialise_pygame()
    _, font = intialise_pygame()
    screen.fill(BACKGROUND)

    # Draw grid lines
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (MARGIN + i * CELL_SIZE, MARGIN),
                         (MARGIN + i * CELL_SIZE, HEIGHT - MARGIN - 50), 1)
        pygame.draw.line(screen, BLACK, (MARGIN, MARGIN + i * CELL_SIZE),
                         (WIDTH - MARGIN - 50, MARGIN + i * CELL_SIZE),
                         1)

    # Draw letters
    for i, letter in enumerate("ABCDEFGHIJKLMNOP"):
        if i < BOARD_SIZE:
            label = font.render(letter, True, BLACK)
            screen.blit(label, (MARGIN + i * CELL_SIZE - LETTER_OFFSET + 5, MARGIN - 2 * LETTER_OFFSET))
            # screen.blit(label, (MARGIN + i * CELL_SIZE - LETTER_OFFSET + 5, HEIGHT - MARGIN + NUMBER_OFFSET - 50))

    # Draw numbers
    for i in range(BOARD_SIZE):
        label = font.render(str(i + 1), True, BLACK)
        screen.blit(label, (MARGIN - 2 * NUMBER_OFFSET, MARGIN + i * CELL_SIZE - NUMBER_OFFSET + 5))
        # screen.blit(label, (WIDTH - MARGIN + NUMBER_OFFSET - 50, MARGIN + i * CELL_SIZE - NUMBER_OFFSET + 5))

    # Draw stones
    for move in game.moves:
        # if (-1, -1) == move[1:]:
        #     break

        color = (game.board.get_stone(move[1], move[2])).color
        if color != "Neither":
            if color == "White":
                color = WHITE
            else:
                color = BLACK
            pygame.draw.circle(screen, color, (MARGIN + move[1] * CELL_SIZE, MARGIN + move[2] * CELL_SIZE),
                               CELL_SIZE // 2 - 2)
    for i, x, y in game.moves:
        if i % 2 == 0:
            color = BLACK
        else:
            color = WHITE
        pygame.draw.circle(screen, color, (MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE), CELL_SIZE // 2 - 2)

    # Draw territory
    if territory:
        territories = game.board.calculate_score(technique)
        square_size = 16
        for x, y in territories[0]:  # black territory
            rect_color = BLACK
            rect = pygame.Surface((square_size, square_size))
            rect.fill(rect_color)
            screen.blit(rect, (MARGIN + x * CELL_SIZE - square_size // 2, MARGIN + y * CELL_SIZE - square_size // 2))

        for x, y in territories[1]:  # white territory
            rect_color = WHITE
            rect = pygame.Surface((square_size, square_size))
            rect.fill(rect_color)
            screen.blit(rect, (MARGIN + x * CELL_SIZE - square_size // 2, MARGIN + y * CELL_SIZE - square_size // 2))

    pygame.display.flip()

    return screen
