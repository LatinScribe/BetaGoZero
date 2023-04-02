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

This module contains the functions nesscary for outputting visual representations
of a game of Go.

Copyright and Usage Information
===============================

This file was developed as part of the course project for CSC111 Winter 2023.
Feel free to test it out, but please contact us to obtain permission if you
intend to redistribute it or use it for your own work.
"""

from PIL import Image, ImageDraw
from board import Board
import webbrowser
import os




def draw_board(given_board: Board, save_path: str = "Game_result/example.jpg", open_in_browser: bool = False, territory: bool = False , technique: str = "flood_fill"):
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
            image.paste(rect, (padding + x * cell_size - square_size // 2, padding + y * cell_size - square_size // 2), rect)

        for x, y in territories[2]:  # white territory
            rect_color = "white"
            rect = Image.new("RGBA", (square_size, square_size), rect_color)
            image.paste(rect, (padding + x * cell_size - square_size // 2, padding + y * cell_size - square_size // 2), rect)


    # save_path = "Game_result" + save_path
    image.save(save_path)

    if open_in_browser:
        webbrowser.open("file://" + os.path.realpath(save_path))


if __name__ == "__main__":
    board = Board()
    board.add_stone(2, 2, "Black")
    board.add_stone(3, 3, "White")
    board.add_stone(4, 2, "Black")
    draw_board(board, open_in_browser=True)
