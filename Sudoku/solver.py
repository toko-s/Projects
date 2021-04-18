import time
from checker import check


def count_zeros(grid):
    # global grid
    res = 0
    for i in range(9):
        res += grid[i].count(0)
    return res


def _solve(grid, remaining):
    if remaining == 0:
        return True
    global iteration
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for n in range(1, 10):
                    if check(i, j, n, grid):
                        iteration += 1
                        grid[i][j] = n
                        remaining -= 1
                        # print(*grid,sep = '\n')
                        # print('-----------------------')
                        # time.sleep(0.2)
                        if _solve(grid, remaining):
                            return True

                        remaining += 1
                        grid[i][j] = 0

                return False
    return False


def solve(grid):
    _solve(grid, count_zeros(grid))


iteration = 0

if __name__ == '__main__':
    grid_s = [[] * 9] * 9
    for _ in range(9):
        grid_s[_] = [0] * 9
    remaining_s = count_zeros(grid_s)
    print(remaining_s)
    # print(*grid,sep = '\n')
    print('starting solve!')
    _solve(grid_s, 0, 0, remaining_s)
    print(*grid_s, sep='\n')
    print('the result')
