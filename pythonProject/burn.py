from collections import deque

import cv2
import numpy as np
from cv2 import waitKey, rectangle
from sipbuild.generator.parser.annotations import string

from pythonProject.New import tileGrid, img_hsv

# goes through each tile and sees if any connecting tile matches
def checkConnections(tileType, que, y, x, grid):
    #checks the grid (if out of range)
    rows, cols = len(grid), len(grid[0])

    #the kernel: (maybe)
    if y > 0 and grid[y - 1][x][1] == tileType and grid[y - 1][x][2] is None:
        que.append((y - 1, x))
    if x > 0 and grid[y][x - 1][1] == tileType and grid[y][x - 1][2] is None:
        que.append((y, x - 1))
    if y < rows - 1 and grid[y + 1][x][1] == tileType and grid[y + 1][x][2] is None:
        que.append((y + 1, x))
    if x < cols - 1 and grid[y][x + 1][1] == tileType and grid[y][x + 1][2] is None:
        que.append((y, x + 1))

# function that will burn everything that has not been burned before.
def ignite(tileType, y, x, grid, id):
    queue = deque([])
    queue.append((y, x))
    size = 0

    while len(queue) > 0:
        curry, currx = queue.popleft()
        if grid[curry][currx][2] == None:
            grid[curry][currx][2] = id
            checkConnections(tileType, queue, curry, currx, grid)
            size += 1

    return size


# tells and counts the size of the blobs and puts an id.
def countpoints(path):
    img = cv2.imread(path)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    grid = tileGrid(img_hsv)
    currentId = 0

    for y, rows in enumerate(grid):
        for x, list in enumerate(rows):
            if list[2] is None:
                size = ignite(list[1], y, x, grid, currentId)
                ignite(list[1], y, x, grid, currentId)
                currentId += 1
                print(size, "Blocks are connected", "with id", currentId)

def draw_rectangle(tileGrid, image):
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    x_start = tileGrid['x_start']
    y_start = tileGrid['y_start']
    x_end = tileGrid['x_end']
    y_end = tileGrid['y_end']
    label_text = tileGrid['label_text']

    # Draw a rectangle and label the color
    cv2.rectangle(img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)  # Draw rectangle
    cv2.putText(img, label_text, (x_start + 5, y_start + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imshow('Detected', img)
    waitKey(0)

draw_rectangle("Croppedandperspectivecorrectedboards/4.jpg")
countpoints("Croppedandperspectivecorrectedboards/4.jpg")

