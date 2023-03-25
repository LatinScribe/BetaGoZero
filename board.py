# TODO: rewrite so that the board starts with the complete graph (maybe not, coz running time)
from __future__ import annotations


class Board:
    """
    A class that represents the game board.

    Attributes:
        size (int): The size of the board (i.e. the number of rows and columns).
        grid (list): A 2D list representing the board, containing Stone objects.
    """

    def __init__(self, size=9):
        """
        Initializes a Board object.

        Args:
            size (int): The size of the board. Defaults to 9.
        """
        self.size = size
        self.grid = [[Stone(x, y) for y in range(size)] for x in range(size)]

    def __getitem__(self, position):
        """
        Returns the Stone object at the specified position.

        Args:
            position (tuple): A tuple containing the x and y coordinates of the Stone object.

        Returns:
            Stone: The Stone object at the specified position.
        """
        x, y = position
        return self.grid[x][y]

    def add_stone(self, x, y, color="Neither"):
        """
        Adds a Stone object to the board at the specified position.

        Args:
            x (int): The x-coordinate of the position.
            y (int): The y-coordinate of the position.
            color (str): The color of the stone. Defaults to "Neither".
        """
        self.grid[x][y].color = color
        # TODO: add neighbours implementation

    def get_stone(self, x, y):
        return self.grid[x][y]

    # pretty useless methods
    def remove_stones(self, stones):
        """
        Removes the specified Stone objects from the board.

        Args:
            stones (list): A list of Stone objects to remove.
        """
        for stone in stones:
            self.grid[stone.x][stone.y].die()

    def get_dead_stones(self):
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

    def __str__(self):
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

    def print_max_neighbours(self):
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
        sequence = []
        i = 0
        for row in self.grid:
            for move in row:
                sequence.append((i, move.x, move.y))
                i += 1
        return sequence


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

    def __init__(self, x, y, color="Neither"):
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
        # TODO: maybe make it work for other sizes of boards? also potentially cash the whole thing

    def __str__(self):
        return f'Stone on coordinates {self.x}, {self.y} is {self.color} and has {self.count_neighbours()} neighbours.'

    def add_neighbour(self, neighbour):
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
            print('You fucked up the neighbours')
            raise Exception

    def remove_neighbour(self, neighbour):
        """
        Removes a neighbour from the stone.

        Args:
            neighbour (Stone): The neighbouring stone to remove.
        """
        self.neighbours[(neighbour.x, neighbour.y)] = None
        neighbour.neighbours[(self.x, self.y)] = None

    def count_neighbours(self):
        """
        Returns the number of neighbours the stone has.

        Returns:
            int: The number of neighbours the stone has.
        """
        return len(self.neighbours)

    def get_neighbours(self):
        """
        Returns a set of neighbouring Stone objects.

        Returns:
            set: A set of neighbouring Stone objects.
        """
        return self.neighbours.values()

    # TODO: potentially move to Stone
    def update_neighbours(self,):
        """
        Updates the neighboring Stone objects for each Stone object on the board.
        """
        neighbours = self.get_neighbours()
        for neighbour in neighbours:
            if neighbour.color != "Neither":
                self.add_neighbour(neighbour)
            else:
                self.remove_neighbour(neighbour)

    # TODO: potentially move to Board
    def die(self):
        """
        Removes the stone and its connections from the board.
        """
        for neighbour in self.neighbours.values():
            neighbour.remove_neighbour(self)
        self.color = "Neither"
        self.neighbours = {}


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
    # print(board)
    print(board.print_max_neighbours())
