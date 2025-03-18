from pysat.solvers import Glucose3 # type: ignore

def generate_variables(n):
    return [[i * n + j + 1 for j in range (n)] for i in range (n)]

def at_least_one(clauses, variables):
    clauses.append(variables)

def at_most_one(clauses, variables):
    for i in range(0, len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])
    return clauses

def exactly_one(clauses, variables):
    at_least_one(clauses, variables)
    at_most_one(clauses, variables)

def generate_clauses(n, board):
    clauses = []

    #exactly one in row
    for i in range(n):
        row_vars = board[i]
        exactly_one(clauses, row_vars)
    
    for j in range (n):
        column_vars = [board[i][j] for i in range(n)]
        exactly_one(clauses, column_vars)

    for i in range(n):
        for j in range(n):
            for k in range(1, n):
                if i + k < n and j + k < n:
                    at_most_one(clauses, [board[i][j], board[i + k][j + k]])
                if i + k < n and j - k >= 0:
                    at_most_one(clauses, [board[i][j], board[i + k][j - k]])

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


n = 8
solution = solve_nqueens(4)
print_solution(solution)
