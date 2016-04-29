
import copy
from sudoku.board import SudokuBoard, InvalidBoard

boards_to_solve = [
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
5---4---7
--6--5--4
2---1-695
--8----6-
-6--7--1-
-9----5--
873-5---9
6--9--7--
1---3---6
""",
# "Evil" board: http://www.websudoku.com/?level=4&set_id=9074109009
"""
5----91-8
-----8--7
--82---56
-----3-2-
3-------1
-2-1-----
94---18--
2--6-----
1-53----4
""",
# http://www.websudoku.com/?level=4&set_id=9074109009
"""
----5-42-
---6-----
91-3-7---
--71----5
-8-----9-
6----23--
---5-9-71
-----6---
-65-3----
""",
"""
---------
---------
---------
---------
----1----
---------
---------
---------
---------
""",
"""
---------
---------
---------
---------
---------
---------
---------
---------
---------
"""
]

MAX_CALLS = 100000
DEBUG_PRINT = True

def _debug_print(str_obj):
    if DEBUG_PRINT:
        print str_obj

def solve_board(board, solved, visited, count):
    if count >= MAX_CALLS:
        return None, False, visited, count
    if solved:
        return board, True, visited, count
    if board in visited:
        # If we've already visited this board, no point in doing it again.
        _debug_print("ALREADY VISITED:")
        _debug_print(board)
        return None, False, visited, count
    try:
        board.analyze()
    except InvalidBoard:
        # This path leads to an invalid board.
        _debug_print("PATH TO INVALID BOARD:")
        _debug_print(board)
        return None, False, visited, count + 1
    if board.solved():
        return board, True, visited, count + 1
    for board_to_try in board.next_moves():
        _debug_print("TRYING BOARD:")
        _debug_print(board_to_try)
        board_result, solved, visited, count = solve_board(board_to_try, False, visited, count + 1)
        if board_result is None:
            # Dead-end.
            continue
        elif solved:
            return board_result, True, visited, count
    # No solution was found.
    _debug_print("NO SOLUTION ON THIS PATH:")
    _debug_print(board)
    _debug_print("ADDED TO VISITED:")
    _debug_print(board)
    visited.add(board)
    return None, False, visited, count + 1

for test_board in boards_to_solve:
    board = SudokuBoard()
    board.populate_from_brdstring(test_board.split('\n'))
    visited = set()
    print "------------------------------"
    print "Original board:"
    print board
    solved_board, solved, visited, count = solve_board(copy.deepcopy(board), False, visited, 0)
    print "Solved board:"
    print solved_board
