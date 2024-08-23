import random
import math
import statistics

puzzle = [
    [0, 0, 0, 1, 0, 2, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 0, 7, 0],
    [0, 0, 8, 0, 0, 0, 9, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [2, 0, 0, 0, 8, 0, 0, 0, 1],
    [0, 0, 9, 0, 0, 0, 8, 0, 5],
    [0, 7, 0, 0, 0, 0, 0, 6, 0],
    [0, 0, 0, 3, 0, 4, 0, 0, 0]
]

def SBT_is_valid(puzzle, row, col, num):
    for i in range(9):
        if puzzle[row][i] == num:
            return False
        
    for i in range(9):
        if puzzle[i][col] == num:
            return False
        
    start_row, start_col = 3 * (row//3), 3 * (col//3)
    for i in range(3):
        for j in range(3):
            if puzzle[i+start_row][j+start_col] == num:
                return False
            
    return True

def SBT_find_empty_location(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return (i, j)
    return None

def SBT_solve_sudoku(puzzle):
    empty_location = SBT_find_empty_location(puzzle)

    if not empty_location:
        return True
    
    row, col = empty_location

    for num in range(1, 10):
        if SBT_is_valid(puzzle, row, col, num):
            puzzle[row][col] = num
            if SBT_solve_sudoku(puzzle):
                return True
            
            puzzle[row][col] = 0

    return False

def SBT_print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(str(num) for num in row))

def SBT_run(puzzle):
    if SBT_solve_sudoku(puzzle):
        print ("Sudoku Puzzle Solved")
        SBT_print_puzzle(puzzle)
    else:
        print("No Solution")

SBT_run(puzzle);