import unittest
from sudoku.cell import POSSIBLE_NUMBERS
from sudoku.block import SudokuBlock


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
