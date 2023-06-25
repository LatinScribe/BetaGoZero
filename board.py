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

This module contains python classes which represent the actual components to
a game of Go - the board and the stones.

See README file for instructions, project details, and the relevant copyright and usage information
"""

from __future__ import annotations
from typing import Optional
# rom typing import Dict, Tuple


class Board:
    """
    A class that represents the game board.

    Attributes:
        size (int): The size of the board (i.e. the number of rows and columns).
        grid (list): A 2D list representing the board, containing Stone objects.
    """
    size: int
    grid: list[list[Stone]]

    def __init__(self, size: Optional[int] = 9) -> None:
        """
        Initializes a Board object. Populates all valid positions with "imaginary stones" of
        neither colour - in reality, these stones would not exist on the board - it is
        our way of representing an empty board. Then, update all the stones to have the correct
        neighbours.

        Args:
            size (int): The size of the board. Defaults to 9.
        """
        self.size = size
        self.grid = [[Stone(x, y) for y in range(size)] for x in range(size)]

        for column in self.grid:
            for stone in column:
                if stone.x + 1 < size:
                    stone.add_neighbour(self.get_stone(stone.x + 1, stone.y))
                if stone.x - 1 >= 0:
                    stone.add_neighbour(self.get_stone(stone.x - 1, stone.y))
                if stone.y + 1 < size:
                    stone.add_neighbour(self.get_stone(stone.x, stone.y + 1))
                if stone.y - 1 >= 0:
                    stone.add_neighbour(self.get_stone(stone.x, stone.y - 1))

    def __getitem__(self, position: tuple[int, int]) -> Stone:
        """
        Returns the Stone object at the specified position.

        Args:
            position (tuple): A tuple containing the x and y coordinates of the Stone object.

        Returns:
            Stone: The Stone object at the specified position.
        """
        x, y = position
        return self.grid[x][y]

    def add_stone(self, x: int, y: int, color: str = "Neither") -> None:
        """
        Adds a Stone object to the board at the specified position.

        Args:
            x (int): The x-coordinate of the position.
            y (int): The y-coordinate of the position.
            color (str): The color of the stone. Defaults to "Neither".
        Preconditions:
            - x<self.size and y<self.size and 0<=x and 0<=y
        """
        self.grid[x][y].color = color

    def get_stone(self, x: int, y: int) -> Stone:
        """Return the stone situated at the given coordinates"""
        return self.grid[x][y]

    # pretty useless methods
    def remove_stones(self, stones: list[Stone]) -> None:
        """
        Removes the specified Stone objects from the board.

        Args:
            stones (list): A list of Stone objects to remove.
        Preconditions:
            - all((stone in self.grid) for stone in stones)
        """
        for stone in stones:
            self.grid[stone.x][stone.y].die()

    def get_dead_stones(self) -> list[Stone]:
        """
        Returns a list of Stone objects that should be removed from the board.

        Returns:
            list: A list of Stone objects that should be removed.
        """
        dead_stones = []
        for x in range(self.size):
            for y in range(self.size):
                stone = self.grid[x][y]
                if stone.color != "Neither" and stone.count_neighbours() >= stone.max_num_neighbours:
                    dead_stones.append(stone)
        return dead_stones

    def __str__(self) -> str:
        """Print a visual representation of the board."""
        ans = "-" * (self.size * 2 + 1) + '\n'
        for y in range(self.size):
            row = "|"
            for x in range(self.size):
                stone = self.get_stone(x, y)
                if stone.color == "Black":
                    row += "○"
                elif stone.color == "White":
                    row += "●"
                else:
                    row += " "
                row += "|"
            ans += row + '\n'
            ans += "-" * (self.size * 2 + 1) + '\n'
        return ans

    def print_max_neighbours(self) -> str:
        """for debugging"""
        ans = "-" * (self.size * 2 + 1) + '\n'
        for y in range(self.size):
            row = "|"
            for x in range(self.size):
                stone = self.get_stone(x, y)
                row += str(stone.max_num_neighbours)
                row += "|"
            ans += row + '\n'
            ans += "-" * (self.size * 2 + 1) + '\n'
        return ans

    def board_to_move_sequence(self) -> list[tuple[int, int, int]]:
        """Convert a board state into a sequence of moves, store as a list of tuples
        NOTE: This does not store the sequence that the moves were actually played in
        """
        sequence = []
        i = 0
        for row in self.grid:
            for stone in row:
                sequence.append((i, stone.x, stone.y))
                i += 1
        return sequence

    def is_valid_move(self, x: int, y: int, color: str) -> bool:
        """Check if a coordinate is valid for the board. It does not overwrite any stone, is not placed in a location
        that leads to instant death, and within boundaries of the board.

        NOTE: It does not (and should not) mutate the board

        Preconditions:
            - color in {'Black' , 'White'}
        """
        stone = self.get_stone(x, y)
        if color not in {'Black', 'White'}:
            raise ValueError
        elif x < 0 or x > 8 or y < 0 or y > 8:
            return False
        elif self.get_stone(x, y).color != "Neither":
            return False

        else:
            stone.color = color
            if any(neighbour.check_is_dead(set()) for neighbour in stone.neighbours.values()):
                stone.color = 'Neither'
                return True

            elif stone.check_is_dead(set()):
                stone.color = 'Neither'
                return False
            else:
                stone.color = 'Neither'
        return True

    def is_valid_coord(self, x: int, y: int) -> bool:
        """Check if a coordinate is valid for the board."""
        return 0 <= x < self.size and 0 <= y < self.size

    def calculate_score(self: Board, technique: str) -> list[list[tuple[int, int]], list[tuple[int, int]]]:
        """Calculates the score for both players.
        """
        black_score, white_score = 0.0, 0.0
        black_territory, white_territory = 0, 0
        black_territory_cord, white_territory_cord = [], []

        for x in range(self.size):
            for y in range(self.size):
                # This code is relevant if you want to count the stones as well
                # stone = self.get_stone(x, y)
                # if stone.color == "Black":
                #     black_score += 1
                # elif stone.color == "White":
                #     white_score += 1
                # else:

                # Captured stones are not counted as territory
                territory_owner = self.get_territory_owner(x, y, technique)
                if territory_owner == "Black":
                    black_territory += 1
                    black_territory_cord.append((x, y))
                elif territory_owner == "White":
                    white_territory += 1
                    white_territory_cord.append((x, y))

        black_score += black_territory
        white_score += white_territory
        return [black_territory_cord, white_territory_cord]

    def is_valid_coord_do(self, x: int, y: int) -> bool:
        """Check if a coordinate is valid for the board."""
        return 0 <= x < self.size and 0 <= y < self.size

    def get_territory_owner(self: Board, x: int, y: int, technique: str = "flood_fill") -> str:
        """Determines the owner of the territory at the given coordinates.
            Flood_fill is a recursive algorithm that checks if the territory is surrounded by one color. it includes the
            current stone in the check and rest of the stones on board.
            DFS is a recursive algorithm that checks if the territory is surrounded by one color. it does not include
            the current stone in the check and only checks territory on the board."""

        def dfs(x_pos: int, y_pos: int, visited: set) -> set[str]:
            """
            Using a similar approach from A3
            """
            if (x_pos, y_pos) in visited:  # if we have already visited this stone, return an empty set
                return set()
            visited.add((x_pos, y_pos))

            neighbors = self.get_stone(x_pos, y_pos).get_neighbours()  # get the neighbours of the stone
            result = set()
            for nx, ny in neighbors:
                if self.is_valid_coord_do(nx, ny) and (nx, ny) not in visited:
                    stone = self.get_stone(nx, ny)
                    if stone.color == "Neither":
                        result = result.union(dfs(nx, ny, visited))
                    else:
                        result.add(stone.color)
            return result

        def flood_fill(x_pos: int, y_pos: int, visited: set) -> set[str]:
            """
            Flood fill algorithm to determine the territory owner
            """
            if (x_pos, y_pos) in visited or not self.is_valid_coord_do(x_pos, y_pos):
                return set()

            visited.add((x_pos, y_pos))
            stone = self.get_stone(x_pos, y_pos)
            if stone.color != "Neither":
                return {stone.color}

            neighbors = stone.get_neighbours()
            result = set()
            for nx, ny in neighbors:
                result = result.union(flood_fill(nx, ny, visited))
            return result

        visitedd = set()
        if technique == "flood_fill":
            stone_colors = flood_fill(x, y, visitedd)
        else:
            stone_colors = dfs(x, y, visitedd)

        # stone_colors = (x, y, visited)
        if len(stone_colors) == 1:
            return next(iter(stone_colors))
        else:
            return "Neither"

    def get_dead_cells(self, color: str) -> list[tuple[int, int]]:
        """Function to get dead cells for a given color on a board.
           WIP and it does not work yet. or capture stones."""

    def capture_stones(self, stone: Stone) -> int:
        """turns all same color stones connected to the given stone into Neither
        Preconditions:
            - Assume the given stone is dead
            - any([(stone in row) for row in self.grid])
        """
        if stone.color not in {'Black', 'White'}:
            raise ValueError
        else:
            captured_so_far = 1
            color = stone.color
            stone.color = 'Neither'
            for neighbour in stone.neighbours.values():
                if neighbour.color == color:
                    captured_so_far += self.capture_stones(neighbour)
            return captured_so_far


class Stone:
    """
    A class representing a stone on a game board.

    Attributes:
        color (str): The color of the stone ("Black", "White", or "Neither").
        x (int): The x position of the stone on the board.
        y (int): The y position of the stone on the board.
        neighbours (dict): A dict of neighbouring Stone objects with (x, y) as keys.

    Methods:
        add_neighbour(neighbor): Adds a neighbour to the stone.
        remove_neighbour(neighbor): Removes a neighbour from the stone.
        count_neighbours(): Returns the number of neighbours the stone has.
        die(): Removes the stone and its connections from the board.
    """

    color: str
    x: int
    y: int
    neighbours: dict[tuple[int, int], Stone]
    max_num_neighbours: int

    def __init__(self, x: int, y: int, color: str = "Neither") -> None:
        """
        Initializes a new stone with the specified color and position.

        Args:
            color (str, optional): The color of the stone. Defaults to "Neither".
            x (int): The x position of the stone on the board.
            y (int): The y position of the stone on the board.
        """
        self.color = color
        self.neighbours = {}
        self.x = x
        self.y = y
        max_neighbours = 4  # default for stones not on edge or corner
        if x == 0 or x == 8:  # stone is on left or right edge
            max_neighbours = 3
        elif y == 0 or y == 8:  # stone is on top or bottom edge
            max_neighbours = 3
        if (x == 0 and y == 0) or (x == 0 and y == 8) or (x == 8 and y == 0) or (x == 8 and y == 8):
            max_neighbours = 2  # stone is in a corner
        self.max_num_neighbours = max_neighbours

    def __str__(self) -> str:
        return f'Stone on coordinates {self.x}, {self.y} is {self.color} and has {self.count_neighbours()} neighbours.'

    def add_neighbour(self, neighbour: Stone) -> None:
        """
        Adds a neighbour to the stone if it is adjacent to the stone.

        Args:
            neighbour (Stone): The neighbouring stone to add.
        """
        # Check if the neighbor is adjacent to the current stone
        if abs(self.x - neighbour.x) + abs(self.y - neighbour.y) == 1:
            self.neighbours[neighbour.x, neighbour.y] = neighbour
            neighbour.neighbours[self.x, self.y] = self
        else:
            raise Exception

    def remove_neighbour(self, neighbour: Stone) -> None:
        """
        Removes a neighbour from the stone.

        Effectively deletes the connection between two stones.

        Args:
            neighbour (Stone): The neighbouring stone to remove.
        """
        del self.neighbours[(neighbour.x, neighbour.y)]
        del neighbour.neighbours[(self.x, self.y)]

    def count_neighbours(self) -> int:
        """
        Returns the number of neighbours the stone has.

        Returns:
            int: The number of neighbours the stone has.
        """
        return len(self.neighbours)

    def get_neighbours(self) -> dict[tuple[int, int], Stone]:
        """
        Returns a set of neighbouring Stone objects.

        Returns:
            set: A set of neighbouring Stone objects.
        """
        return self.neighbours

    #  potentially move to Stone
    def update_neighbours(self) -> None:
        """
        Updates the neighboring Stone objects for each Stone object on the board.
        """
        neighbours = self.get_neighbours().values()
        for neighbour in neighbours:
            if neighbour.color != "Neither":
                self.add_neighbour(neighbour)
            else:
                self.remove_neighbour(neighbour)

    # check this, probably not nesscary - don't need to delete the connections
    def die(self) -> None:
        """
        Removes the stone and its connections from the board.
        """
        for neighbour in self.neighbours.values():
            neighbour.remove_neighbour(self)
        self.color = "Neither"
        self.neighbours = {}

    def check_is_dead(self, visited: set[Stone]) -> bool:
        """this function checks if the stone is dead
        visited should be an empty set"""
        if self.color == "Neither":
            return False
        elif len([neighbour for neighbour in self.neighbours.values() if
                  neighbour.color != 'Neither']) < self.max_num_neighbours:
            return False
        elif all(((neighbour.color not in {self.color, 'Neither'}) or (neighbour in visited)) for neighbour in
                 self.neighbours.values()):
            return True
        else:
            visited.add(self)
            bools = []
            for neighbour in self.neighbours.values():
                if neighbour not in visited and neighbour.color == self.color:
                    bools.append(neighbour.check_is_dead(visited))
            return all(bools)

    def get_liberties(self, color: str) -> int:
        """Returns the number of liberties the stone has.
        TODO: Experimental Function"""
        liberties = 0
        for neighbour in self.neighbours.values():
            if neighbour.color == "Neither":
                liberties += 1
            elif neighbour.color != color:
                liberties += 1
        return liberties


if __name__ == '__main__':
    # Create a new 9x9 board
    board = Board(9)
    # print(board[(1, 5)])
    # print(board)
    # board.add_stone(1, 5, "Black")
    # print(board[(1, 5)])
    # print(board)
    # board.add_stone(1, 6, "White")
    # print(board[(1, 5)])
    # print(board[(1, 6)])
    # # print(board)
    # print(board.print_max_neighbours())
    board.grid[8][0].color = 'White'
    board.grid[7][0].color = 'White'
    # board.capture_stones(board.grid[7][0])
    board.grid[8][1].color = 'Black'
    board.grid[7][1].color = 'Black'
    board.grid[6][0].color = 'Black'
    print(board.grid[7][0].check_is_dead(set()))

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
