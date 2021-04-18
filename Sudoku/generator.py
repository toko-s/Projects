import solver
from checker import check
from random import uniform, randrange

generator_grid = [[]] * 9
generator_solved = [[]] * 9


def _generate(checked):
    if checked == 81:
        return True
    for i in range(9):
        for j in range(9):
            if generator_grid[i][j] == 0:
                row = list(range(1, 10))
                for _ in range(9):
                    n = row.pop(randrange(0, len(row)))
                    if check(i, j, n, generator_grid):
                        generator_grid[i][j] = n
                        generator_solved[i][j] = n
                        checked += 1
                        if _generate(checked):
                            return True
                        generator_grid[i][j] = 0
                        generator_solved[i][j] = 0
                        checked -= 1

                return False
    return False


def _clear(lvl):
    for i in range(9):
        for j in range(9):
            if uniform(0, 1) < lvl:
                generator_grid[i][j] = 0


def generate(lvl):
    global generator_grid
    global generator_solved
    for _ in range(9):
        generator_grid[_] = [0] * 9
        generator_solved[_] = [0] * 9
    _generate(0)
    _clear(lvl)


if __name__ == '__main__':
    level = 0.4
    generate(level)
    print('Initial board!')
    print(*generator_grid, sep='\n')
    print('take a good look')
    import time

    time.sleep(3)
    print('lets solve this cunt')
    time.sleep(3)
    solver.solve(generator_grid)
    print('Here\'s final board')
    print(*generator_grid, sep='\n')
    print('congrats it only took ', solver.iteration, 'iteration!')
