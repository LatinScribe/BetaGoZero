from board import Board
from sgf_reader import read_sgf
from go_gui import draw_board
from game import Game

board = Board(9)


def get_dead_cells(board, color) -> list[tuple[int, int]]:
    dead_cells = []

    for x in range(board.size):
        for y in range(board.size):
            stone = board.get_stone(x, y)
            if stone.color == color:
                liberties = board.get_stone(x, y).get_liberties(color)
                if liberties == 0:
                    dead_cells.append((x, y))
    print("dead cells", dead_cells, "color", color)
    return dead_cells


def calculate_score(board: Board):
    """Calculates the score for both players."""
    black_score, white_score = 0.0, 0.0
    black_territory, white_territory = 0, 0
    black_territory_cord, white_territory_cord = [], []

    for x in range(board.size):
        for y in range(board.size):
            stone = board.get_stone(x, y)
            # if stone.color == "Black":
            #     black_score += 1
            # elif stone.color == "White":
            #     white_score += 1
            # else:
            territory_owner = get_territory_owner(board, x, y)
            if territory_owner == "Black":
                black_territory += 1
                black_territory_cord.append((x, y))
            elif territory_owner == "White":
                white_territory += 1
                white_territory_cord.append((x, y))
    # # #
    # for i in get_dead_cells(board, "Black"):
    #     white_territory_cord.append(i)
    # for i in get_dead_cells(board, "White"):
    #     black_territory_cord.append(i)

    black_score += black_territory
    white_score += white_territory
    return [("Black score:", black_score, "WhiteScore:", white_score), black_territory_cord, white_territory_cord]


def get_territory_owner(board: Board, x, y) -> str:
    """Determines the owner of the territory at the given coordinates."""

    def dfs(x, y, visited):
        if (x, y) in visited:  # if we have already visited this stone, return an empty set
            return set()
        visited.add((x, y))

        neighbors = board.get_stone(x, y).get_neighbours()  # get the neighbours of the stone
        result = set()
        for nx, ny in neighbors:
            if board.is_valid_coord(nx, ny) and (nx, ny) not in visited:
                stone = board.get_stone(nx, ny)
                if stone.color == "Neither":
                    result = result.union(dfs(nx, ny, visited))
                else:
                    result.add(stone.color)
        return result

    visited = set()
    stone_colors = dfs(x, y, visited)
    if len(stone_colors) == 1:
        return next(iter(stone_colors))
    else:
        return "Neither"


sgf_reader = read_sgf("/2015-07-19T12_32_03.406Z_ycdor3fuul2s.sgf", "DataSet/2015-Go9", False)
# print(sgf_reader)
xop = calculate_score(sgf_reader)
draw_board(sgf_reader, "hello.jpg")
print(xop)
game = Game()
for x in xop[-1]:
    x_y, y_z = x

    game.add_move_using_color("White", x_y, y_z)

for x in xop[-2]:
    x_y, y_z = x

    game.add_move_using_color("Black", x_y, y_z)
print(len(xop[-1]))
print(len(xop[-2]))


draw_board(game.board, "hello2.jpg")

# sgf_reader_2 = read_sgf("/2015-07-19T12_32_03.406Z_ycdor3fuul2s.sgf", "DataSet/2015-Go9", False)
# xop = calculate_score(sgf_reader_2)
# draw_board(sgf_reader_2, "pollo.jpg")
# print(xop)
#
#
# sgf_reader_2 = read_sgf("/2015-07-19T12_40_05.361Z_ds8v8n0s4al0.sgf", "DataSet/2015-Go9", False)
# xop = calculate_score(sgf_reader_2)
# draw_board(sgf_reader_2, "pollooo.jpg")
# print(xop)
