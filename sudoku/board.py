"""
Class representing a Sudoku board.
The board can be the initial problem up to the solved board.

Each space in the board is referenced using a (major, minor) square index,
where the "major" index is the specific 3x3 square and the "minor" index
is the specific square within the "major" square.

The "major" (block) index will be sequenced as below:

0 0 0 | 1 1 1 | 2 2 2
0 0 0 | 1 1 1 | 2 2 2
0 0 0 | 1 1 1 | 2 2 2
---------------------
3 3 3 | 4 4 4 | 5 5 5
3 3 3 | 4 4 4 | 5 5 5
3 3 3 | 4 4 4 | 5 5 5
---------------------
6 6 6 | 7 7 7 | 8 8 8
6 6 6 | 7 7 7 | 8 8 8
6 6 6 | 7 7 7 | 8 8 8

The "minor" (cell) index will be sequenced as below:

0 1 2 | 0 1 2 | 0 1 2
3 4 5 | 3 4 5 | 3 4 5
6 7 8 | 6 7 8 | 6 7 8
---------------------
0 1 2 | 0 1 2 | 0 1 2
3 4 5 | 3 4 5 | 3 4 5
6 7 8 | 6 7 8 | 6 7 8
---------------------
0 1 2 | 0 1 2 | 0 1 2
3 4 5 | 3 4 5 | 3 4 5
6 7 8 | 6 7 8 | 6 7 8

Notes:
- Don't get lured in to using list of numbers and basic types.
    - Stay with classes and keep algorithms general.
    - Convert to needed encapsulated type just-in-time.
"""

import os
import unittest
import csv
from itertools import chain
from collections import defaultdict, Counter
from copy import deepcopy

from cell import POSSIBLE_NUMBERS
from block import SudokuBlock


class InvalidBoard(Exception):
    pass

class BoardParseError(Exception):
    pass


class SudokuBoard(object):
    """
    An entire Sudoku board.
    """
    def __init__(self, block_nums=None):
        """
        Initialize the board.
        """
        self.blocks = [ SudokuBlock() for __ in range(9) ]
        if block_nums:
            self.populate(block_nums)

    def populate(self, block_nums):
        """
        Populate an entire SudokuBoard with numbers.
        The numbers are a list of lists, with one list for each major block
        in major order. Each list has nine numbers - a number for each minor square.
        """
        for i, one_block in enumerate(block_nums):
            self.blocks[i].populate(one_block)

    def _populate_from_numdata(self, numdata):
        """
        Populate an entire Sudoku board from BRD line data.
        """
        blocks = defaultdict(list)
        row_num = 0
        for row in numdata:
            if isinstance(row, basestring):
                row = list(row.strip())
            if len(row) == 0:
                continue
            if len(row) != 9:
                raise BoardParseError(
                    "Row number {} does not have 9 values - it has {} values. Row: {}".format(
                    row_num, len(row), row
                ))
            base_block_num = (row_num / 3) * 3
            blocks[base_block_num].extend(row[0:3])
            blocks[base_block_num + 1].extend(row[3:6])
            blocks[base_block_num + 2].extend(row[6:9])
            row_num += 1
        for block_num in range(9):
            self.blocks[block_num].populate(blocks[block_num])

    def populate_from_csvfile(self, filename):
        """
        Populate an entire Sudoku board from a CSV file.
        The file contains nine lines - each row of the Sudoku board with numbers where present
        and blanks where no number is present, with numbers and blanks separated by commas.
        """
        with open(filename, 'rb') as csvfile:
            rows = csv.reader(csvfile)
            self._populate_from_numdata(csv.reader(csvfile))

    def populate_from_brdfile(self, filename):
        """
        Populate an entire Sudoku board from a BRD file.
        The file contains nine lines - each row of the Sudoku board with numbers where present
        and "-" where no number is present. Each line has 9 characters only.
        """
        with open(filename, 'r') as brdfile:
            rows = brdfile.readlines()
            self._populate_from_numdata(rows)

    def populate_from_csvstring(self, csvstring):
        """
        Populate an entire Sudoku board from a multi-line string representing the contents
        of a CSV file.
        The string contains nine lines - each row of the Sudoku board with numbers where present
        and blanks where no number is present, with numbers and blanks separated by commas.
        """
        self._populate_from_numdata(csv.reader(csvstring.split(os.linesep)))

    def populate_from_brdstring(self, brdstring):
        """
        Populate an entire Sudoku board from a multi-line string representing the contents
        of a CSV file.
        The file contains nine lines - each row of the Sudoku board with numbers where present
        and "-" where no number is present. Each line has 9 characters only.
        """
        self._populate_from_numdata(brdstring)

    def _reduce_filter(self, lists, set_cells=False, unset_cells=False):
        """
        Reduces multiple lists of SudokuCells to a single list of SudokuCells.
        Filters to set/empty cells.
        For example:
        [ [2, None, 5], [1, None, None], [None, None, None] ] => [2, 5, 1]
        """
        cells = []
        for a_list in lists:
            for cell in a_list:
                if set_cells:
                    if cell.number is not None:
                        cells.append(cell)
                if unset_cells:
                    if cell.number is None:
                        cells.append(cell)
        return cells

    def _row_blocks(self, row_num):
        return [self.blocks[(row_num / 3) * 3 + i] for i in range(3)]

    def row(self, row_num, as_numbers=True, set_cells=True, unset_cells=True):
        """
        Return all numbers currently set in the board row (0-based).
        If a row has a number more than once, it returns all instances of the number.
        """
        blocks = self._row_blocks(row_num)
        block_row_cells = [block.row(row_num % 3, as_numbers=False) for block in blocks]
        block_row_cells = self._reduce_filter(block_row_cells, set_cells=set_cells, unset_cells=unset_cells)
        if as_numbers:
            block_row_numbers = [cell.number for cell in block_row_cells]
            return sorted(block_row_numbers)
        else:
            return block_row_cells

    def row_remaining(self, row_num):
        """
        Return all numbers remaining to be set in a board row (0-based).
        """
        return sorted(list(POSSIBLE_SET - set(self.row(row_num))))

    def col(self, col_num, as_numbers=True, set_cells=True, unset_cells=True):
        """
        Return all numbers currently set in the board column (0-based).
        """
        blocks = [self.blocks[(col_num / 3) + 3 * i] for i in range(3)]
        block_col_cells = [block.col(col_num % 3, as_numbers=False) for block in blocks]
        block_col_cells = self._reduce_filter(block_col_cells, set_cells=set_cells, unset_cells=unset_cells)
        if as_numbers:
            block_col_numbers = [cell.number for cell in block_col_cells]
            return sorted(block_col_numbers)
        else:
            return block_col_cells

    def col_remaining(self, col_num):
        """
        Return all numbers remaining to be set in a board column (0-based).
        """
        return sorted(list(POSSIBLE_SET - set(self.col(col_num))))

    def reset_possibles(self):
        """
        Reset the possible values of each cell to the full set.
        """
        for block in self.blocks:
            block.reset_possibles()

    def set_possibles(self):
        """
        Eliminate the impossible values in each block, row, and column.
        """
        # Go through each block, find remaining values, and reduce possible cell values.
        for block in self.blocks:
            values = block.numbers()
            values_set = set(values)
            for cell in block.empty_cells():
                cell.eliminate_possibles(values_set)

        # Go through each board row, ...
        for row_num in range(9):
            row_cells = self.row(row_num, as_numbers=False)
            row_values = [ cell.number for cell in row_cells if not cell.empty ]
            row_values_set = set(row_values)
            for cell in row_cells:
                if cell.empty:
                    cell.eliminate_possibles(row_values_set)

        # Go through each board column, ...
        for col_num in range(9):
            col_cells = self.col(col_num, as_numbers=False)
            col_values = [ cell.number for cell in col_cells if not cell.empty ]
            col_values_set = set(col_values)
            for cell in col_cells:
                if cell.empty:
                    cell.eliminate_possibles(col_values_set)

        # If two/three/four cells have the same two/three/four possibles in a block/row/column,
        # eliminate those possibles from the other cells' possibles in that block/row/column.
        possibles_count = Counter()
        for block in self.blocks:
            possibles_count.clear()
            for cell in block.empty_cells():
                possibles_count[tuple(cell.possibles)] += 1
            for possibles, cnt in possibles_count.iteritems():
                if len(possibles) == cnt:
                    for cell in block.empty_cells():
                        if list(possibles) != cell.possibles:
                            cell.eliminate_possibles(set(possibles))

        for row_num in range(9):
            possibles_count.clear()
            row_cells = self.row(row_num, as_numbers=False)
            for cell in row_cells:
                if cell.empty:
                    possibles_count[tuple(cell.possibles)] += 1
            for possibles, cnt in possibles_count.iteritems():
                if len(possibles) == cnt:
                    for cell in row_cells:
                        if cell.empty and list(possibles) != cell.possibles:
                            cell.eliminate_possibles(set(possibles))

        for col_num in range(9):
            possibles_count.clear()
            col_cells = self.col(col_num, as_numbers=False)
            for cell in col_cells:
                if cell.empty:
                    possibles_count[tuple(cell.possibles)] += 1
            for possibles, cnt in possibles_count.iteritems():
                if len(possibles) == cnt:
                    for cell in col_cells:
                        if cell.empty and list(possibles) != cell.possibles:
                            cell.eliminate_possibles(set(possibles))


    def verify(self):
        """
        Eliminate the impossible values in each block, row, and column.
        """
        # Go through each block, find remaining values, and reduce possible cell values.
        for i, block in enumerate(self.blocks):
            values = block.numbers()
            if len(values) and len(values) != len(set(values)):
                # Duplicate values in this block.
                raise InvalidBoard('Block {} has duplicate values.\nBoard:\n{}'.format(i, self))

        # Go through each board row, ...
        for row_num in range(9):
            row_cells = self.row(row_num, as_numbers=False)
            row_values = [ cell.number for cell in row_cells if not cell.empty ]
            if len(row_values) and len(row_values) != len(set(row_values)):
                # Duplicate values in this row.
                raise InvalidBoard('Row {} has duplicate values.\nBoard:\n{}'.format(i, self))

        # Go through each board column, ...
        for col_num in range(9):
            col_cells = self.col(col_num, as_numbers=False)
            col_values = [ cell.number for cell in col_cells if not cell.empty ]
            if len(col_values) and len(col_values) != len(set(col_values)):
                # Duplicate values in this column.
                raise InvalidBoard('Column {} has duplicate values.\nBoard:\n{}'.format(i, self))

    def set_obvious(self):
        """
        If any cells have only one possible number, set the cell to that number.
        """
        cells_set = False
        for block in self.blocks:
            empty_cells = block.empty_cells()
            for cell in empty_cells:
                if len(cell.possibles) == 1:
                    cell.number = cell.possibles[0]
                    cell.possibles = None
                    cells_set = True
        return cells_set

    def analyze(self):
        """
        Given a Sudoku board, update the possible numbers for each empty slot.
        If only a single value is possible in a square, fill it in.
        If the board is in an illogical state, report it.
        Use all rules!
        """
        # Check that the board is in a logical state.
        # TODO: Should only happen due to bugs or incorrectly entered board?
        self.verify()

        # Reset the possible values of each empty cell to the full set.
        self.reset_possibles()

        # Using number elimination based on Sudoku rules, set possible values for each empty cell.
        self.set_possibles()

        # If any values are now obvious, set them and try again.
        while self.set_obvious():
            self.verify()
            self.reset_possibles()
            self.set_possibles()

    def filled(self):
        """
        Returns whether all cells are filled.
        """
        for block in self.blocks:
            empty_cells = block.empty_cells()
            if len(empty_cells) != 0:
                return False
        return True

    def solved(self):
        """
        Returns whether a board has been completely filled with a valid solution.
        """
        if not self.filled():
            return False

        try:
            self.verify()
        except InvalidBoard:
            return False

        return True

    def next_moves(self):
        """
        Return an iterator that yields SudokuBoard objects that represent
        all possible next moves in sequence.
        """
        # Iterate over all the blocks and cells.
        for block_num, block in enumerate(self.blocks):
            for cell_num, cell in enumerate(block.cells):
                if cell.empty:
                    # For each cell's possible values, create a new board and yield it.
                    for possible in cell.possibles:
                        board_copy = deepcopy(self)
                        board_copy[block_num][cell_num].number = possible
                        yield board_copy

    def __getitem__(self, index):
        return self.blocks[index]

    def __eq__(self, other):
        """
        Boards are equal when all blocks are equal.
        """
        for block_num, block in enumerate(self.blocks):
            if other[block_num] != block:
                return False
        return True

    def __unicode__(self):
        board = ""
        for board_row in range(3):
            for block_row in range(3):
                s = []
                for x in range(3):
                    s.append(self.blocks[board_row * 3 + x].row(block_row, as_numbers=False))
                conv = []
                for row in s:
                    conv.append(' '.join([cell.to_string() for cell in row ]))
                board += '{}\n'.format(' | '.join(conv))
            if board_row < 2:
                board += '------+-------+------\n'
        return board

    def __repr__(self):
        return unicode(self)


