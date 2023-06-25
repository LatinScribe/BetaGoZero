"""Beta-Go-Zero: AI for playing Go built with python

Author:
Henry "TJ" Chen

Original project by:
Henry "TJ" Chen
Dmitrii Vlasov
Ming Yau (Oscar) Lam
Duain Chhabra

Version: 1.3

Module Description
==================

This module contains a python class that is used to represent a Tree of possible move
sequences in a game of Go.

See README file for instructions, project details, and the relevant copyright and usage information
"""

from __future__ import annotations
from typing import Optional
from game import Game

GAME_START_MOVE = (0, -1, -1)
PASS_MOVE = (-1, -1, -1)


class GameTree:
    """A decision tree for Beta-GO moves

    Each node in the tree stores a GO move.

    Instance Attributes:
        - move: the current move (spot on the board), or (0, -1, -1) if this tree represents the start of a game
        - _subtrees: the dictionary of the subtrees of the game trees, with keys corresponding to the moves
        - win_probability: probability of going down this branch  (backpropagation)  #: assume win probability for black
    Representation Invariants:
        - self.move[0]>=-1 and self.move[1]>=-1 and self.move[2]>=-1
        - all(self._subtrees[subtree].move==subtree for subtree in self._subtrees)
    """
    move: tuple[int, int, int]
    _subtrees: dict[tuple[int, int, int], GameTree]
    win_probability: float

    def __init__(self, move: tuple[int, int, int] = GAME_START_MOVE,
                 win_probability: float = 0.0) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments.

        >>> game = GameTree()
        >>> game.move == GAME_START_MOVE
        True
        """
        self.move = move
        self._subtrees = {}
        self.win_probability = win_probability

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return list(self._subtrees.values())

    def find_subtree_by_move(self, move: tuple[int, int, int]) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        if move in self._subtrees:
            return self._subtrees[move]
        else:
            return None

    def is_black_turn(self) -> bool:
        """Return whether the CURRENT move should was made by black."""
        return self.move[0] > 0 and self.move[0] % 2 == 1

    def __len__(self) -> int:
        """Return the number of items in this tree."""
        # Note: no "empty tree" base case is necessary here.
        # Instead, the only implicit base case is when there are no subtrees (sum returns 0).
        return 1 + sum(subtree.__len__() for subtree in self._subtrees.values())

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.

        You MAY change the implementation of this method (e.g. to display different instance attributes)
        as you work on this assignment.

        Preconditions:
            - depth >= 0
        """
        #  check whether it's working correctly
        # seems to be
        if self.move[0] == 0:
            turn_desc = "Game start:"
        elif self.is_black_turn():
            turn_desc = "Black's move:"
        else:
            turn_desc = "White's move:"
        move_desc = f'{turn_desc} {self.move} ({self.win_probability})\n'
        str_so_far = '  ' * depth + move_desc
        for subtree in self._subtrees.values():
            str_so_far += subtree._str_indented(depth + 1)
        return str_so_far

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees[subtree.move] = subtree

    def insert_move_sequence(self, moves: list[tuple[int, int, int]], probability: float) -> None:
        """Insert the given move sequence with this tree as the parent"""
        #: potentially add the proability to the parameters
        self._insert_move_sequence_helper(moves, 0, probability)
        self.update_win_probability()

    def _insert_move_sequence_helper(self, moves: list[tuple[int, int, int]], current_index: int,
                                     probability: float) -> None:
        """helps, hopefully - helper function for insert_move_sequence"""
        #  add parents to trees
        if current_index == len(moves):
            self.win_probability = probability
            return
        elif moves[current_index] not in self._subtrees:
            self.add_subtree(GameTree(moves[current_index], probability))  # added parent here
        self._subtrees[moves[current_index]]._insert_move_sequence_helper(moves, current_index + 1, probability)

    def update_win_probability(self) -> None:
        """updates the probability of 1 branch use this method after it creates after 1 complete game is added."""
        if not self._subtrees:
            return
        else:
            for subtree in self._subtrees.values():
                subtree.update_win_probability()
        probabilities = [subtree.win_probability for subtree in self.get_subtrees()]
        self.win_probability = sum(probabilities) / len(probabilities)

    def insert_game_into_tree(self, game: Game) -> None:
        """Insert a game into a tree as a sequence,
        with the leaf probability of territory score at the end of the game."""
        #  fix the output of calculate_score and adjust this method accordingly
        victory_score = game.overall_score()[1] - game.overall_score()[0]
        self.insert_move_sequence(game.moves, victory_score)

    def insert_game_into_tree_absolute(self, game: Game) -> None:
        """Insert a game into a tree as a sequence,
        with the leaf probability of territory score at the end of the game."""
        #  fix the output of calculate_score and adjust this method accordingly
        if game.overall_score()[1] - game.overall_score()[0] > 0:
            victory_score = 1
        else:
            victory_score = 0
        self.insert_move_sequence(game.moves, victory_score)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
