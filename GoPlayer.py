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


import board

from game import Game
import GameTree
import random


class AbstractGoPlayer:
    """An abstract class for different algorithms to play Go"""
    gt: GameTree

    def __init__(self, gt: GameTree):
        self.gt = gt

    def make_move(self, game):
        """This function will determine how the algorithm chooses the
        next move to play
        """
        raise NotImplementedError


class Fully_random:
    """A Go player that plays randomly by choosing its next move randomly"""

    def __init__(self, gt: GameTree):
        self.gt = gt

    def make_move(self, game) -> tuple:
        """This function determines how the next move should be made. It
        plays randomly by choosing its next move randomly from empty positions
        """
        return random.choice(game.available_moves())


class RandomGoPlayer(AbstractGoPlayer):
    """A Go player that plays randomly by choosing its next move randomly
    from empty positions in proximity the last move played"""

    def __init__(self, gt: GameTree):
        """Initialize this GoPlayer"""
        AbstractGoPlayer.__init__(self, gt)

    def make_move(self, game: Game) -> tuple:
        """This function determines how the next move should be made. It
        plays randomly by choosing its next move randomly from empty positions
        in proximity the last move played
        """
        valid_moves = []
        move_sequence = game.moves
        if move_sequence != []:

            last_move = game.get_move_info(move_sequence[-1][1], move_sequence[-1][2])

            check_stone = game.board.get_stone(move_sequence[-1][1], move_sequence[-1][2])
            choices = [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
                       (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)]
            print(last_move[1])

            if not any(game.board.is_valid_move(choice[0], choice[1], last_move[1]) for choice in choices):
                valid_moves = game.available_moves()
                return random.choice(valid_moves)
            else:

                coord = random.choice(choices)
                while not game.board.is_valid_move(coord[0], coord[1], last_move[1]):
                    choices.remove(coord)
                    coord = random.choice(choices)

            return (coord[0], coord[1])
        else:
            return (random.randint(0, 8), random.randint(0, 8))


class SlightlyBetterBlackPlayer(AbstractGoPlayer):
    """A Go AI that makes the best move given in its subtree."""

    def __init__(self, gt: GameTree):
        """Initialize this GoPlayer"""
        AbstractGoPlayer.__init__(self, gt)

    def make_move(self, game: Game) -> tuple:
        """This function determines how the next move should be made. It
        plays the best possible move among its given choices, or randomly by choosing its next move randomly from empty
        positions in proximity the last move played if the tree is None or if it is a leaf
        notes: this DOES NOT update the move sequence
        since the AI updates the tree twice, when 2 AIs go against each other, they should not share a tree
        """
        if self.gt is not None:
            last_move = game.moves[-1]
            if self.gt.find_subtree_by_move(last_move) is None:
                self.gt = None  # update the subtree from previous move
            else:
                self.gt = self.gt.find_subtree_by_move(last_move)
        if self.gt is None or self.gt.get_subtrees() == [] or (game.moves[-1] not in self.gt._subtrees):
            self.gt = None  # TODO: _subtrees is private
            valid_moves = []
            move_sequence = game.moves
            if move_sequence != []:

                last_move = game.get_move_info(move_sequence[-1][1], move_sequence[-1][2])

                check_stone = game.board.get_stone(move_sequence[-1][1], move_sequence[-1][2])
                choices = [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
                           (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)]

                if not any(game.board.is_valid_move(choice[0], choice[1], last_move[1]) for choice in choices):
                    valid_moves = game.available_moves()
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

            max_win_prob = -99999999
            for subtree in self.gt.get_subtrees():  # TODO: get rid of private instance attribute
                if subtree.win_probability > max_win_prob:
                    max_win_prob = subtree.win_probability
                    best_choice = subtree
            self.gt = best_choice  # updates GameTree to be a subtree with the best choice
            return (best_choice.move[1],best_choice.move[2])  # will not be referenced before


class ProbabilityBaseGoplayer(AbstractGoPlayer):
    """A Go AI that makes the best move given in its subtree and its score probability."""

    def __init__(self, gt: GameTree):
        """Initialize this GoPlayer"""
        AbstractGoPlayer.__init__(self, gt)

    def make_move(self, game) -> tuple:
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

            return self.gt.move


if __name__ == '__main__':
    import sgf_reader

    gametree = None
    # game = Game()
    # ai=RandomGoPlayer(gametree,game)
    # print(ai.make_move())
    test_seq = sgf_reader.sgf_to_game_sequence('2015-06-30T13_28_05.990Z_j15601s5g8gk.sgf', 'DataSet/2015-Go9/')[0]
    game = Game(None, 'Black', test_seq)
    ai = RandomGoPlayer(gametree, game)
    print(ai.make_move())
