from datetime import datetime
from random import randint
from .cell import Cell
from .group import Group
from ._contants import status


class Puzzle:
    """
    Represents puzzle providing a method to solve the puzzle
    """
    def __init__(self, cells_values, logger=None):
        date = datetime.now().strftime("%m_%d_%Y-%H_%M_%S")
        self.logger = logger if logger else open(f'.\\logs\\{randint(0,10000)}-{date}.log', 'a') #TODO logging is a little clunky
        self.original = False if logger else True
        self.logger.write(f'\n{"=" * 8}\nBEGIN TESTING NEW PUZZLE\n{"=" * 8}\n\n')
        self.cells = [[Cell(c) for c in row] for row in cells_values]
        self.update_number = sum(1 for i in range(9) for j in range(9) if self.cells[i][j].val == '0')
        self._build_column_groups()
        self._build_row_groups()
        self._build_square_groups()
        self.logger.write(f'After constructions puzzle is: \n\n{self.to_string()}')

    def _build_column_groups(self):
        self.columns = [Group([self.cells[j][i] for j in range(9)]) for i in range(9)]
        self.logger.write('Columns groups built...\n')

    def _build_row_groups(self):
        self.rows = [Group(self.cells[i]) for i in range(9)]
        self.logger.write('Row groups built...\n')

    def _build_square_groups(self):
        self.squares = []
        self._square_dict = {}
        for off_set in range(3):
            row_offset = 0
            for x_index in range(0, 9, 3):
                temp_list = []
                for y_index in range(0, 3):
                    temp_list += self.cells[y_index + 3 * off_set][x_index :x_index + 3]
                self.squares.append(Group(temp_list))  # TODO nice list comprhension for this?
                self._square_dict.update({(off_set, row_offset): self.squares[-1]})
                row_offset += 1
        self.logger.write('Square groups built...\n')

    def solve_puzzle(self):
        """
        iterate through groups updating cells; when cell takes value, updata groups
        do while puzzle not solved. Will need to update process for handling guessing
        :return cells with value if puzzle was solved, false otherwise
        """
        debug_count, puzzle_updated = 1, True
        while self.update_number != 0 and puzzle_updated:
            debug_count += 1
            puzzle_updated = False
            for row_num in range(9):
                for col_num in range(9):
                    iteration_status = self._check_updates(row_num, col_num)
                    puzzle_updated = puzzle_updated or (not iteration_status == {status.no_change})
                    if status.value_set in iteration_status:
                        self.logger.write(f'\ncell{(row_num, col_num)} value set to {self.cells[row_num][col_num].val}')
                        iteration_status = iteration_status.union(self._update_groups(row_num, col_num))
                        self.logger.write(f'\npuzzle current state is\n\n{self.to_string()}')
                    if status.puzzle_error_found in iteration_status:
                        return False, None #TODO need to better handle of this flag
            if not puzzle_updated:
                if self._guess():
                    break
                else:
                    return False, None
        if self.original:
            self._close_log()
        return True, self.cells

    def _check_updates(self, row_num, col_num):
        cell, ret_statuses = self.cells[row_num][col_num], set()
        ret_statuses.add(cell.update_options(self.rows[row_num].options))
        ret_statuses.add(cell.update_options(self.columns[col_num].options))
        ret_statuses.add(cell.update_options(self._square_dict[(int(row_num/3), int(col_num/3))].options))
        return ret_statuses

    def _update_groups(self, row_num, col_num):
        cell, ret_statuses = self.cells[row_num][col_num], set()
        self.update_number -= 1
        ret_statuses.add(self.rows[row_num].update_options(cell.val))
        ret_statuses.add(self.columns[col_num].update_options(cell.val))
        ret_statuses.add(self._square_dict[(int(row_num / 3), int(col_num / 3))].update_options(cell.val))
        return ret_statuses

    def _guess(self):
        """
        Avoid infinite loop of failing to update any cells/groups
        by guessing cell value starting with cell with minimum number of options
        and increasing until puzzle is solved
        :return: True if puzzle has been solved, other wise false
        """
        self.logger.write(f'\nGEUSSING CELL VALUE\n{"*" * 8}\n\n')
        _, row_num, col_num = min((self.cells[y][x].val, y, x) for y in range(9) for x in range(9))
        for option in self.cells[row_num][col_num].options:
            self.cells[row_num][col_num].set_val(option)
            self.logger.write(f'guessing cell{(row_num, col_num)} is {self.cells[row_num][col_num].val}\n')
            guess_puzzle = Puzzle([[c.val for c in row] for row in self.cells], logger=self.logger)
            solved, new_cells = guess_puzzle.solve_puzzle()
            if solved:
                self.logger.write(f'\nGuessing resulted in solved puzzle\n')
                self.cells = new_cells
                return True
        self.cells[row_num][col_num] = '0'
        return False

    def _close_log(self):
        self.logger.write(f'\n{"=" * 8}\nPUZZLE SOLVED\n{"=" * 8}\n\n')
        self.logger.close()

    def to_string(self):
        ret = ''
        for index, row in enumerate(self.cells):
            temp_str = ''.join([c.val for c in row])
            temp_line = '|'.join(a + b + c for a, b, c in zip(temp_str[::3], temp_str[1::3], temp_str[2::3]))
            ret += (' '.join(temp_line) + '\n')
            if index in {2, 5}:
                ret += ('-  ' * 8) + '\n'
        return ret

    def print_puzzle(self):
        print(self.to_string())
