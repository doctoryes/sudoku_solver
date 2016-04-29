
import unittest
import copy
from path import Path as path
from sudoku.board import SudokuBoard, InvalidBoard

DATA_DIR = path(__file__).dirname()

class TestSudokuBoard(unittest.TestCase):

    def setUp(self):
        self.board_nums = [
            [
                # http://www.websudoku.com/?level=1&set_id=6848832067
                [None, 9, None, None, 5, None, 3, 6, 8],
                [1, None, 6, 3, None, 7, 4, None, None],
                [None, None, 2, None, 8, None, None, None, 1],
                [None, 8, None, None, None, None, 6, None, None],
                [None, 6, None, 7, 5, 3, None, 4, None],
                [None, None, 9, None, None, None, None, 3, None],
                [5, None, None, None, 2, None, 8, None, None],
                [None, None, 2, 5, None, 8, 9, None, 4],
                [8, 7, 4, None, 6, None, None, 2, None],
            ],
            [
                [None, None, None, None, 1, None, 2, None, None],
                [None, None, 4, None, 2, 8, 9, 5, None],
                [9, None, None, None, 3, None, None, None, None],
                [9, 2, None, None, 5, 6, None, None, 8],
                [None, None, None, None, None, None, None, None, None],
                [1, None, None, 4, 2, None, None, 5, 9],
                [None, None, None, None, 6, None, None, None, 2],
                [None, 8, 6, 5, 1, None, 7, None, None],
                [None, None, 3, None, 7, None, None, None, None],
            ]
        ]
        self.brd_nums = [
"""
519643--7
736--5--4
284-1-695
--8----6-
-6--7--1-
-9----5--
873-5---9
6--9--7--
1---3---6
""",
"""
2-3--4-7-
19-73-8--
-7--2-943
96------8
--2---5--
8------21
539-4--1-
--8-17-59
-1-3--2-4
""",
"""
------175
-9-735862
---821943
96-572438
342186597
857493621
539248716
-28617359
716359284
""",
        ]


    def test_empty_repr(self):
        board = SudokuBoard()
        self.assertEqual(unicode(board), '- - - | - - - | - - -\n- - - | - - - | - - -\n- - - | - - - | - - -\n------+-------+------\n- - - | - - - | - - -\n- - - | - - - | - - -\n- - - | - - - | - - -\n------+-------+------\n- - - | - - - | - - -\n- - - | - - - | - - -\n- - - | - - - | - - -\n')

    # TODO: ddt these tests to check all param combinations.
    def test_a_board(self):
        board = SudokuBoard(self.board_nums[0])
        self.assertEqual(board[4].row(1), [7, 5, 3])
        self.assertEqual(board[7].col(2), [2, 8, 4])
        self.assertEqual(board.row(5, unset_cells=False), [3, 4, 6])
        self.assertEqual(board.col(5, unset_cells=False), [2, 3, 4, 6, 7, 8])

    def test_possibles(self):
        board = SudokuBoard(self.board_nums[1])
        board.analyze()
        self.assertItemsEqual(board[4][5].possibles, [1, 3, 7, 9])

    def _verify_board(self, board):
        self.assertEqual(board[4].row(1), [None, None, None])
        self.assertEqual(board[2].row(2), [9, 4, 3])
        self.assertEqual(board[2].col(2), [None, None, 3])
        self.assertEqual(board.row(5, unset_cells=False), [1, 2, 8])
        self.assertEqual(board.col(8, unset_cells=False), [1, 3, 4, 8, 9])

    def test_board_load_from_csvfile(self):
        board = SudokuBoard()
        board.populate_from_csvfile(DATA_DIR / 'board1.csv')
        self._verify_board(board)

    def test_board_load_from_csvstring(self):
        board = SudokuBoard()
        with open(DATA_DIR / 'board1.csv', 'rb') as csvfile:
            csvstring = csvfile.read()
        board.populate_from_csvstring(csvstring)
        self._verify_board(board)

    def test_board_load_from_brdfile(self):
        board = SudokuBoard()
        board.populate_from_brdfile(DATA_DIR / 'board1.brd')
        self._verify_board(board)

    def test_board_load_from_brdstring(self):
        board = SudokuBoard()
        with open(DATA_DIR / 'board1.brd', 'r') as brdfile:
            brdstring = brdfile.readlines()
        board.populate_from_brdstring(brdstring)
        self._verify_board(board)

    def test_board_equality(self):
        board1 = SudokuBoard(self.board_nums[0])
        board2 = SudokuBoard(self.board_nums[1])
        board3 = SudokuBoard(self.board_nums[1])
        self.assertNotEqual(board1, board2)
        self.assertNotEqual(board1, board3)
        self.assertEqual(board2, board3)
        self.assertTrue(board2 in [board3])

    def test_board_analyze_invalid(self):
        board = SudokuBoard()
        board.populate_from_brdstring(self.brd_nums[0].split('\n'))
        with self.assertRaises(InvalidBoard):
            board.analyze()

    def test_board_deepcopy(self):
        board = SudokuBoard(self.board_nums[0])
        # Ensure that a deepcopy can be done without raising an exception.
        board_copy = copy.deepcopy(board)

    def test_set_possibles(self):
        board = SudokuBoard()
        board.populate_from_brdstring(self.brd_nums[2].split('\n'))
        board.reset_possibles()
        board.set_possibles()
        self.assertEqual(board[0][0].possibles, [2])
        self.assertEqual(board[0][1].possibles, [8])
        self.assertEqual(board[0][2].possibles, [3])
        self.assertEqual(board[0][3].possibles, [1])
        self.assertEqual(board[0][5].possibles, [4])
        self.assertEqual(board[0][6].possibles, [6])
        self.assertEqual(board[0][7].possibles, [7])
        self.assertEqual(board[0][8].possibles, [5])
        self.assertEqual(board[1][0].possibles, [9])
        self.assertEqual(board[1][1].possibles, [6])
        self.assertEqual(board[1][2].possibles, [4])
        self.assertEqual(board[3][2].possibles, [1])
        self.assertEqual(board[6][3].possibles, [4])


if __name__ == '__main__':
    unittest.main()


