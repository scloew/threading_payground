from .puzzle import Puzzle
import textwrap


def build_puzzle_file(puzzle_file):
    """
    parse puzzle_file, build a 2D list with list[i] being ith row
    and index list[i][j] being the value of cell (i, j)
    and initialize and return new puzzle with that list
    :param puzzle_file: text file representing puzzle with 0 representing unknown value
    :return: new Puzzle with puzzle.cells containing value from puzzle_file
    """
    with open(puzzle_file, 'r') as in_file:
        cells = [[v for v in line if v != '\n'] for line in in_file.readlines()]
    return Puzzle(cells)


def build_puzzle_str(puzzle_str):
    rows = textwrap.wrap(puzzle_str, 9)
    cells = [[v for v in line] for line in rows]
    p = Puzzle(cells)
    return p
