"""
This Python script reads Smart Game Format (SGF) files for Go games and checks if they have a valid result.
If a file does not have a valid result, it can optionally be deleted. The script can process all SGF files
in a given folder.

Functions:
- read_sgf(file_name: str, file_directory: str, do_deletion: bool): Reads a single SGF file and checks
if it has a valid result. If it does not have a valid result and do_deletion is True, the file will be deleted.
- read_all_sgf_in_folder(folder_directory: str, do_deletion: bool = False): Reads all SGF files in a folder
and calls read_sgf for each file.

Parameters:
- file_name (str): The name of the SGF file to read.
- file_directory (str): The directory where the SGF file is located.
- do_deletion (bool): If True and the SGF file does not have a valid result, the file will be deleted.

Usage:
- Modify the value of games_folder_path_absolute or games_folder_path_relative to the path of the folder
containing the SGF files.
- Call read_all_sgf_in_folder to process all SGF files in the folder. Set do_deletion to True if you want
to delete files without a valid result.

Note:
- requires the os and board modules to be imported
"""
from __future__ import annotations
import os
import shutil
import board as b
import GameTree as gt


def read_sgf(file_name: str, file_directory: str, do_deletion: bool) -> None | b.Board:
    """
    Reads a single SGF file and checks if it has a valid result. If it does not have a valid result and
    do_deletion is True, the file will be deleted.

    Return None if the file is being deleted

    Args:
        file_name (str): The name of the SGF file to read.
        file_directory (str): The directory where the SGF file is located.
        do_deletion (bool): If True and the SGF file does not have a valid result, the file will be deleted.
    """
    with open(file_directory + file_name) as sgf_file:
        header = sgf_file.readline()
        if header.find('RE') == -1:
            print("Game does not have a valid result, unusable.")
            if do_deletion:
                print("Proceeding with deletion.")
                try:
                    # shutil.move(file_directory + file_name, "/DataSet/Unusable//" + file_name) does not work
                    os.remove(file_directory + file_name)
                except FileNotFoundError:
                    print("Fail. File was not found.")
                else:
                    print("Success. File deleted.")
                    return
        else:
            print(f"Game has a valid result of {header[header.index('RE') + 2:header.index('KM')]} aka is usable.")
            sgf_file.readline()
            sgf_file.readline()
            game = sgf_file.readline().split(';')
            game = game[1:-2]
            board = b.Board(9)
            for stone in game:
                if stone[-2:] != "[]":  # is not a pass
                    x = ord(stone[2]) - 97
                    y = ord(stone[3]) - 97
                    if stone[0] == "B":
                        board.add_stone(x, y, "Black")
                    elif stone[0] == "W":
                        board.add_stone(x, y, "White")
            # print(board)
    return board


def read_all_sgf_in_folder(folder_directory: str, do_deletion: bool = False):
    """
    Reads all SGF files in a folder and calls read_sgf for each file.

    Args:
        folder_directory (str): The directory containing the SGF files.
        do_deletion (bool): If True and the SGF file does not have a valid result, the file will be deleted.
    """
    for file in os.listdir(folder_directory):
        read_sgf(file, folder_directory, do_deletion)


def sgf_to_game_sequence(file_name: str, file_directory: str) -> list[tuple[int, int, int]]:
    """
    Reads an SGF file and converts it into a sequence of moves for the GameTree
    # TODO: finish the docstring
    :param file_name:
    :param file_directory:
    :return move_seq:
    """
    with open(file_directory + file_name) as sgf_file:
        header = sgf_file.readline()
        if header.find('RE') != -1:
            sgf_file.readline()
            sgf_file.readline()
            game = sgf_file.readline().split(';')
            game = game[1:]
            move_seq = []
            i = 1  # index of turn, starts at 1 (0 is the default, placeholder move)
            for stone in game:
                if stone[-2:] == "[]":  # is a pass
                    move_seq.append((i, -1, -1))
                else:
                    x = ord(stone[2]) - 97
                    y = ord(stone[3]) - 97
                move_seq.append((i, x, y))
                i += 1
            return move_seq
        else:
            raise ValueError


def sgf_folder_to_tree(folder_directory: str) -> gt.GameTree:
    """Returns a game tree by exctracting move sequences out of all sgf files in a given folder

    Preciditions:
    - all files have to be sgf
    """
    tree = gt.GameTree()
    for file in os.listdir(folder_directory):
        tree.insert_move_sequence(sgf_to_game_sequence(file, folder_directory))
    return tree

def rotate_move_seq_by_90(moves: list[tuple[int, int, int]], board_size=9) -> list[tuple[int, int, int]]:
    """rotates a sequence of moves clockwise by 90 degrees"""
    rotated_sequence = []
    id_added = 1000  # TODO: modify this (possibly with reference to total number of moves in data set)
    for move in moves:  # TODO: check if this works
        new_move = (id_added + move[0], move[2], board_size - move[1])
        rotated_sequence.append(new_move)
    return rotated_sequence


if __name__ == '__main__':
    # All of this is for debugging
    # TODO: prints multiple times, fix when it should and should not print
    games_folder_path_absolute = '/Users/dmitriivlasov/Downloads/go9/'
    games_folder_path_relative = 'DataSet/2015-Go9/'
    # read_all_sgf_in_folder(games_folder_path_relative, True)
    go9folder_game_tree = sgf_folder_to_tree(games_folder_path_relative)
    print(go9folder_game_tree)
    # print(f"length of the go9 tree: {len(go9folder_game_tree)}")
