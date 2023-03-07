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
import os
import board as b


def read_sgf(file_name: str, file_directory: str, do_deletion: bool):
    """
    Reads a single SGF file and checks if it has a valid result. If it does not have a valid result and
    do_deletion is True, the file will be deleted.

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
                print("Proceeding with deletion:")
                try:
                    os.remove(file_directory + file_name)
                except FileNotFoundError:
                    print("Fail. File was not found.")
                else:
                    print("Success. File deleted.")
        else:
            print(f"Game has a valid result of {header[header.index('RE') + 2:header.index('KM')]} aka is usable.")
            sgf_file.readline()
            sgf_file.readline()
            game = sgf_file.readline().split(';')
            game = game[1:-2]
            board = b.Board(9)
            for stone in game:
                x = ord(stone[2]) - 97
                y = ord(stone[3]) - 97
                if stone[0] == "B":
                    board.add_stone(x, y, "Black")
                elif stone[0] == "W":
                    board.add_stone(x, y, "White")
            print(board)


def read_all_sgf_in_folder(folder_directory: str, do_deletion: bool = False):
    """
    Reads all SGF files in a folder and calls read_sgf for each file.

    Args:
        folder_directory (str): The directory containing the SGF files.
        do_deletion (bool): If True and the SGF file does not have a valid result, the file will be deleted.
    """
    for file in os.listdir(folder_directory):
        read_sgf(file, folder_directory, do_deletion)


if __name__ == '__main__':
    games_folder_path_absolute = '/Users/dmitriivlasov/Downloads/go9/'
    games_folder_path_relative = 'games/'
    read_all_sgf_in_folder(games_folder_path_relative, False)
