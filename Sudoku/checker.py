def check(row, col, n, grid):
    # check row / col
    for i in range(9):
        # row check
        if n == grid[row][i]:
            return False
        # col check
        if n == grid[i][col]:
            return False

    # cube check
    sub_row = row // 3 * 3
    sub_col = col // 3 * 3

    for i in range(3):
        for j in range(3):
            if n == grid[sub_row + i][sub_col + j]:
                return False
    return True
