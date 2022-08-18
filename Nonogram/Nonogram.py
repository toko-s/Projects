import random

import pygame as p

from draw_mode import DrawMode

width = 600
height = 600
inner_size = 500
inner_start_x = width - inner_size
inner_start_y = height - inner_size
diff = inner_size / 16
draw_mode = DrawMode.RECT
grid = [[]] * 16
solved_grid = [[]] * 16
curr_x, curr_y = -1, -1
drawing = False
deleting = False
screen = p.display.set_mode((width, height))
p.font.init()
font = p.font.Font('freesansbold.ttf', 20)


def manage_mode(value):
    def decorator(func):
        def wrapper(x: int, y: int, color=p.Color('black')):
            global drawing
            global deleting
            if grid[x][y] == 0 and not deleting:
                if not drawing:
                    drawing = True
                func(x, y, color)
                grid[x][y] = value
            elif not drawing and grid[x][y] == value:
                deleting = True
                p.draw.rect(screen, p.Color('white'),
                            (inner_start_x + diff * x + 2, inner_start_y + diff * y + 2, diff - 2, diff - 2))
                grid[x][y] = 0

        return wrapper

    return decorator


@manage_mode(1)
def draw_rect(x: int, y: int, color):
    p.draw.rect(screen, color, (inner_start_x + diff * x + 2, inner_start_y + diff * y + 2, diff - 2, diff - 2))


@manage_mode(2)
def draw_cross(x: int, y: int, color=p.Color('black')):
    pos_x = inner_start_x + x * diff + 5
    pos_y = inner_start_y + y * diff + 5
    pos_x1 = pos_x + diff - 10
    pos_y1 = pos_y + diff - 10
    p.draw.line(screen, color, (pos_x, pos_y), (pos_x1, pos_y1), 6)
    p.draw.line(screen, color, (pos_x1, pos_y), (pos_x, pos_y1), 6)


def draw_grid():
    for i in range(16):
        pos_x = inner_start_x + i * diff
        pos_y = inner_start_y + i * diff
        p.draw.line(screen, (204, 204, 204), (pos_x, height - inner_size), (pos_x, height), 2)
        p.draw.line(screen, (204, 204, 204), (inner_start_x, pos_y), (width, pos_y), 2)


def initialize_ui():
    p.init()
    p.display.set_caption('Nonogram puzzle')
    draw_grid()


def initialize_game():
    for x in range(16):
        grid[x] = [0] * 16
        solved_grid[x] = [0] * 16
        for y in range(16):
            solved_grid[x][y] = int(random.uniform(0, 2))


if __name__ == "__main__":
    screen.fill(color=p.Color('white'))
    initialize_ui()
    initialize_game()
    running = True
    while running:
        p.display.update()

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if e.type == p.KEYUP:
                if e.key == p.K_SPACE:
                    if draw_mode == DrawMode.RECT:
                        draw_mode = DrawMode.CROSS
                    else:
                        draw_mode = DrawMode.RECT
            if (e.type == p.MOUSEMOTION and p.mouse.get_pressed()[0]) or e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                i = int((pos[0] - inner_start_x) // diff)
                j = int((pos[1] - inner_start_y) // diff)
                if (curr_x, curr_y) == (i, j):
                    continue
                curr_x, curr_y = i, j
                if i > 16 or j > 16 or pos[0] < inner_start_x or pos[1] < inner_start_y:
                    continue
                if draw_mode == DrawMode.RECT:
                    draw_rect(i, j)
                elif draw_mode == DrawMode.CROSS:
                    draw_cross(i, j)
            if e.type == p.MOUSEBUTTONUP:
                curr_x, curr_y = -1, -1
                deleting, drawing = False, False
