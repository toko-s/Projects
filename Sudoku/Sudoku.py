from turtle import mode

from generator import generate, generator_grid, generator_solved
import solver
import pygame as p
from checker import check
import time
import timeit

# # constants and globals
width = 1000
height = 600
diff = height / 9
screen = p.display.set_mode((width, height))
p.font.init()
font = p.font.Font('freesansbold.ttf', 40)
tips = p.font.Font('freesansbold.ttf', 20)
sub = p.font.Font('freesansbold.ttf', 80)
m = p.font.Font('freesansbold.ttf', 35)
grid = generator_grid
selected = False
sel_x = -1
sel_y = -1
original = [[]] * 9
solved = [[]] * 9
remaining = 0
won = False
correction = False
prev_time = 0
prev_higlight = (-1, -1)
prev_sub_higlight = (-1, -1)
sub_deff = 0
sub_grid = [9] * 9
mode = 0
lvl = 0.40
sub_sel = (False, 0)


def init():
    global remaining
    global solved
    global sub_grid
    global lvl
    lvl = 0.4 + 0.1 * mode
    sub_grid = [9] * 9
    generate(lvl)
    remaining = solver.count_zeros(grid)
    solved = generator_solved
    p.init()
    p.display.set_caption('Sudoku with solver')
    p.display.set_icon(p.image.load('icon.png'))
    screen.fill((204, 204, 204))
    draw_grid()
    draw_line()
    set_grid()
    draw_lvls()
    draw_instructions()
    for i in range(9):
        original[i] = grid[i].copy()
    for i in range(9):
        for j in range(9):
            sub_grid[j] -= grid[i].count(j + 1)
    draw_sub_grid()


def draw_instructions():
    t1 = tips.render('\'space\' --> correct wrong input', True, 'firebrick1')
    t2 = tips.render('\'R\' --> restart | \'Shift\' --> change mode', True, 'firebrick1')
    t3 = tips.render('\'Enter\' --> auto solver', True, 'firebrick1')
    screen.blit(t1, (610, 515))
    screen.blit(t2, (610, 545))
    screen.blit(t3, (610, 575))


def draw_lvls():
    a = ''
    global mode
    if mode == 0:
        a = 'Easy'
    elif mode == 1:
        a = 'Medium'
    elif mode == 2:
        a = 'Hard'
    elif mode == 3:
        a = 'Expert'
    t = m.render("Mode: " + a, True, 'cadetblue4')
    screen.blit(t, (660, 100))


def draw_sub_rect(x, y, color):
    x0 = 620
    x1 = 960
    y0 = 165
    sub_diff = (x1 - x0) / 3
    m = y * 3 + x
    p.draw.rect(screen, p.Color(color),
                (int(x0 + sub_diff * x + 1), int(y0 + sub_diff * y + 1), sub_diff - 1, sub_diff - 1))
    num = sub.render(str(m + 1), True, 'cyan3')
    screen.blit(num, (int(x0 + sub_diff * x + 34), int(y0 + sub_diff * y + 20)))


def draw_sub_grid():
    global sub_deff
    global sub_grid
    for i in range(3):
        for j in range(3):
            m = j * 3 + i
            if sub_grid[m] == 0:
                draw_sub_rect(i, j, 'lightgreen')
            else:
                draw_sub_rect(i, j, 'white')


def reset():
    generate(lvl)
    init()
    global won
    global remaining
    global prev_time
    won = False
    remaining = solver.count_zeros(grid)
    prev_time = p.time.get_ticks() // 1000


def draw_line():
    for i in range(9):
        p.draw.line(screen, (204, 204, 204), (0, i * diff), (height, i * diff), 2)
        p.draw.line(screen, (204, 204, 204), (i * diff, 0), (i * diff, height), 2)
    for i in range(4):
        p.draw.line(screen, (0, 0, 0), (0, 3 * i * diff), (height, 3 * i * diff), 3)
        p.draw.line(screen, (0, 0, 0), (3 * i * diff, 0), (3 * i * diff, height), 3)


def draw_rect(i, j, color):
    p.draw.rect(screen, p.Color(color), (int(diff * i + 2), int(diff * j + 2), int(diff - 2), int(diff - 2)))


def draw_grid():
    for i in range(9):
        for j in range(9):
            draw_rect(i, j, 'white')
    draw_line()


def set_num(n, x, y, color):
    global selected
    grid[x][y] = n
    draw_rect(x, y, color)
    reset_num(x, y)
    if not correction:
        selected = False


def set_grid():
    for i in range(9):
        for j in range(9):
            set_num(grid[i][j], i, j, 'white')


def highlight_num(n):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == n:
                draw_rect(i, j, 'Cyan4')
                num = font.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(num, (i * diff + 20, j * diff + 15))


def sub_mouse_action(pos):
    global sub_sel
    global selected
    global sel_x
    global sel_y
    x0 = 620
    x1 = 960
    y0 = 165
    sub_diff = (x1 - x0) / 3
    x = int((pos[0] - x0) // sub_diff)
    y = int((pos[1] - y0) // sub_diff)
    # draw_sub_rect(x, y, 'firebrick1')
    # p.display.update()
    # time.sleep(0.001)
    n = y * 3 + x + 1
    if selected and not original[sel_x][sel_y] and not won:
        key_action(n)
    else:
        if selected and original[sel_x][sel_y]:
            selected = False
            sel_x = -1
            sel_y = -1
        set_grid()
        sub_sel = (True, n)
        highlight_num(n)


def key_action(n):
    global correction
    global remaining
    global solved
    global grid
    global sub_grid
    if n == solved[sel_x][sel_y]:
        set_num(n, sel_x, sel_y, 'white')
        correction = False
        remaining -= 1
        sub_grid[n - 1] -= 1
        original[sel_x][sel_y] = True
        mouse_action((sel_x * diff + 1, sel_y * diff + 1))
    else:
        correction = True
        set_num(n, sel_x, sel_y, 'firebrick1')
    draw_sub_grid()


def mouse_action(pos):
    global sel_x
    global sel_y
    global selected
    global sub_sel

    set_grid()
    selected = True
    sel_x = int(pos[0] // diff)
    sel_y = int(pos[1] // diff)
    if grid[sel_x][sel_y]:
        highlight_num(grid[sel_x][sel_y])
        sub_sel = (True, grid[sel_x][sel_y])
    else:
        draw_rect(sel_x, sel_y, 'Cyan')
        sub_sel = (False, 0)


def reset_num(x, y):
    n = grid[x][y]
    if n:
        num = font.render(str(grid[x][y]), True, (0, 0, 0))
    else:
        num = font.render(str(), True, (0, 0, 0))
    screen.blit(num, (x * diff + 20, y * diff + 15))


def grid_highlight(pos):
    global prev_higlight
    global sub_sel
    draw_sub_grid()
    x = int(pos[0] // diff)
    y = int(pos[1] // diff)
    x_prev = prev_higlight[0]
    y_prev = prev_higlight[1]
    prev_higlight = (x, y)
    if not correction and (x_prev, y_prev) != (x, y):
        if (x_prev, y_prev) != (sel_x, sel_y):
            if sub_sel[0] and sub_sel[1] == grid[x_prev][y_prev]:
                highlight_num(sub_sel[1])
            elif grid[x_prev][y_prev] == grid[sel_x][sel_y] and selected and grid[sel_x][sel_y] != 0 :
                draw_rect(x_prev, y_prev, 'cyan4')
            else:
                draw_rect(x_prev, y_prev, 'white')
            reset_num(x_prev, y_prev)
        if grid[x][y] != grid[sel_x][sel_y] or grid[x][y] == 0 and (x, y) != (sel_x, sel_y):
            if grid[x][y] != sub_sel[1] or not sub_sel[0]:
                draw_rect(x, y, 'grey')
                reset_num(x, y)
    elif correction and (sel_x, sel_y) != (x_prev, y_prev):
        draw_rect(x_prev, y_prev, 'white')
        reset_num(x_prev, y_prev)


def sub_grid_highlight(pos):
    global prev_sub_higlight
    global prev_higlight
    global sub_sel
    if not correction:
        for i in range(9):
            for j in range(9):
                draw_rect(i, j, 'white')
                reset_num(i, j)
        draw_rect(sel_x, sel_y, 'cyan')
        if sub_sel[0]:
            highlight_num(sub_sel[1])

    x0 = 620
    x1 = 960
    y0 = 165
    sub_diff = (x1 - x0) / 3
    x = int((pos[0] - x0) // sub_diff)
    y = int((pos[1] - y0) // sub_diff)
    x_prev = prev_sub_higlight[0]
    y_prev = prev_sub_higlight[1]
    n = y_prev * 3 + x_prev
    if prev_sub_higlight != (x, y) and prev_sub_higlight != (-1, -1):
        prev_sub_higlight = (pos)
        if sub_grid[n]:
            draw_sub_rect(x_prev, y_prev, 'white')
        else:
            draw_sub_rect(x_prev, y_prev, 'lightgreen')
    draw_sub_rect(x, y, 'grey')
    prev_sub_higlight = (x, y)


def highlight():
    if p.mouse.get_pos()[0] < 600:
        grid_highlight(p.mouse.get_pos())
    elif 165 < p.mouse.get_pos()[1] < 505 and 620 < p.mouse.get_pos()[0] < 960:
        sub_grid_highlight(p.mouse.get_pos())


def display_time():
    p.draw.rect(screen, (204, 204, 204), (620, 20, 900, 60))
    time = p.time.get_ticks() // 1000 - prev_time
    str_time = '{0:02}'.format(time // 60) + ' : ' + '{0:02}'.format(time % 60)
    disp_time = font.render('Time | ' + str_time, True, (0, 0, 0))
    screen.blit(disp_time, (670, 20))


def graphic_solve():
    display_time()
    global remaining
    if remaining == 0:
        return True
    for j in range(9):
        for i in range(9):
            if grid[i][j] == 0:
                for n in range(1, 10):
                    # set_num(n, i, j, 'lightgreen')
                    # p.display.update()
                    if check(i, j, n, grid):
                        set_num(n, i, j, 'lightgreen')
                        p.display.update()
                        grid[i][j] = n
                        time.sleep(0.05)
                        remaining -= 1
                        if graphic_solve():
                            set_num(n, i, j, 'white')
                            p.display.update()
                            return True
                        remaining += 1
                        grid[i][j] = 0
                set_num(0, i, j, 'firebrick1')
                p.display.update()
                time.sleep(0.05)
                return False
    return False


if __name__ == '__main__':
    init()
    running = True
    while running:
        p.display.update()

        if not won:
            display_time()

        if remaining == 0:
            won = True
            txt = font.render('You win!', True, (0, 0, 0))
            txt1 = font.render('press R to restart', True, (0, 0, 0))
            p.draw.rect(screen, p.Color('green'), (diff * 2, diff * 3, diff * 6 - diff / 2, diff * 2))
            screen.blit(txt, (3 * diff + 20, 3 * diff + 15))
            screen.blit(txt1, (2 * diff + 20, 4 * diff + 15))

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if e.type == p.KEYDOWN:
                if selected and not original[sel_x][sel_y] and not won:
                    if e.key == p.K_1:
                        key_action(1)
                    elif e.key == p.K_2:
                        key_action(2)
                    elif e.key == p.K_3:
                        key_action(3)
                    elif e.key == p.K_4:
                        key_action(4)
                    elif e.key == p.K_5:
                        key_action(5)
                    elif e.key == p.K_6:
                        key_action(6)
                    elif e.key == p.K_7:
                        key_action(7)
                    elif e.key == p.K_8:
                        key_action(8)
                    elif e.key == p.K_9:
                        key_action(9)
                    elif e.key == p.K_SPACE and correction:
                        set_num(0, sel_x, sel_y, 'white')
                        correction = False
                        selected = False
                if e.key == p.K_r:
                    reset()
                if e.key == p.K_RETURN:
                    if correction:
                        set_num(0, sel_x, sel_y, 'white')
                    set_grid()
                    graphic_solve()
                if e.key == p.K_LSHIFT or e.key == p.K_RSHIFT:
                    mode += 1
                    if mode > 3:
                        mode = 0
                    reset()

            if e.type == p.MOUSEBUTTONDOWN and not won:
                m_pos = p.mouse.get_pos()
                if not correction:
                    if m_pos[0] < 600:
                        mouse_action(p.mouse.get_pos())
                if 165 < m_pos[1] < 505 and 620 < m_pos[0] < 960:
                    sub_mouse_action(m_pos)
            if e.type == p.MOUSEMOTION and not won:
                highlight()
