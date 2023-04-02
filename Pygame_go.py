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
def update_display(game: Game):
    """ Generate and Update the display
        We can use this function to update the display after each move
        Also Change the display to show the number of stones captured by each player
        Attributes can be changed later for better representation"""
    screen.fill(BACKGROUND)

    # Draw grid lines
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (MARGIN + i * CELL_SIZE, MARGIN), (MARGIN + i * CELL_SIZE, HEIGHT - MARGIN - 50), 1)
        pygame.draw.line(screen, BLACK, (MARGIN, MARGIN + i * CELL_SIZE), (WIDTH - MARGIN - 50, MARGIN + i * CELL_SIZE), 1)

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
            pygame.draw.circle(screen, color, (MARGIN + move[1] * CELL_SIZE, MARGIN + move[2] * CELL_SIZE), CELL_SIZE // 2 - 2)
    # for i, x, y in game.moves:
    #     if i % 2 == 0:
    #         color = BLACK
    #     else:
    #         color = WHITE
    #     pygame.draw.circle(screen, color, (MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE), CELL_SIZE // 2 - 2)

    pygame.display.flip()



# Test Loop
# turn = 0
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             x, y = event.pos
#             row = (x - MARGIN) // CELL_SIZE
#             col = (y - MARGIN) // CELL_SIZE
#             if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
#                 turn += 1
#                 game.moves.append((turn, row, col))
#                 update_display(game)
