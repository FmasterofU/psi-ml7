import os
import imageio
import numpy as np
from PIL import Image


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

def process_field(board, white_tiles, black_tiles, figures, field_size, empty_fields_count,curr_field_row, curr_field_column, board_start_row, board_start_column, board_end_row, board_end_column):
    FEN_part = ''
    if curr_field_column > board_end_column:
        curr_field_row += field_size
        curr_field_column = board_start_column
        if empty_fields_count == 0:
            FEN_part += '/'
        else:
            FEN_part += str(empty_fields_count) + '/'
        empty_fields_count = 0
    field = board[curr_field_row:curr_field_row+field_size, curr_field_column:curr_field_column+field_size, :]
    if np.all(field == white_tiles[0][0][0:3]) or np.all(field == black_tiles[0][0][0:3]):
        empty_fields_count += 1
    else:
        if empty_fields_count != 0:
            FEN_part += str(empty_fields_count)
            empty_fields_count = 0
        field = field * (field != field[0][0])
        cfs = list()
        for i in range(len(figures)):
            cfs.append(np.mean((field[:,:,0:2] / 255 - figures[i][:,:,0:2] / 255) ** 2))
        index = np.argmin(np.array(cfs))
        if index == 0:
            FEN_part += 'b'
        elif index == 1:
            FEN_part += 'k'
        elif index == 2:
            FEN_part += 'n'
        elif index == 3:
            FEN_part += 'p'
        elif index == 4:
            FEN_part += 'q'
        elif index == 5:
            FEN_part += 'r'
        elif index == 6:
            FEN_part += 'B'
        elif index == 7:
            FEN_part += 'K'
        elif index == 8:
            FEN_part += 'N'
        elif index == 9:
            FEN_part += 'P'
        elif index == 10:
            FEN_part += 'Q'
        elif index == 11:
            FEN_part += 'R'
    curr_field_column += field_size
    return FEN_part, curr_field_row, curr_field_column, empty_fields_count

def resize_to_field(image, side_size):
    return np.array(Image.fromarray(image, 'RGBA').resize((side_size, side_size), Image.ANTIALIAS))

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
    board_end_row = match[-1,0]
    board_end_column = match[-1,1]
    field_size = int((board_end_column - board_start_column + 1) / 8)
    white_tiles = resize_to_field(white_tiles, field_size)
    black_tiles = resize_to_field(black_tiles, field_size)
    for i in range(len(figures)):
        figures[i] = resize_to_field(figures[i], field_size)
    curr_field_row = board_start_row
    curr_field_column = board_start_column
    FEN = ''
    empty_fields_count = 0
    for _ in range(64):
        field_FEN, curr_field_row, curr_field_column, empty_fields_count = process_field(board, white_tiles, black_tiles, figures, field_size, empty_fields_count, curr_field_row, curr_field_column, board_start_row, board_start_column, board_end_row, board_end_column)
        FEN += field_FEN
    if empty_fields_count != 0:
        FEN += str(empty_fields_count)
    print(FEN)
    whites = 0
    blacks = 0
    for ch in FEN:
        if ch.islower():
            blacks += 1
        elif not ch.isnumeric() and ch != '/':
            whites += 1
    if blacks <= 2 and whites >= 3:
        print("W")
    elif whites <= 2 and blacks >= 3:
        print("B")
    else:
        print()
    if (blacks == 1 and whites != 1) or (whites == 1 and blacks != 1):
        print(1)
    else: 
        print()