from ctypes import sizeof
from textwrap import fill

import pygame

from pygame.draw import rect


WHITE = (200, 200, 200)
pygame.init()
screen = pygame.display.set_mode((500, 500))

grid = [[1] * 8 for n in range(8)]
grid[0][0] = 1
grid[7][7] = 1

print(grid)

w = 70  # width of each cell


def setup():
    sizeof(800, 600)


def draw():
    x, y = 0, 0  # starting position

    for row in grid:
        for col in row:
            if col == 1:
                fill(250, 0, 0)
            else:
                fill(255)
            rect(x, y, w, w)
            x = x + w  # move right
        y = y + w  # move down
        x = 0  # rest to left edge


def mousePressed():
   pass
    # integer division is good here!


pygame.quit()
