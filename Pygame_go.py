"""Beta-Go-Zero: AI for playing Go built with python

Author:
Henry "TJ" Chen

Original project by:
Henry "TJ" Chen, Dmitrii Vlasov, Ming Yau (Oscar) Lam, Duain Chhabra

Version: 1.3

Module Description
==================

This module contains a functions nesscary to display a GUI to the user using
pygame

See README file for instructions, project details, and the relevant copyright and usage information
"""

import pygame
import webbrowser
import os
from pygame import Surface, SurfaceType
from pygame.font import Font
from PIL import Image, ImageDraw
from game import Game
from board import Board

# from typing import Tuple
# import sys

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


def return_row_col(x, y) -> tuple[int, int]:
    """
    Return the row and column of the cell that was clicked on

    Preconditions:
            - x and y are valid coordinates on the pygame window board
    """
    row = (x - MARGIN + 15) // CELL_SIZE
    col = (y - MARGIN + 15) // CELL_SIZE
    return row, col


def initialise_display(game: Game) -> Surface:
    """Initialise a pygame surface (screen) to respresent the current state of the given game
    returns the newly created screen

    Preconditions:
            - given game is a valid go game
    """

    # set up the pygame surface
    pygame.display.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Go Board")
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    screen.fill(BACKGROUND)

    pygame.event.clear()

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

    # Draw numbers on sides of board
    for i in range(BOARD_SIZE):
        label = font.render(str(i + 1), True, BLACK)
        screen.blit(label, (MARGIN - 2 * NUMBER_OFFSET, MARGIN + i * CELL_SIZE - NUMBER_OFFSET + 5))
        # screen.blit(label, (WIDTH - MARGIN + NUMBER_OFFSET - 50, MARGIN + i * CELL_SIZE - NUMBER_OFFSET + 5))

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

    pygame.display.flip()

    return screen


def update_display(screen: Surface, game: Game, territory: bool = False, technique: str = "flood_fill",
                   pause: bool = False) -> Surface:
    """ Takes the given pygame surface (screen) and updates

    We can use this function to update the display after each move
    Also Change the display to show the number of stones captured by each player
    Attributes can be changed later for better representation

    Preconditions:
            - given screen is a valid pygame surface
            - given game is a valid go game
            - given technique is a valid scoring technique
    """
    pygame.event.clear()

    font = pygame.font.Font(None, 24)

    if pause:
        # pause nesscary for when both players are AI to prevent flickering
        pygame.time.wait(WAIT_TIME)

    # Draw the last stone
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

        win = game.overall_score("dfs")
        if game.iswinner("White"):
            print("white wins by", win[0] - win[1])

        elif game.iswinner("Black"):
            print("black wins by", win[1] - win[0])
        else:
            print("tie")

        wait_for_quit()

    pygame.display.flip()

    return screen


def draw_board(given_board: Board, save_path: str = "Game_images/saved_board.jpg", open_in_browser: bool = False,
               territory: bool = False, technique: str = "flood_fill") -> None:
    """Generates a visualisation of the given board and saves it as a jpg file to the designated location.

    Defaults to saving in the Game_images folder as saved_board.jpg

    The user can specify whether to open the image in their browser, default to not open it

    Preconditions:
            - given board is a valid go board
            - given technique is a valid scoring technique
            - given save path is a valid save path
    """
    cell_size = 50
    board_size = given_board.size * cell_size
    padding = 20

    image = Image.new("RGB", (board_size + 2 * padding, board_size + 2 * padding), "#EEDC82")
    draw = ImageDraw.Draw(image)

    # Draw the lines
    for i in range(given_board.size):
        x = padding + i * cell_size
        draw.line([(x, padding), (x, board_size + padding - 50)], "black")
        draw.line([(padding, x), (board_size + padding - 50, x)], "black")

    # Draw the stones
    for x in range(given_board.size):
        for y in range(given_board.size):
            stone = given_board.get_stone(x, y)
            if stone.color != "Neither":
                radius = (cell_size // 2) - 4
                stone_x = padding + x * cell_size
                stone_y = padding + y * cell_size
                draw.ellipse([(stone_x - radius, stone_y - radius),
                              (stone_x + radius, stone_y + radius)],
                             fill=stone.color.lower())

    # Draw territory
    if territory:
        territories = given_board.calculate_score(technique=technique)
        square_size = 16

        for x, y in territories[0]:  # black territory
            rect_color = "black"
            rect = Image.new("RGBA", (square_size, square_size), rect_color)
            image.paste(rect, (padding + x * cell_size - square_size // 2, padding + y * cell_size - square_size // 2),
                        rect)

        for x, y in territories[1]:  # white territory
            rect_color = "white"
            rect = Image.new("RGBA", (square_size, square_size), rect_color)
            image.paste(rect, (padding + x * cell_size - square_size // 2, padding + y * cell_size - square_size // 2),
                        rect)

    # save_path = "Game_images" + save_path
    image.save(save_path)

    if open_in_browser:
        webbrowser.open("file://" + os.path.realpath(save_path))


def intialise_pygame() -> tuple[Surface | SurfaceType, Font]:
    """
    Initialise pygame and create a new pygame surface, which is returned along with a font
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Go Board")
    font = pygame.font.Font(None, 24)
    screen.fill(BACKGROUND)

    return screen, font


def wait_for_quit() -> None:
    """Wait until user closes the pygame window.

    Preconditions:
        - pygame window has been opened
    """
    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.wait()
    pygame.quit()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
