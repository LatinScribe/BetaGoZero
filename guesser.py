""" AI FILE"""
import board

import game
import GameTree
import random


class AbstractGoAi:
    """An abstract go ai class"""
    board: board.Board
    gt: GameTree.GameTree
    game: game.Game

    def __init__(self, gt, game_, size=9):
        self.board = board.Board(size)
        self.gt = gt
        self.game = game_

    def make_move(self):
        raise NotImplementedError


class RandomGoAi(AbstractGoAi):

    def __init__(self, gt: GameTree, size=9):
        self.board = board.Board(size)
        self.gt = gt

    def make_move(self):
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
