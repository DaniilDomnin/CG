import time
from math import floor

import matplotlib.pyplot as plt
import numpy as np


def fill_area(plot, x, y, color):
    x_start = x // width * width
    x_end = x_start + width
    y_start = y // height * height
    y_end = y_start + height
    plot.fill_between([x_start, x_end], [y_end, y_end], [y_start, y_start], color=color)


def step_algorithm(plot, x1, y1, x2, y2, color):
    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1
        for i in range(y1, y2 + 1):
            fill_area(plot, x1, i, color)
        return

    dx = x2 - x1
    dy = y2 - y1
    k = dy / dx
    b = (x2 * y1 - x1 * y2) / dx

    if x1 > x2:
        x1, x2 = x2, x1

    for i in range(x1, x2 + 1):
        fill_area(plot, i, floor(i * k + b), color)


def bresenham_algorithm(plot, x0, y0, x1, y1, color):
    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = abs(y1 - y0)
    error = dx / 2
    ystep = 1 if y0 < y1 else -1
    y = y0

    for x in range(x0, x1 + 1):
        if steep:
            fill_area(plot, y, x, color)
        else:
            fill_area(plot, x, y, color)
        error -= dy
        if error < 0:
            y += ystep
            error += dx


if __name__ == "__main__":
    x1dda, y1dda, x2dda, y2dda = map(int, input("Enter x1, y1, x2, y2 DDA\n").strip().split())
    x1br, y1br, x2br, y2br = map(int, input("Enter x1, y1, x2, y2 Bresenham\n").strip().split())

    # Plot set
    scale_x = 15
    scale_y = 15
    fig = plt.figure()
    plot = fig.add_subplot(1, 1, 1)
    plot.grid(which='both')
    x_max = max(x1dda, x2dda, x1br, x2br) * 1.05
    y_max = max(y1dda, y2dda, y1br, y2br) * 1.05
    plt.ylim(0, y_max)
    plt.xlim(0, x_max)
    plt.xticks(np.arange(0, x_max, x_max // scale_x))
    plt.yticks(np.arange(0, y_max, y_max // scale_y))
    plt.xlabel('x')
    plt.ylabel('y')
    width = x_max // scale_x
    height = y_max // scale_y

    # Draw lines
    plot.plot([x1dda, x2dda], [y1dda, y2dda], color='orange', label="Line 1 - Step")
    plot.plot([x1br, x2br], [y1br, y2br], color='purple', label="Line 2 - Bresenham")

    start_time = time.time()
    # DDA
    step_algorithm(plot, x1dda, y1dda, x2dda, y2dda, "red")
    end_time = time.time()
    time_dda = end_time - start_time

    start_time = time.time()
    # Bresenham
    bresenham_algorithm(plot, x1br, y1br, x2br, y2br, "blue")
    end_time = time.time()
    time_bresenham = end_time - start_time

    #
    print("Step time:", time_dda, "seconds")
    print("Bresenham time:", time_bresenham, "seconds")
    plot.legend()
    plt.show()
