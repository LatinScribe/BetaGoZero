from board import Board
from sgf_reader import read_sgf
from go_gui import draw_board


board = Board(9)

def calculate_score(board:Board) -> tuple[float, float]:
    """Calculates the score for both players."""
    black_score, white_score = 0.0, 0.0
    black_territory, white_territory = 0, 0

    for x in range(board.size):
        for y in range(board.size):
            stone = board.get_stone(x, y)
            if stone.color == "Black":
                black_score += 1
            elif stone.color == "White":
                white_score += 1
            else:
                territory_owner = get_territory_owner(board, x, y)
                if territory_owner == "Black":
                    black_territory += 1
                elif territory_owner == "White":
                    white_territory += 1

    black_score += black_territory
    white_score += white_territory
    return black_score, white_score

def get_territory_owner(board:Board, x, y) -> str:
    """Determines the owner of the territory at the given coordinates."""

    def dfs(x, y, visited):
        if (x, y) in visited:
            return set()
        visited.add((x, y))

        neighbors = board.get_stone(x, y).get_neighbours()
        # print(neighbors)
        result = set()
        for nx, ny in neighbors:
            if board.is_valid_coord(nx, ny) and (nx, ny) not in visited:
                stone = board.get_stone(nx, ny)
                if stone.color == "Neither":
                    result |= dfs(nx, ny, visited)
                else:
                    result.add(stone.color)
        return result

    visited = set()
    stone_colors = dfs(x, y, visited)
    if len(stone_colors) == 1:
        return next(iter(stone_colors))
    else:
        return "Neither"


sgf_reader = read_sgf("/2015-06-30T13_28_05.990Z_j15601s5g8gk.sgf","DataSet/2015-Go9", False)
print(sgf_reader)
xop = calculate_score(sgf_reader)
draw_board(sgf_reader)
print(sgf_reader.get_stone(0, 0))
print(sgf_reader.get_stone(8, 0))
print(sgf_reader.get_stone(8, 8))
print(sgf_reader.get_stone(0, 8))
print(sgf_reader.get_stone(0, 0).neighbours)
print(xop)

# sgf_reader_2 = read_sgf("/2015-07-19T12_32_03.406Z_ycdor3fuul2s.sgf","DataSet/2015-Go9", False)
# print(sgf_reader_2)
# xop = calculate_score(sgf_reader_2)
# draw_board(sgf_reader_2)
# print(sgf_reader_2.get_stone(0, 0).get_neighbours())
# print(xop)
