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

Copyright and Usage Information
===============================

This file was developed as part of the course project for CSC111 Winter 2023.
Feel free to test it out, but please contact us to obtain permission if you
intend to redistribute it or use it for your own work.
"""

from __future__ import annotations

import os
# from typing import Optional
import pickle
# import shutil
import board as b
import GameTree as Gt
from game import Game


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
            # Print some basic information about the game, helps with testing
            print(f"Game has a valid result of {header[header.index('RE') + 2:header.index('KM')]} aka is usable.")
            board_size = header[header.index('SZ') + 2:header.index('RE')]
            board_size = board_size.translate({ord(i): None for i in '[]'})
            num_size = int(board_size)
            print("Boardsize:", num_size)
            sgf_file.readline()
            sgf_file.readline()
            current_game = sgf_file.readline().split(';')
            current_game = current_game[1:-2]

            # generate the board class
            board = b.Board(size=num_size)
            for stone in current_game:
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
    boards = []
    for file in os.listdir(folder_directory):
        boards.append(read_sgf(file, folder_directory, do_deletion))
    return boards


def sgf_to_game_sequence(file_name: str, file_directory: str) -> tuple[list[tuple[int, int, int]], int]:
    """
    Reads an SGF file and converts it into a sequence of moves for the GameTree and a win state
    # TODO: finish the docstring
    :param file_name:
    :param file_directory:
    :return move_seq, win_state:
    """
    with open(file_directory + file_name) as sgf_file:
        header = sgf_file.readline()
        if header.find('RE') != -1:
            sgf_file.readline()
            sgf_file.readline()
            score_start_index = header.find('RE') + 3
            game_score_str = header[score_start_index: score_start_index + 3]
            if game_score_str[0] == 'B':
                game_score = int(game_score_str[2])  # if it is a victory by black, it is positive
            elif game_score_str[0] == 'W':  # if it is a victory by white, it is negative
                game_score = -1 * int(game_score_str[2])
            game = sgf_file.readline().split(';')
            game = game[1:]
            move_seq = []
            i = 1  # index of turn, starts at 1 (0 is the default, placeholder move)
            for stone in game:
                if stone[1:3] == "[]":  # is a pass
                    move_seq.append((i, -1, -1))
                else:
                    x = ord(stone[2]) - 97
                    y = ord(stone[3]) - 97
                    move_seq.append((i, x, y))
                i += 1
            return move_seq, game_score
        else:
            raise ValueError


def sgf_to_game_sequence_absolute(file_name: str, file_directory: str) -> tuple[list[tuple[int, int, int]], int]:
    """
    Reads an SGF file and converts it into a sequence of moves for the GameTree and a win state
    (pure wins or pure loses).
    """
    with open(file_directory + file_name) as sgf_file:
        header = sgf_file.readline()
        if header.find('RE') != -1:
            sgf_file.readline()
            sgf_file.readline()
            score_start_index = header.find('RE') + 3
            game_score_str = header[score_start_index: score_start_index + 3]
            if game_score_str[0] == 'B':
                game_score = 1  # if it is a victory by black, it is 1
            elif game_score_str[0] == 'W':
                game_score = 0  # if it is a victory by white, it is 0 (loss for black)
            game = sgf_file.readline().split(';')
            game = game[1:]
            move_seq = []
            i = 1  # index of turn, starts at 1 (0 is the default, placeholder move)
            for stone in game:
                if stone[1:3] == "[]":  # is a pass
                    move_seq.append((i, -1, -1))
                else:
                    x = ord(stone[2]) - 97
                    y = ord(stone[3]) - 97
                    move_seq.append((i, x, y))
                i += 1
            return move_seq, game_score
        else:
            raise ValueError


def sgf_to_game(file_name: str, file_directory: str) -> Game:
    """
    Reads an SGF file and converts it into a Game class
    """
    with open(file_directory + file_name) as sgf_file:

        # procress the given file
        header = sgf_file.readline()
        if header.find('RE') != -1:
            board_size = header[header.index('SZ') + 2:header.index('RE')]
            board_size = board_size.translate({ord(i): None for i in '[]'})
            num_size = int(board_size)
            sgf_file.readline()
            sgf_file.readline()
            current_game = sgf_file.readline().split(';')
            current_game = current_game[1:]

            # generating move sequence
            move_seq = []
            i = 1  # index of turn, starts at 1 (0 is the default, placeholder move)
            for stone in current_game:
                if stone[1:3] == "[]":  # is a pass
                    move_seq.append((i, -1, -1))
                else:
                    x = ord(stone[2]) - 97
                    y = ord(stone[3]) - 97
                move_seq.append((i, x, y))
                i += 1

            current_game = current_game[:-2]
            # generate the board class
            board = b.Board(size=num_size)
            for stone in current_game:
                if stone[1:3] != "[]":  # is not a pass
                    x = ord(stone[2]) - 97
                    y = ord(stone[3]) - 97
                    if stone[0] == "B":
                        board.add_stone(x, y, "Black")
                    elif stone[0] == "W":
                        board.add_stone(x, y, "White")

        else:
            raise ValueError

        if (len(move_seq)) % 2 == 0:
            turn = "Black"
        else:
            turn = "White"
        # create the new Game class
        current_game = Game(
            active_board=board,
            player_turn=turn,
            move_sequence=move_seq,
            size=num_size,
        )
        return current_game


def sgf_folder_to_tree(folder_directory: str, is_absolute: bool = False) -> Gt.GameTree:
    """Returns a game tree by exctracting move sequences out of all sgf files in a given folder

    Preciditions:
    - all files have to be sgf
    """
    tree = Gt.GameTree()
    if is_absolute:
        method = sgf_to_game_sequence_absolute
    else:
        method = sgf_to_game_sequence
    for file in os.listdir(folder_directory):
        sequence, probability = method(file, folder_directory)
        tree.insert_move_sequence(sequence, probability)
    return tree


def sgf_folder_to_tree_recalc_win_score(folder_directory: str) -> Gt.GameTree:
    """Returns a game tree by exctracting move sequences out of all sgf files in a given folder

    Preciditions:
    - all files have to be sgf
    """
    tree = Gt.GameTree()
    for file in os.listdir(folder_directory):
        game = sgf_to_game(file, folder_directory)
        tree.insert_game_into_tree(game)
    return tree


def rotate_move_seq_by_90(moves: list[tuple[int, int, int]], board_size=9) -> list[tuple[int, int, int]]:
    """rotates a sequence of moves clockwise by 90 degrees"""
    rotated_sequence = []
    id_added = 1000  # TODO: modify this (possibly with reference to total number of moves in data set)
    for move in moves:  # TODO: check if this works
        new_move = (id_added + move[0], move[2], board_size - move[1])
        rotated_sequence.append(new_move)
    return rotated_sequence


def save_tree_to_file(tree: Gt.GameTree, file_name: str, folder_directory: str) -> None:
    """Saves the given GameTree as a txt file"""
    with open(folder_directory + file_name, 'wb') as file:
        pickle.dump(tree, file)


def load_tree_from_file(file_name: str, folder_directory: str) -> Gt.GameTree:
    """Load the tree from the txt file"""
    with open(folder_directory + file_name, 'rb') as file:
        return pickle.load(file)


def average_length_of_game_in_folder(folder_directory: str) -> float:
    """Returns an average length of games in a sgf folder"""
    sequence_lengths = []
    for file in os.listdir(folder_directory):
        sequence_lengths.append(len(sgf_to_game_sequence(file, folder_directory)[0]))  # simpler this way
    return sum(sequence_lengths) / len(sequence_lengths)


def sd_length_of_game_in_folder(folder_directory: str, average: float) -> float:
    """Returns the standard deviation of length of games in a sgf folder"""
    square_distances_to_mean = []
    for file in os.listdir(folder_directory):
        square_distances_to_mean.append(pow(abs(len(sgf_to_game_sequence(file, folder_directory)[0]) - average), 2))
    return pow((sum(square_distances_to_mean) / len(square_distances_to_mean)), 0.5)


def print_misc_stats() -> None:
    """Output miscellanious stats about our data set and the resulting trees."""
    games_folder_path = 'DataSet/2015-Go9/'
    go9folder_game_tree_relative = load_tree_from_file("completeScoreTree.txt", "tree_saves/")
    go9folder_game_tree_absolute = load_tree_from_file("CompleteWinRateTree.txt", "tree_saves/")
    go9folder_game_tree_recalculated = load_tree_from_file("RecalcScoreTree.txt", "tree_saves/")
    z_score_80 = 0.842  # for 80th percentile
    average_game_length = average_length_of_game_in_folder(games_folder_path)
    sd = sd_length_of_game_in_folder(games_folder_path, average_game_length)
    print(f"Average game length of our 9x9 games is {average_game_length} with the standard deviation of {sd}")
    print(f"Hence, our 80th percentile cutoff will be {average_game_length + z_score_80 * sd}")
    print("(This was used to determine the cutoff at which the AI will finish the game and then score it)")
    print(f"Score at the root of the complete win rate tree is {go9folder_game_tree_absolute.win_probability}")
    print("(The number represents how many more games were won by black than white)")
    print(f"Score at the root of the complete score tree is {go9folder_game_tree_relative.win_probability} and score "
          f"at the root of the complete recalculated score tree is {go9folder_game_tree_recalculated.win_probability}")
    print("(The two numbers represents how many more point were scored by black in comparison to white,"
          "first according to our data and second according to our scoring system)")


if __name__ == '__main__':
    # All of this is for debugging
    # TODO: prints multiple times, fix when it should and should not print
    games_folder_path = 'DataSet/2015-Go9/'
    games_folder_path_small = 'DataSet/2015-Go9-small/'
    games_folder_path_super_small = 'DataSet/2015-Go9-super-small/'
