import random as r


def create_empty_grid(rows: int, cols: int) -> list[list[int]]:
    """
    Creates a 2D grid filled with zeros.

    :param rows: number of rows in the grid
    :param cols: number of columns in the grid
    :return: 2D list (list of lists) with all values set to 0
    """
    list_return = []
    for row in range(rows):
        row_list = [0 for _ in range(cols)]
        list_return.append(row_list)
    return list_return


def random_grid(rows: int, cols: int, prob: float = 0.5) -> list[list[int]]:
    """
    Creates a 2D grid filled with random 0s and 1s.

    :param rows: number of rows in the grid
    :param cols: number of columns in the grid
    :param prob: probability of a cell being 0 (default is 0.5)
    :return: 2D list with randomly generated values (0 or 1)
    """
    list_return = []
    for row in range(rows):
        row_list = [0 if r.random() < prob else 1 for _ in range(cols)]
        list_return.append(row_list)
    return list_return


def load_grid_from_file(filename: str) -> list[list[int]]:
    """
    Loads a grid from a text file.

    Each line in the file represents a row of the grid,
    and each character in the line should be a digit (0 or 1).

    :param filename: path to the file
    :return: 2D list representing the grid
    """
    list_return = []
    with open(f'{filename}', 'r') as f:
        for line in f:
            line = line.strip()
            list_return.append([int(x) for x in line])
    return list_return


def save_grid_to_file(grid: list[list[int]], filename: str) -> None:
    """
    Saves a grid to a text file.

    Each row of the grid is written as a line of digits without spaces.

    :param grid: 2D list representing the grid
    :param filename: path to the file
    :return: None
    """
    with open(f'{filename}', 'w') as f:
        for row in grid:
            f.write(''.join(str(x) for x in row) + '\n')


def set_cell(grid: list[list[int]], row: int, col: int, value: int) -> None:
    """
    Sets a specific cell in the grid to a given value.

    :param grid: 2D list representing the grid
    :param row: row index of the cell
    :param col: column index of the cell
    :param value: value to set (typically 0 or 1)
    :raises IndexError: if row or column is out of bounds
    :return: None
    """
    if 0 <= row < len(grid) and 0 <= col < len(grid[row]):
        grid[row][col] = value
    else:
        raise IndexError("Row or column out of range")
