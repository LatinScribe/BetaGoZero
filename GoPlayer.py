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

This module contains the python classes nesscary to represent our different
implementations of algorithms designed to play Go.

Copyright and Usage Information
===============================

This file was developed as part of the course project for CSC111 Winter 2023.
Feel free to test it out, but please contact us to obtain permission if you
intend to redistribute it or use it for your own work.
"""

# import board
import sys
import pygame
from game import Game
import GameTree
import random
from Pygame_go import draw_board, return_row_col, update_display


class GoPlayer:
    """An abstract class for different algorithms to play Go"""
    gt: GameTree

    def __init__(self, gt: GameTree) -> None:
        self.gt = gt

    def make_move(self, game) -> tuple[int, int]:
        """This function will determine how the algorithm chooses the
        next move to play
        """
        raise NotImplementedError


class FullyRandom:
    """A Go player that plays randomly by choosing its next move randomly"""

    def __init__(self, gt: GameTree) -> None:
        self.gt = gt

    def make_move(self, game: Game) -> tuple[int, int]:
        """This function determines how the next move should be made. It
        plays randomly by choosing its next move randomly from empty positions
        """
        return random.choice(game.available_moves())


class UserGoPlayer(GoPlayer):
    """A Go player that allows the user to play a move on the board by clicking"""

    def __init__(self, gt: GameTree) -> None:
        GoPlayer.__init__(self, gt)

    def make_move(self, game) -> tuple[int, int]:
        """makes move based on where the user clicks """
        new_game = game

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if the user clicks the close button
                    print("Black captured:", new_game.black_captured)
                    print("White captured:", new_game.white_captured)
                    win = new_game.overall_score("dfs")
                    if new_game.iswinner("White"):
                        print("white wins by", win[0] - win[1])

                    elif new_game.iswinner("Black"):
                        print("black wins by", win[1] - win[0])
                    else:
                        print("tie")

                    draw_board(new_game.board, "go2434.jpg", True, True)
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # if the user clicks the mouse
                    x, y = event.pos
                    row, col = return_row_col(x, y)

                    if len(new_game.moves) % 2 == 0:
                        color = "Black"
                    else:
                        color = "White"

                    if 0 <= row < 9 and 0 <= col < 9 and (row, col) and new_game.board.is_valid_move(row, col, color):
                        print((len(new_game.moves) + 1, row, col))
                        print("coordinates: ", row, col)
                        return (row, col)
                    else:
                        print("Invalid move")


class RandomGoPlayer(GoPlayer):
    """A Go player that plays randomly by choosing its next move randomly
    from empty positions in proximity the last move played"""

    def __init__(self, gt: GameTree) -> None:
        """Initialize this GoPlayer"""
        GoPlayer.__init__(self, gt)

    def make_move(self, game: Game) -> tuple[int, int]:
        """This function determines how the next move should be made. It
        plays randomly by choosing its next move randomly from empty positions
        in proximity the last move played

        Does not work as of now
        """
        valid_moves = []
        move_sequence = game.moves
        if move_sequence:

            last_move = game.get_move_info(move_sequence[-1][1], move_sequence[-1][2])

            check_stone = game.board.get_stone(move_sequence[-1][1], move_sequence[-1][2])
            choices = [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
                       (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)]

            if not any(game.board.is_valid_move(choice[0], choice[1], last_move[1]) for choice in choices):

                for x in range(0, game.board.size):
                    for y in range(0, game.board.size):
                        if game.board.is_valid_move(x, y, last_move[1]):
                            valid_moves.append((last_move[0] + 1, x, y))

                valid_moves = game.available_moves()
                # for x in range(0, game.board.size):
                #     for y in range(0, game.board.size):
                #         if game.board.is_valid_move(x, y, last_move[1]):
                #             valid_moves.append((x, y))

                return random.choice(valid_moves)
            else:

                coord = random.choice(choices)
                while not game.board.is_valid_move(coord[0], coord[1], last_move[1]):
                    choices.remove(coord)
                    coord = random.choice(choices)

            return (coord[0], coord[1])
        else:
            return (random.randint(0, 8), random.randint(0, 8))


class SlightlyBetterBlackPlayer(GoPlayer):
    """A Go AI that makes the best move given in its subtree."""

    def __init__(self, gt: GameTree) -> None:
        """Initialize this GoPlayer"""
        GoPlayer.__init__(self, gt)

    def make_move(self, game: Game) -> tuple[int, int]:
        """This function determines how the next move should be made. It
        plays the best possible move among its given choices, or randomly by choosing its next move randomly from empty
        positions in proximity the last move played if the tree is None or if it is a leaf
        notes: this DOES NOT update the move sequence
        since the AI updates the tree twice, when 2 AIs go against each other, they should not share a tree

        Does not work as of now
        """
        if self.gt is not None:
            if game.moves:
                last_move = game.moves[-1]
            else:
                return (random.randint(0, 8), random.randint(0, 8))
            if self.gt.find_subtree_by_move(last_move) is None:
                self.gt = None  # update the subtree from previous move
            else:
                self.gt = self.gt.find_subtree_by_move(last_move)
        if self.gt is None or self.gt.get_subtrees() == [] or (game.moves[-1] not in self.gt.get_subtrees()):
            self.gt = None

            move_sequence = game.moves
            if move_sequence:

                last_move = game.get_move_info(move_sequence[-1][1], move_sequence[-1][2])

                check_stone = game.board.get_stone(move_sequence[-1][1], move_sequence[-1][2])
                choices = [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
                           (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)]

                if not any(game.board.is_valid_move(choice[0], choice[1], last_move[1]) for choice in choices):
                    valid_moves = game.available_moves()
                    # for x in range(0, game.board.size):
                    #     for y in range(0, game.board.size):
                    #         if game.board.is_valid_move(x, y, last_move[1]):
                    #             valid_moves.append((x, y))
                    return random.choice(valid_moves)
                else:

                    coord = random.choice(choices)
                    while not game.board.is_valid_move(coord[0], coord[1], last_move[1]):
                        choices.remove(coord)
                        coord = random.choice(choices)

                return (coord[0], coord[1])
            else:
                return (random.randint(0, 8), random.randint(0, 8))
        else:
            subtrees = self.gt.get_subtrees()
            best_choice = subtrees[0]
            max_win_prob = best_choice.win_probability
            for i in range(1, len(subtrees)):
                subtree = subtrees[i]
                if subtree.win_probability > max_win_prob:
                    max_win_prob = subtree.win_probability
                    best_choice = subtree
            self.gt = best_choice  # updates GameTree to be a subtree with the best choice
            return (best_choice.move[1], best_choice.move[2])  # will not be referenced before


class ProbabilityBaseGoplayer(GoPlayer):
    """A Go AI that makes the best move given in its subtree and its score probability."""

    def __init__(self, gt: GameTree) -> None:
        """Initialize this GoPlayer"""
        GoPlayer.__init__(self, gt)

    def make_move(self, game: Game) -> tuple[int, int]:
        """ This function determines how the next move should be made.
        It moves forward to the last move on the tree, then chooses a move based on the probability of that move,
        and follows the tree to make a random move."""

        # Reassign the tree
        if not game.get_move_sequence():  # First Move
            pass
        elif not self.gt or len(self.gt.get_subtrees()) == 0:
            self.gt = None
        else:
            adversary_move = game.get_move_sequence()[-1]
            new_subtree = self.gt.find_subtree_by_move(adversary_move)
            self.gt = new_subtree

        if not self.gt or len(self.gt.get_subtrees()) == 0:
            possible_moves = game.available_moves()
            return random.choice(list(possible_moves))
        else:
            choices = self.gt.get_subtrees()

            highest_prob = 0.0
            highest_move = choices[0]

            for choice in choices:
                if choice.win_probability >= highest_prob:
                    highest_prob = choice.win_probability
                    highest_move = choice.move

            subtree = self.gt.find_subtree_by_move(highest_move)

            self.gt = subtree  # Reassigning the tree to the chosen move's subtree

            if self.gt is None:
                possible_moves = game.available_moves()
                return random.choice(list(possible_moves))

            return (self.gt.move[1], self.gt.move[2])


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # import sgf_reader

    # gametree = None
    # game = Game()
    # ai=RandomGoPlayer(gametree,game)
    # print(ai.make_move())
    # test_seq = sgf_reader.sgf_to_game_sequence('2015-06-30T13_28_05.990Z_j15601s5g8gk.sgf', 'DataSet/2015-Go9/')[0]
    # game = Game(None, 'Black', test_seq)
    # ai = RandomGoPlayer(gametree, game)
    # print(ai.make_move())
