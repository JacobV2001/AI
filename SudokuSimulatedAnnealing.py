import random
import math
import statistics

def SSA_fix_puzzle_values(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                puzzle[i][j] = 1
    return puzzle

def SSA_calculate_number_of_errors(puzzle):
    error_count = 0
    for i in range(9):
        error_count += SSA_calculate_errors_row_column(i, i, puzzle)
    return error_count

def SSA_calculate_errors_row_column(row, column, puzzle):
    unique_row_values = set()
    unique_column_values = set()
    for i in range(9):
        unique_row_values.add(puzzle[i][column])
        unique_column_values.add(puzzle[row][i])
    error_count = (9 - len(unique_row_values)) + (9 - len(unique_column_values))
    return error_count

def SSA_create_list_3x3_blocks():
    final_block_list = []
    for r in range(9):
        tmp_list = []
        block1 = [i + 3 * ((r) % 3) for i in range(3)]
        block2 = [i + 3 * math.trunc((r) / 3) for i in range(3)]
        for x in block1:
            for y in block2:
                tmp_list.append([x, y])
        final_block_list.append(tmp_list)
    return final_block_list

def SSA_randomly_fill_3x3_blocks(puzzle, block_list):
    for block in block_list:
        for box in block:
            if puzzle[box[0]][box[1]] == 0:
                current_block = [puzzle[i][j] for i in range(block[0][0], block[-1][0] + 1)
                                 for j in range(block[0][1], block[-1][1] + 1)]
                puzzle[box[0]][box[1]] = random.choice([i for i in range(1, 10) if i not in current_block])
    return puzzle

def SSA_sum_of_one_block(puzzle, one_block):
    final_sum = 0
    for box in one_block:
        final_sum += puzzle[box[0]][box[1]]
    return final_sum

def SSA_two_random_boxes_within_block(fixed_puzzle, block):
    while (1):
        first_box = random.choice(block)
        second_box = random.choice([box for box in block if box is not first_box])

        if fixed_puzzle[first_box[0]][first_box[1]] != 1 and fixed_puzzle[second_box[0]][second_box[1]] != 1:
            return [first_box, second_box]

def SSA_flip_boxes(puzzle, boxes_to_flip):
    proposed_puzzle = [row[:] for row in puzzle]
    placeholder = proposed_puzzle[boxes_to_flip[0][0]][boxes_to_flip[0][1]]
    proposed_puzzle[boxes_to_flip[0][0]][boxes_to_flip[0][1]] = proposed_puzzle[boxes_to_flip[1][0]][boxes_to_flip[1][1]]
    proposed_puzzle[boxes_to_flip[1][0]][boxes_to_flip[1][1]] = placeholder
    return proposed_puzzle

def SSA_proposed_state(puzzle, fixed_puzzle, block_list):
    random_block = random.choice(block_list)

    if SSA_sum_of_one_block(fixed_puzzle, random_block) > 6:
        return puzzle, []  # Return an empty list if condition is met
    boxes_to_flip = SSA_two_random_boxes_within_block(fixed_puzzle, random_block)
    proposed_puzzle = SSA_flip_boxes(puzzle, boxes_to_flip)
    return proposed_puzzle, boxes_to_flip



def SSA_choose_new_state(current_puzzle, fixed_puzzle, block_list, sigma):
    proposal = SSA_proposed_state(current_puzzle, fixed_puzzle, block_list)
    new_puzzle = proposal[0]
    boxes_to_check = proposal[1]
    
    # Check if boxes_to_check is empty
    if not boxes_to_check:
        # Return current puzzle and cost difference as 0
        return current_puzzle, 0
    
    # Calculate current and new costs only if boxes_to_check is not empty
    current_cost = SSA_calculate_errors_row_column(boxes_to_check[0][0], boxes_to_check[0][1], current_puzzle) + \
                   SSA_calculate_errors_row_column(boxes_to_check[1][0], boxes_to_check[1][1], current_puzzle)
    new_cost = SSA_calculate_errors_row_column(boxes_to_check[0][0], boxes_to_check[0][1], new_puzzle) + \
               SSA_calculate_errors_row_column(boxes_to_check[1][0], boxes_to_check[1][1], new_puzzle)

    cost_difference = new_cost - current_cost
    rho = math.exp(-cost_difference / sigma)
    
    if random.uniform(0, 1) < rho:
        return new_puzzle, cost_difference
    return current_puzzle, 0


def SSA_choose_number_of_iterations(fixed_puzzle):
    iterations_count = 0
    for i in range(9):
        for j in range(9):
            if fixed_puzzle[i][j] != 0:
                iterations_count += 1
    return iterations_count

def SSA_calculate_initial_sigma(puzzle, fixed_puzzle, block_list):
    differences_list = []
    temp_puzzle = puzzle
    for i in range(1, 10):
        temp_puzzle = SSA_proposed_state(temp_puzzle, fixed_puzzle, block_list)[0]
        differences_list.append(SSA_calculate_number_of_errors(temp_puzzle))
    return statistics.pstdev(differences_list)

def SSA_solve_sudoku(puzzle):
    solution_found = False
    max_iterations = 2000
    iterations = 0
    while not solution_found and iterations < max_iterations:
        decrease_factor = 0.99
        stuck_count = 0
        fixed_puzzle = [row[:] for row in puzzle]
        SSA_fix_puzzle_values(fixed_puzzle)
        list_of_blocks = SSA_create_list_3x3_blocks()
        temp_puzzle = SSA_randomly_fill_3x3_blocks(puzzle, list_of_blocks)
        sigma = SSA_calculate_initial_sigma(puzzle, fixed_puzzle, list_of_blocks)
        score = SSA_calculate_number_of_errors(temp_puzzle)
        iterations = SSA_choose_number_of_iterations(fixed_puzzle)

        if score <= 0:
            solution_found = True

        while not solution_found:
            previous_score = score
            for i in range(iterations):
                new_state = SSA_choose_new_state(temp_puzzle, fixed_puzzle, list_of_blocks, sigma)
                temp_puzzle = new_state[0]
                score_diff = new_state[1]
                if score_diff < 0:
                    score += score_diff
                if score <= 0:
                    solution_found = True
                    break
            iterations += 1  # Increment the iteration counter
            if iterations >= max_iterations:  # Check if max iterations reached
                print("Puzzle Failed")
                return None

            sigma *= decrease_factor
            if score <= 0:
                solution_found = True
                break
            if score >= previous_score:
                stuck_count += 1
            else:
                stuck_count = 0
            if stuck_count > 80:
                sigma += 2
            if SSA_calculate_number_of_errors(temp_puzzle) == 0:
                break
    return temp_puzzle

def SSA_print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(str(num) for num in row))

def SSA_run(puzzle):
    print("Starting SSA")
    solution = SSA_solve_sudoku(puzzle)
    if solution is not None:
        print("Puzzle Solved")
        SSA_print_puzzle(solution)


puzzle = [
    [0, 9, 6, 1, 5, 7, 0, 3, 0],
    [0, 1, 8, 0, 0, 6, 7, 0, 0],
    [0, 0, 3, 2, 0, 0, 1, 0, 0],
    [5, 3, 1, 6, 0, 0, 0, 0, 4],
    [6, 0, 0, 8, 0, 0, 0, 5, 0],
    [0, 0, 0, 5, 0, 9, 0, 0, 3],
    [9, 0, 0, 0, 1, 0, 3, 0, 8],
    [0, 8, 5, 7, 6, 0, 0, 2, 0],
    [0, 7, 0, 9, 0, 8, 5, 6, 0]
]

SSA_run(puzzle)

