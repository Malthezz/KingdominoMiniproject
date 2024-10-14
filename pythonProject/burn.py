from collections import deque

import cv2
from pythonProject.New import tileGrid
from pythonProject.target import crown, divide_into_grid, crowns_to_grid


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
def ignite(tileType, y, x, grid, label_id):
    queue = deque([])
    queue.append((y, x))
    size = 0
    connected_tiles = []

    while queue:
        curry, currx = queue.popleft()

        if grid[curry][currx][2] == None:
            grid[curry][currx][2] = label_id
            size += 1
            connected_tiles.append((curry, currx))

            checkConnections(tileType, queue, curry, currx, grid)

    return size, connected_tiles

# tells and counts the size of the blobs and puts an id.
def countpoints(path):
    img = cv2.imread(path)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    grid = tileGrid(img,img_hsv)
    currentId = 0

    for y, rows in enumerate(grid):
        for x, cell in enumerate(rows):
            if cell[2] is None:
                label = cell[1]
                size, connected_tiles = ignite(label, y, x, grid, currentId)
                coordinates = (y, x)
                print(size, "Blocks are connected", "with id", currentId, label, connected_tiles)
                currentId += 1
