import random                           
from collections import defaultdict    
from collections import Counter       

SHC_conflicts_puzzle = [[0 for _ in range(9)] for _ in range(9)]  
puzzle = [   
        [8, 0, 2, 0, 0, 6, 0, 5, 0],
        [0, 4, 0, 0, 1, 8, 0, 0, 0],
        [0, 9, 0, 0, 0, 3, 0, 8, 4],
        [2, 0, 0, 0, 0, 9, 8, 0, 1],
        [0, 1, 0, 0, 0, 0, 5, 4, 9],
        [0, 8, 0, 0, 3, 0, 6, 0, 0],
        [0, 7, 8, 9, 0, 2, 4, 0, 5],
        [0, 2, 9, 0, 0, 5, 7, 0, 3],
        [5, 0, 1, 0, 7, 0, 9, 0, 8]
    ]

def SHC_generate_initial_solution(puzzle):
    initial_solution = [row[:] for row in puzzle]   
    #occurrences = Counter(num for row in puzzle for num in row if num != 0)   

    for i in range(9):
        occurrences = Counter(initial_solution[i])
        for j in range(9):
            if initial_solution[i][j] == 0:   
                available_numbers = [num for num in range(1, 10) if occurrences]   
                num = random.choice(available_numbers)   
                initial_solution[i][j] = num   
                occurrences[num] += 1   
    return initial_solution   

def SHC_print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(str(num) for num in row))   

def SHC_count_conflicts(puzzle):
    conflicts = [[0 for _ in range(9)] for _ in range(9)]

    for row in range(9):
        row_counts = Counter(puzzle[row])
        for num, count in row_counts.items():
            if num != 0 and count > 1:
                for col in range(9):
                    if puzzle[row][col] == num:
                        conflicts[row][col] += (count - 1)

    for col in range(9):
        col_counts = Counter(puzzle[row][col] for row in range(9))
        for num, count in col_counts.items():
            if num != 0 and count > 1:
                for row in range(9):
                    if puzzle[row][col] == num:
                        conflicts[row][col] += (count -1)

    for start_row in (0, 3, 6):
        for start_col in (0, 3, 6):
            block_counts = Counter(
                puzzle[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)
            )
            for num, count in block_counts.items():
                if num != 0 and count > 1:
                    for row in range(start_row, start_row + 3):
                        for col in range(start_col, start_col + 3):
                            if puzzle[row][col] == num:
                                conflicts[row][col] += (count -1)
    return conflicts

def SHC_hill_climbing(puzzle):
    initial_puzzle = SHC_generate_initial_solution(puzzle)
    max_iterations = 500000
    current_puzzle = [row[:] for row in initial_puzzle]

    for iteration in range(max_iterations):
        conflicts_puzzle =  SHC_count_conflicts(current_puzzle)
        max_conflicts = max(max(row) for row in conflicts_puzzle)

        if max_conflicts == 0:
            return current_puzzle
        
        max_conflicts_cells = [(i, j) for i in range(9) for j in range(9) if conflicts_puzzle[i][j] == max_conflicts]
        if len(max_conflicts_cells) < 2:
            continue

        first_cell, second_cell = random.sample(max_conflicts_cells, 2)
        row1, col1 = first_cell
        row2, col2 = second_cell

        current_puzzle[row1][col1], current_puzzle[row2][col2] = current_puzzle[row2][col2], current_puzzle[row1][col1]

        if iteration % 2500 == 0:
            current_puzzle = [row[:] for row in SHC_generate_initial_solution(puzzle)]
    return None


def SHC_run(puzzle):
    print("Initial Sudoku puzzle:")   
    SHC_print_puzzle(puzzle)
    print("\n")   

    solved_puzzle = SHC_hill_climbing(puzzle)   

    if solved_puzzle is not None:
        print("\nSolved Sudoku puzzle:")   
        SHC_print_puzzle(solved_puzzle)
    else:
        print("\nFailed to solve")   

SHC_run(puzzle)
