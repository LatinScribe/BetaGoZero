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
    board: board.Board
    gt: GameTree.GameTree
    game: Game

    def __init__(self, gt: GameTree, active_game: Game):
        self.board = board.Board(active_game.board_size)
        self.gt = gt
        self.game = active_game

    def make_move(self):
        """This function will determine how the algorithm chooses the
        next move to play
        """
        raise NotImplementedError


class RandomGoPlayer(AbstractGoPlayer):
    """A Go player that plays randomly by choosing its next move randomly
    from empty positions in proximity the last move played"""

    def __init__(self, gt: GameTree, active_game: Game):
        """Initialize this GoPlayer"""
        AbstractGoPlayer.__init__(self, gt, active_game)

    def make_move(self):
        """This function determines how the next move should be made. It
        plays randomly by choosing its next move randomly from empty positions
        in proximity the last move played
        """
        move_sequence = self.game.moves
        i = -1
        check_stone = self.board.get_stone(move_sequence[i][1], move_sequence[i][2])

        while len(check_stone.get_neighbours()) == check_stone.max_num_neighbours:
            i -= 1
            check_stone = self.board.get_stone(move_sequence[i][1], move_sequence[i][2])
        coord = random.choice(
            [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
             (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)])
        while (coord in check_stone.neighbours) or coord[0] in [-1, 9] or coord[1] in [-1, 9]:
            coord = random.choice(
                [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
                 (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)])
        return coord
    
class SlightlyBetterBlackPlayer(AbstractGoPlayer):
    """A Go AI that makes the best move given in its subtree."""

    def __init__(self, gt: GameTree, active_game: Game):
        """Initialize this GoPlayer"""
        AbstractGoPlayer.__init__(self, gt, active_game)

    def make_move(self) -> tuple:
        """This function determines how the next move should be made. It
        plays the best possible move among its given choices, or randomly by choosing its next move randomly from empty 
        positions in proximity the last move played if the tree is None or if it is a leaf 
        """
        if self.gt is None or self.gt.get_subtrees() == []:
            self.gt = None
            move_sequence = self.game.moves
            i = -1
            check_stone = self.board.get_stone(move_sequence[i][1], move_sequence[i][2])

            while len(check_stone.get_neighbours()) == check_stone.max_num_neighbours:
                i -= 1
            check_stone = self.board.get_stone(move_sequence[i][1], move_sequence[i][2])
            choices = [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
                       (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)]
            coord = random.choice(choices)
            while (coord in check_stone.neighbours) or coord[0] in [-1, 9] or coord[1] in [-1, 9]:
                choices.remove(coord)
                coord = random.choice(
                    [(check_stone.x + 1, check_stone.y), (check_stone.x - 1, check_stone.y),
                     (check_stone.x, check_stone.y + 1), (check_stone.x, check_stone.y - 1)])

            return coord
        else:
            max_win_prob = -9999
            for subtree in self.gt.get_subtrees():
                if subtree.win_probability > max_win_prob:
                    max_win_prob = subtree.win_probability
                    best_choice = subtree
            return best_choice.move
