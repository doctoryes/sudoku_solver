"""
Representation of a single Sudoku cell.
"""

# Possible cell numbers - list and set.
POSSIBLE_NUMBERS = range(1, 10)
POSSIBLE_SET = frozenset(POSSIBLE_NUMBERS)


class SudokuCell(object):
    """
    A single Sudoku cell.
    """
    def __init__(self):
        # Filled-in number for cell. None means empty.
        self.number = None
        # List of possible numbers for this cell.
        # Begins with all possible numbers.
        self.possibles = POSSIBLE_NUMBERS

    def set_possibles(self, possibles):
        """
        Set possible numbers as the passed-in number list.
        """
        self.possibles = possibles

    def eliminate_possibles(self, impossibles):
        """
        Eliminates all the passed-in numbers from the list of possible numbers.
        """
        self.possibles = sorted(list(set(self.possibles) - set(impossibles)))

    @property
    def empty(self):
        return self.number is None

    def to_string(self):
        return '-' if self.empty else '{}'.format(self.number)

    def __repr__(self):
        if self.empty:
            value = 'UNSET'
        else:
            value = str(self.number)
        return "{} - Possibles: {}".format(value, self.possibles)


