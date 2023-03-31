"""A simple GUI for the Go game."""

from PIL import Image, ImageDraw
from board import Board
import webbrowser
import os


def draw_board(board: Board, save_path: str = "Game_result/go.jpg", open_in_browser: bool = False):
    """
    Generates a visualisation of the board and saves it as a jpg file
    """
    cell_size = 50
    board_size = board.size * cell_size
    padding = 20

    image = Image.new("RGB", (board_size + 2 * padding, board_size + 2 * padding), "#EEDC82")
    draw = ImageDraw.Draw(image)

    for i in range(board.size):
        x = padding + i * cell_size
        draw.line([(x, padding), (x, board_size + padding)], "black")
        draw.line([(padding, x), (board_size + padding, x)], "black")

    for x in range(board.size):
        for y in range(board.size):
            stone = board.get_stone(x, y)
            if stone.color != "Neither":
                radius = (cell_size // 2) - 4
                stone_x = padding + x * cell_size
                stone_y = padding + y * cell_size
                draw.ellipse([(stone_x - radius, stone_y - radius),
                              (stone_x + radius, stone_y + radius)],
                             fill=stone.color.lower())

    save_path = "Game_result" + save_path
    image.save(save_path)

    if open_in_browser:
        webbrowser.open("file://" + os.path.realpath(save_path))


if __name__ == "__main__":
    board = Board()
    board.add_stone(2, 2, "Black")
    board.add_stone(3, 3, "White")
    board.add_stone(4, 2, "Black")
    draw_board(board)
