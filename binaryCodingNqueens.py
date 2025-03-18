from pysat.solvers import Glucose3 # type: ignore
import math
def generate_variables(n):
    return [[i * n + j + 1 for j in range (n)] for i in range(n)]

def convert_to_binary(variables, n):
    bit_length = math.ceil(math.log2(n * n))  # Số bit cần dùng
    return [format(num - 1, f'0{bit_length}b') for num in variables]

def at_least_one(clauses, variables):
    clauses.append(variables)

def at_most_one(clauses, variables, y_vars):
    bit_length = len(y_vars)
    binary_vars = convert_to_binary(variables, bit_length)
    print(binary_vars)
    print()
    for i in range(0, len(variables)):
        bit_code = binary_vars[i]
        k = 0
        for j in range(bit_length - 1, -1, -1):
            if bit_code[j] == '0':
                clauses.append([-variables[i], -y_vars[k]])
            else:
                clauses.append([-variables[i], y_vars[k]])
            k += 1
    return clauses

def exactly_one(clauses, variables, y_vars):
    at_least_one(clauses, variables)
    at_most_one(clauses, variables, y_vars)

def generate_clauses(n, board):
    clauses = []
    y_vars = y_vars = [n * n + 1 + j for j in range(math.ceil(math.log2(n * n)))]
    
    #exactly one in row
    for i in range(n):
        row_vars = board[i]
        exactly_one(clauses, row_vars, y_vars)
    
    for j in range(n):
        col_vars = [board[i][j] for i in range (n)]
        exactly_one(clauses, col_vars, y_vars)
    
    #duong cheo chinh
    for j in range(n):
        col = j
        row = 0
        diagonal = []
        while col < n and row < n:
            diagonal.append(board[row][col])
            col += 1
            row += 1
        
        at_most_one(clauses, diagonal, y_vars)
    
    for j in range(n - 1, -1, -1):
        col = j
        row = 0
        diagonal = []
        while col >= 0 and row < n:
            diagonal.append(board[row][col])
            col -= 1
            row += 1
        at_most_one(clauses, diagonal, y_vars)
    
    for i in range(1, n):
        row = i
        col = 0
        diagonal = []
        while row < n and col < n:
            diagonal.append(board[row][col])
            row += 1
            col += 1
        at_most_one(clauses, diagonal, y_vars)

    for i in range(1, n):
        row = i
        col = n - 1
        diagonal = []
        while row < n and col >= 0:
            diagonal.append(board[row][col])
            row += 1
            col -=  1
        at_most_one(clauses, diagonal, y_vars)
    
    return clauses


def solve_nqueens(n):
    board = generate_variables(n)
    clauses = generate_clauses(n, board)
    print(clauses)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * n + j] > 0) for j in range (n)] for i in range (n)]
    return None

def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        print(solution)
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))



n = 3
solution = solve_nqueens(3)
print_solution(solution)

