from board import Board
from sgf_reader import read_sgf
from go_gui import draw_board




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
