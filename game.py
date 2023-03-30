"""Game class for Go."""

from board import Board
from go_gui import draw_board


class Game:
    """A class representing the state of a game of Go.

     Instance Attributes:
        - board: representation of the current state of the board
        - current_player: who's turn is it, either "Black" or "White
        - moves: a list that represents the sequence of moves played so far in the game

    """
    board: Board
    current_player: str
    moves: list[tuple[int, int, int]]

    def __init__(self):
        self.board = Board()
        self.current_player = "Black"
        self.moves = []

    def play_move(self, x, y) -> bool:
        """
        Given the location of a new move, updates the board and game.
        :param x:
        :param y:
        :return:
        """
        if self.board.get_stone(x, y).color == "Neither":
            self.board.add_stone(x, y, self.current_player)
            self.current_player = "White" if self.current_player == "Black" else "Black"

            new_move = (len(self.moves) + 1, x, y)
            self.moves.append(new_move)
            return True
        else:
            return False

    def run_example(self, moves_sequence) -> None:
        """Function for testing the ouputting of a final board state"""
        for move in moves_sequence:
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


################################################################################
# Functions for running games
################################################################################

def run_game() -> Game:
    """Run an Adversarial Wordle game between the two given players.

    Use the words in word_set_file, and use max_guesses as the maximum number of guesses.

    Return the AdversarialWordle instance after the game is complete.

    Preconditions:
    - word_set_file is a non-empty with one word per line
    - all words in word_set_file have the same length
    - max_guesses >= 1
    """
    new_game = Game()
    next_move = ''

    while next_move != 'STOP':
        next_move = input("it is currently")

    return game


if __name__ == "__main__":
    game = Game()
    moves = [(0, 0), (1, 1), (0, 1), (1, 0), (0, 2), (2, 2)]
    game.run_example(moves)
