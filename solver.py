
from sudoku.board import SudokuBoard

test_board = """
2,,3,,,4,,7,
1,9,,7,3,,8,,,
,7,,,2,,9,4,3
9,6,,,,,,,8
,,2,,,,5,,
8,,,,,,,2,1
5,3,9,,4,,,1,
,,8,,1,7,,5,9
,1,,3,,,2,,4
"""

def solve_board(board):
    if board.solved():
        return board
    for board_to_try in board.next_moves():
        return solve_board(board_to_try)

board = SudokuBoard()
board.populate_from_csvstring(test_board)
solved = solve_board(board)
print "Original board:"
print board
print "Solved board:"
print solved
