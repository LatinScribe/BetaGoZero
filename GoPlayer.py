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
import math

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

    def make_move(self) -> tuple:
        """This function determines how the next move should be made. It
        plays randomly by choosing its next move randomly from empty positions
        in proximity the last move played
        """
        valid_moves = []
        move_sequence = self.game.moves
        if move_sequence !=[]:
            last_move = self.game.get_move_info(move_sequence[-1][1], move_sequence[-1][2])

            check_stone = self.board.get_stone(move_sequence[-1][1], move_sequence[-1][2])
            choices = [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
                       (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)]
            print(last_move[1])
            if not any(self.board.is_valid_move(choice[0], choice[1], last_move[1]) for choice in choices):
                for x in range(0, self.board.size):
                    for y in range(0, self.board.size):
                        if self.board.is_valid_move(x, y, last_move[1]):
                            valid_moves += (last_move[0], x, y)
                return random.choice(valid_moves)
            else:
                coord = random.choice(choices)
                while not self.board.is_valid_move(coord[0], coord[1], last_move[1]):
                    choices.remove(coord)
                    coord = random.choice(choices)

            return (len(self.game.moves), coord[0], coord[1])
        else:
            return (random.randint(0,8),random.randint(0,8))


class SlightlyBetterBlackPlayer(AbstractGoPlayer):
    """A Go AI that makes the best move given in its subtree."""

    def __init__(self, gt: GameTree):
        """Initialize this GoPlayer"""
        AbstractGoPlayer.__init__(self, gt)

    def make_move(self, game) -> tuple:
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
        if self.gt is None or self.gt.get_subtrees() == [] or (
                game.moves[-1] not in self.gt._subtrees):  # TODO: _subtrees is private
            self.gt = None
            move_sequence = game.moves
            i = -1
            check_stone = game.board.get_stone(move_sequence[i][1], move_sequence[i][2])
            choices = [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
                       (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)]

            while not any(game.is_valid_move(choice[0], choice[1]) for choice in choices):
                i -= 1
                check_stone = game.board.get_stone(move_sequence[i][1], move_sequence[i][2])
                choices = [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
                           (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)]
            coord = random.choice(choices)
            while not game.is_valid_move(coord[0], coord[1]):
                choices.remove(coord)
                coord = random.choice(choices)

            return (len(game.moves), coord[0], coord[1])
        else:

            max_win_prob = -math.inf
            for subtree in self.gt.get_subtrees():  # TODO: get rid of private instance attribute
                if subtree.win_probability > max_win_prob:
                    max_win_prob = subtree.win_probability
                    best_choice = subtree
            self.gt = best_choice  # updates GameTree to be a subtree with the best choice
            return best_choice.move  # will not be referenced before

if __name__ == '__main__':
    import sgf_reader
    gametree = None
    # game = Game()
    # ai=RandomGoPlayer(gametree,game)
    # print(ai.make_move())
    test_seq=sgf_reader.sgf_to_game_sequence('2015-06-30T13_28_05.990Z_j15601s5g8gk.sgf', 'DataSet/2015-Go9/')[0]
    game=Game(None,'Black',test_seq)
    ai = RandomGoPlayer(gametree, game)
    print(ai.make_move())
