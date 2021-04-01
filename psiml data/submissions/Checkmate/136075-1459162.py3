import os
import imageio
import numpy as np


def fill_figures(offset, figures, dirpath, files):
    for file in files:
        if file == 'bishop.png':
            figures[offset + 0] = imageio.imread(os.path.abspath(os.path.join(dirpath, file)))
        elif file == 'king.png':
            figures[offset + 1] = imageio.imread(os.path.abspath(os.path.join(dirpath, file)))
        elif file == 'knight.png':
            figures[offset + 2] = imageio.imread(os.path.abspath(os.path.join(dirpath, file)))
        elif file == 'pawn.png':
            figures[offset + 3] = imageio.imread(os.path.abspath(os.path.join(dirpath, file)))
        elif file == 'queen.png':
            figures[offset + 4] = imageio.imread(os.path.abspath(os.path.join(dirpath, file)))
        elif file == 'rook.png':
            figures[offset + 5] = imageio.imread(os.path.abspath(os.path.join(dirpath, file)))


if __name__ == '__main__':
    path = os.path.abspath(input())
    board = None
    white_tiles = None
    black_tiles = None
    figures = [None, None, None, None, None, None, None, None, None, None, None, None]
    for dirpath, dirs, files in os.walk(path):
        if os.path.samefile(dirpath, path):
            board = imageio.imread(os.path.abspath(os.path.join(dirpath, files[0])))
            continue
        elif os.path.basename(dirpath) == 'tiles':
            for file in files:
                if file == 'black.png':
                    black_tiles = imageio.imread(os.path.abspath(os.path.join(dirpath, file)))
                else:
                    white_tiles = imageio.imread(os.path.abspath(os.path.join(dirpath, file)))
        elif os.path.basename(dirpath) == 'black':
            fill_figures(0, figures, dirpath, files)
        elif os.path.basename(dirpath) == 'white':
            fill_figures(6, figures, dirpath, files)
    match = np.argwhere(board == white_tiles[0][0][0:3])
    board_start_row = match[0,0]
    board_start_column = match[0,1]
    print(board_start_row, board_start_column, sep=',')