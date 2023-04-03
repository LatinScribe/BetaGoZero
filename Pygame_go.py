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

This module contains a functions nesscary to display a GUI to the user using
pygame

Copyright and Usage Information
===============================

This file was developed as part of the course project for CSC111 Winter 2023.
Feel free to test it out, but please contact us to obtain permission if you
intend to redistribute it or use it for your own work.
"""
import pygame
import sys
from board import Board
from game import Game

from PIL import Image, ImageDraw
from board import Board
import webbrowser
import os

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 9
CELL_SIZE = 50
LETTER_OFFSET = 20
NUMBER_OFFSET = 20
MARGIN = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (240, 230, 200)

# Screen size calculation
WIDTH = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * MARGIN

# Create a Pygame window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Go Board")
font = pygame.font.Font(None, 24)

# Create a game board
board = Board(9)


# game = Game()


def retnr_row_col(x, y):
    row = (x - MARGIN + 15) // CELL_SIZE
    col = (y - MARGIN + 15) // CELL_SIZE
    return row, col


def update_display(game: Game, territory: bool = False) -> None:
    """ Generate and Update the display
        We can use this function to update the display after each move
        Also Change the display to show the number of stones captured by each player
        Attributes can be changed later for better representation"""
    screen.fill(BACKGROUND)

    # Draw grid lines
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (MARGIN + i * CELL_SIZE, MARGIN),
                         (MARGIN + i * CELL_SIZE, HEIGHT - MARGIN - 50), 1)
        pygame.draw.line(screen, BLACK, (MARGIN, MARGIN + i * CELL_SIZE), (WIDTH - MARGIN - 50, MARGIN + i * CELL_SIZE),
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
        color = (game.board.get_stone(move[1], move[2])).color
        if color != "Neither":
            if color == "White":
                color = WHITE
            else:
                color = BLACK
            pygame.draw.circle(screen, color, (MARGIN + move[1] * CELL_SIZE, MARGIN + move[2] * CELL_SIZE),
                               CELL_SIZE // 2 - 2)
    # for i, x, y in game.moves:
    #     if i % 2 == 0:
    #         color = BLACK
    #     else:
    #         color = WHITE
    #     pygame.draw.circle(screen, color, (MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE), CELL_SIZE // 2 - 2)

    # Draw territory
    if territory:
        territories = game.board.calculate_score()
        square_size = 16
        for x, y in territories[2]:  # black territory
            rect_color = BLACK
            rect = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            rect.fill(rect_color)
            screen.blit(rect, (MARGIN + x * CELL_SIZE - square_size // 2, MARGIN + y * CELL_SIZE - square_size // 2))

        for x, y in territories[1]:  # white territory
            rect_color = WHITE
            rect = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            rect.fill(rect_color)
            screen.blit(rect, (MARGIN + x * CELL_SIZE - square_size // 2, MARGIN + y * CELL_SIZE - square_size // 2))

    pygame.display.flip()


def draw_board(given_board: Board, save_path: str = "Game_result/example.jpg", open_in_browser: bool = False,
               territory: bool = False, technique: str = "flood_fill"):
    """
    Generates a visualisation of the given board and saves it as a jpg file to the designated location.

    Defaults to saving in the Game_results folder as example.jpg

    The user can specify whether to open the image in their browser, default to not open it
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

        for x, y in territories[1]:  # black territory
            rect_color = "black"
            rect = Image.new("RGBA", (square_size, square_size), rect_color)
            image.paste(rect, (padding + x * cell_size - square_size // 2, padding + y * cell_size - square_size // 2),
                        rect)

        for x, y in territories[2]:  # white territory
            rect_color = "white"
            rect = Image.new("RGBA", (square_size, square_size), rect_color)
            image.paste(rect, (padding + x * cell_size - square_size // 2, padding + y * cell_size - square_size // 2),
                        rect)

    # save_path = "Game_result" + save_path
    image.save(save_path)

    if open_in_browser:
        webbrowser.open("file://" + os.path.realpath(save_path))
