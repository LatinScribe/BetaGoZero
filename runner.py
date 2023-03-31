import sys
import pygame
from game import Game
from Pygame_go import update_display, retnr_row_col
from go_gui import draw_board

def run_game() -> None:
    """Run a basic Go game

    prompts user to input the moves
    returns the newly created game
    """
    new_game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:# if the user clicks the close button
                draw_board(new_game.board, "go2434.jpg", True)
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # if the user clicks the mouse
                x, y = event.pos
                row, col = retnr_row_col(x, y)

                if 0 <= row < 9 and 0 <= col < 9 and (row, col) not in new_game.played_moves():
                    print((len(new_game.moves) + 1, row, col))
                    print("coordinates: ", row, col)
                    new_game.play_move(row, col)
                    update_display(new_game)
                else:
                    print("Invalid move")


if __name__ == "__main__":
    game = Game()
    run_game()
