def solve_n_queens(n):
    def backtrack(row, cols, diags, anti_diags, board):
        if row == n:
            solutions.append(["".join(row) for row in board])
            return
        for col in range(n):
            diag = row - col
            anti_diag = row + col
            if col in cols or diag in diags or anti_diag in anti_diags:
                continue
            cols.add(col)
            diags.add(diag)
            anti_diags.add(anti_diag)
            board[row][col] = 'Q'
            backtrack(row + 1, cols, diags, anti_diags, board)
            cols.remove(col)
            diags.remove(diag)
            anti_diags.remove(anti_diag)
            board[row][col] = '.'

    solutions = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    backtrack(0, set(), set(), set(), board)
    return solutions

if __name__ == "__main__":
    n = int(input("Enter board size (N): "))
    solutions = solve_n_queens(n)
    print(f"Found {len(solutions)} solutions for {n}-Queens:")
    for i, solution in enumerate(solutions[:3], 1):  # Show first 3 solutions
        print(f"\nSolution {i}:")
        for row in solution:
            print(row)