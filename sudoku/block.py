"""
Representation of a Sudoku 3x3 block.
"""

from cell import SudokuCell, POSSIBLE_NUMBERS, POSSIBLE_SET


class SudokuBlock(object):
    """
    A single 3x3 Sudoku block made up of 9 SudokuCell objects.
    A board is made up of 9 SudokuBlock objects.
    Rows are addressed as 0, 1, 2 for top, middle, and bottom rows respectively.
    Columns are addressed as 0, 1, 2 for left, middle, and right columns respectively.
    """
    __slots__ = ['cells']

    def __init__(self, numbers=None):
        self.cells = [ SudokuCell() for __ in range(9) ]
        if numbers:
            self.populate(numbers)

    def populate(self, numbers):
        """
        Takes a list of nine numbers and populates cells.
        """
        for i, x in enumerate(numbers):
            if isinstance(x, basestring):
                if x.isdigit():
                    x = int(x)
                else:
                    x = None
            self.cells[i].number = x

    def reset_possibles(self):
        """
        Reset the possible values in each empty cell.
        """
        for cell in self.cells:
            if cell.empty:
                cell.possibles = POSSIBLE_NUMBERS
            else:
                cell.possibles = None

    def row(self, row_num, as_numbers=True):
        """
        Returns a row of SudokuCells, optionally as numbers.
        """
        cells = []
        for i in range(3):
            cells.append(self.cells[row_num * 3 + i])
        if as_numbers:
            return [x.number for x in cells]
        else:
            return cells

    def col(self, col_num, as_numbers=True):
        """
        Returns a column of SudokuCells, optionally as numbers.
        """
        cells = []
        for i in range(3):
            cells.append(self.cells[col_num + 3 * i])
        if as_numbers:
            return [x.number for x in cells]
        else:
            return cells

    def numbers(self):
        """
        Returns a list of all numbers currently in the block.
        """
        return [cell.number for cell in self.cells if not cell.empty ]

    def remaining(self):
        """
        Returns a list of numbers not yet present in block.
        """
        return sorted(list(POSSIBLE_SET - set(self.numbers())))

    def empty_cells(self):
        """
        Returns a list of all empty SudokuCells.
        """
        return [ cell for cell in self.cells if cell.empty ]

    def __getitem__(self, index):
        return self.cells[index]

    def __eq__(self, other):
        """
        Blocks are equal if each cell is equal.
        """
        for cell_num, cell in enumerate(self.cells):
            if other[cell_num] != cell:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __unicode__(self):
        s = ""
        for row_num in range(3):
            row = self.row(row_num, as_numbers=False)
            s += ' '.join([cell.to_string() for cell in row])
            s += '\n'
        return s

    def __repr__(self):
        return unicode(self)
