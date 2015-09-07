"""
Representation of a Sudoku 3x3 block.
"""

import unittest
from cell import SudokuCell, POSSIBLE_NUMBERS, POSSIBLE_SET


class SudokuBlock(object):
    """
    A single 3x3 Sudoku block made up of 9 SudokuCell objects.
    A board is made up of 9 SudokuBlock objects.
    Rows are addressed as 0, 1, 2 for top, middle, and bottom rows respectively.
    Columns are addressed as 0, 1, 2 for left, middle, and right columns respectively.
    """
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
                if len(x):
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
        return [cell.number for cell in self.cells if cell.number is not None]

    def remaining(self):
        """
        Returns a list of numbers not yet present in block.
        """
        return sorted(list(POSSIBLE_SET - set(self.numbers())))

    def empty_cells(self):
        """
        Returns a list of all empty SudokuCells.
        """
        return [ cell for cell in self.cells if cell.number is None ]

    def __getitem__(self, index):
        return self.cells[index]

    def __unicode__(self):
        s = ""
        for row_num in range(3):
            row = self.row(row_num, as_numbers=False)
            s += ' '.join([cell.to_string() for cell in row])
            s += '\n'
        return s

    def __repr__(self):
        return unicode(self)


class TestSudokuBlock(unittest.TestCase):

    def test_empty(self):
        block = SudokuBlock()
        for x in range(3):
            self.assertEqual(block.row(x), [None, None, None])
            self.assertEqual(block.col(x), [None, None, None])

    def test_row(self):
        block = SudokuBlock([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(block.row(0), [1, 2, 3])
        self.assertEqual(block.row(1), [4, 5, 6])
        self.assertEqual(block.row(2), [7, 8, 9])

    def test_col(self):
        block = SudokuBlock([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(block.col(0), [1, 4, 7])
        self.assertEqual(block.col(1), [2, 5, 8])
        self.assertEqual(block.col(2), [3, 6, 9])

    def test_remaining(self):
        block = SudokuBlock()
        self.assertEqual(block.remaining(), POSSIBLE_NUMBERS)
        block = SudokuBlock([1, None, 3, 4, 5, 6, None, 8, 9])
        self.assertEqual(block.remaining(), [2, 7])

    def test_populate_numbers(self):
        block = SudokuBlock()
        block.populate([1, None, 5, None, None, None, 9, 3, 7])
        self.assertEqual(block.remaining(), [2, 4, 6, 8])

    def test_populate_strings(self):
        block = SudokuBlock()
        block.populate(['1', '', '5', '', '', '', '9', '3', '7'])
        self.assertEqual(block.remaining(), [2, 4, 6, 8])

if __name__ == '__main__':
    unittest.main()

