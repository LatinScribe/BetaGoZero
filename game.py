"""Game class for Go."""

from board import Board
from go_gui import draw_board

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = "Black"

    def play_move(self, x, y):
        if self.board.get_stone(x, y).color == "Neither":
            self.board.add_stone(x, y, self.current_player)
            self.current_player = "White" if self.current_player == "Black" else "Black"
            return True
        else:
            return False

    def run_example(self, moves):
        for move in moves:
            x, y = move
            print(f"Playing {self.current_player}'s move at ({x}, {y})")
            success = self.play_move(x, y)
            if success:
                print("Move successful.")
            else:
                print("Move failed. Position already occupied.")
        print("Final board state:")
        print(self.board)
        draw_board(self.board, open_in_browser=True)


if __name__ == "__main__":
    game = Game()
    moves = [(0, 0), (1, 1), (0, 1), (1, 0), (0, 2), (2, 2)]
    game.run_example(moves)
