"""CSC111 Project: Beta-Go
===============================

This Python module contains the GameTree class that will represent each game
"""
from __future__ import annotations
from typing import Optional


GAME_START_MOVE = (0, -1, -1)
PASS_MOVE = (-1, -1, -1)


class GameTree:
    """A decision tree for Beta-GO moves

    Each node in the tree stores a GO move.

    Instance Attributes:
        - _parent: the parent of the game tree, None if it is the root
        - move: the current move (spot on the board), or (0, -1, -1) if this tree represents the start of a game
        - _subtrees: the dictionary of the subtrees of the game trees, with keys corresponding to the moves
        - win_probability: probability of going down this branch (backpropagation)
    TODO: finish the docstring
    """
    _parent: None | GameTree
    move: tuple[int, int, int]
    _subtrees: dict[tuple[int, int, int], GameTree]
    win_probability: float

    def __init__(self, parent: None | GameTree = None, move: tuple[int, int, int] = GAME_START_MOVE, win_probability: float = 0.0) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments.

        >>> game = GameTree()
        >>> game.move == GAME_START_MOVE
        True
        """
        self._parent = parent
        self.move = move
        self._subtrees = {}
        self.win_probability = win_probability

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return list(self._subtrees.values())

    def get_parent(self) -> GameTree:
        """Return the parent of this game tree."""
        return self._parent

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
        # TODO: check whether it's working correctly
        # seems to be
        if self.move[0] == 0:
            turn_desc = "Game start:"
        elif self.is_black_turn():
            turn_desc = "Black's move:"
        else:
            turn_desc = "White's move:"
        move_desc = f'{turn_desc} {self.move}\n'
        str_so_far = '  ' * depth + move_desc
        for subtree in self._subtrees.values():
            str_so_far += subtree._str_indented(depth + 1)
        return str_so_far

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees[subtree.move] = subtree

    def insert_move_sequence(self, moves: list[tuple[int, int, int]], probability: float = 0.0) -> None:
        """Insert the given move sequence with this tree as the parent"""
        # TODO: potentially add the proability to the parameters
        self._insert_move_sequence_helper(moves, 0)

    def _insert_move_sequence_helper(self, moves: list[tuple[int, int, int]], current_index: int) -> None:
        """helps, hopefully"""
        # TODO: add parents to trees
        if current_index == len(moves):
            return
        if moves[current_index] not in self._subtrees:
            self.add_subtree(GameTree(self._parent, moves[current_index]))  # added parent here
        # self._update_win_probability()
        self._subtrees[moves[current_index]]._insert_move_sequence_helper(moves, current_index + 1)

    # TODO: the backpropagation_step
    def _update_win_probability(self) -> None:
        """Recalculate the guesser win probability of this tree.

        Note: like the "_length" Tree attribute from tutorial, you should only need
        to update self here, not any of its subtrees. (You should *assume* that each
        subtree has the correct guesser win probability already.)

        Use the following definition for the guesser win probability of self:
            - if self is a leaf, don't change the guesser win probability
              (leave the current value alone)
            - if self is not a leaf and self.is_guesser_turn() is True, the guesser win probability
              is equal to the MAXIMUM of the guesser win probabilities of its subtrees
            - if self is not a leaf and self.is_guesser_move is False, the guesser win probability
              is equal to the AVERAGE of the guesser win probabilities of its subtrees
        """
        ...


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
