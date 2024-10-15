import cv2
import numpy as np

from pythonProject.NMS import non_max_suppression_fast
from pythonProject.New import tileGrid, label_color


#This part loads the templates put in Crown():
def load_templates(template_files):
    templates = []
    for template_file in template_files:
        template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
        templates.append(template)
    return templates

#This functions matches the templates from above into the image in Crown():
def match_templates(img_gray, templates, threshold=0.5):
    # This is an empty []
    rectangle_coords = []

    for template in templates:
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            # Define rectangle points
            top_left = pt
            top_right = (pt[0] + w, pt[1])
            bottom_left = (pt[0], pt[1] + h)
            bottom_right = (pt[0] + w, pt[1] + h)

            # Stores the crowns yellow rectangles
            rectangle_coords.append([top_left, top_right, bottom_left, bottom_right])

    return rectangle_coords

#Divides the image into rows and cols aka a grid.
def divide_into_grid(image, rows=5, cols=5):
    height, width, _ = image.shape
    cube_height = height // rows
    cube_width = width // cols
    grid_coords = []

    for row in range(rows):
        for col in range(cols):
            x_start, x_end = col * cube_width, (col + 1) * cube_width
            y_start, y_end = row * cube_height, (row + 1) * cube_height

            # puts the grids into the empty grid_coords' []
            grid_coords.append([(row, col), (x_start, y_start, x_end, y_end)])

    return grid_coords

#Displays the rectangles aka the grid for each tile.
def display_image_rectangle(image, rectangle_coords):
    for rect in rectangle_coords:
        top_left, top_right, bottom_left, bottom_right = rect
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 255), 2)

    cv2.imshow('Detected', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#This right here finds where the crowns are located into the grid.
def crowns_to_grid(rectangle_coords, grid_coords, rows, cols):
    crown_count = [[0 for _ in range(cols)] for _ in range(rows)]
    crown_ids = {}

    # ID counter
    current_crown_id = 0

    for rect in rectangle_coords:
        top_left = rect[0]
        for grid in grid_coords:
            (row,col), (x_start, y_start, x_end, y_end) = grid
            if x_start <= top_left[0] <= x_end and y_start <= top_left[1] <= y_end:
                crown_count[row][col] += 1
                crown_ids[current_crown_id] = (row, col)  # Assign ID to crown's grid position
                current_crown_id += 1
                break
                
                sorted_crowns = sorted(crown_ids, key=lambda grid: (row, col, rect))
                print(sorted_crowns)

    return crown_count, crown_ids

#Displays the rectangles and the grid.
def display_image_with_rectangles_and_grid(image, rectangle_coords, grid_coords):
    # Draw rectangles around matched crowns
    for rect in rectangle_coords:
        top_left, top_right, bottom_left, bottom_right = rect
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 255), 2)

    # Draw the grid over the image
    for grid in grid_coords:
        _, (x_start, y_start, x_end, y_end) = grid
        cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (255, 0, 0), 1)

    cv2.imshow('Detected Crowns with Grid', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#All the good stuff is put in here, so everything works elsewhere :) (hopefully)
def crown(image):
    img_rgb = cv2.imread(image)
    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # List of template file names
    template_files = [
        "1 Krone1 Desert.jpg",
        "1 Krone1 Desert 90.jpg", "1 Krone1 Desert 180.jpg", "1 Krone1 Desert 270.jpg",
        "1 Krone1 Grass.jpg",
        "1 Krone1 Grass 90.jpg", "1 Krone1 Grass 180.jpg", "1 Krone1 Grass 270.jpg",
        "1 Krone2 Desert.jpg",
        "1 Krone2 Desert 90.jpg", "1 Krone2 Desert 180.jpg", "1 Krone2 Desert 270.jpg",
        "1 Krone2 Grass.jpg",
        "1 Krone2 Grass 90.jpg", "1 Krone2 Grass 180.jpg", "1 Krone2 Grass 270.jpg",
        "1 Krone3 Desert.jpg",
        "1 Krone3 Desert 90.jpg", "1 Krone3 Desert 180.jpg", "1 Krone3 Desert 270.jpg",
        "1 Krone3 Grass.jpg",
        "1 Krone3 Grass 90.jpg", "1 Krone3 Grass 180.jpg", "1 Krone3 Grass 270.jpg",
        "1 Krone Skov.jpg",
        "1 Krone Skov 90.jpg", "1 Krone Skov 180.jpg", "1 Krone Skov 270.jpg",
        "1 Krone Water.jpg",
        "1 Krone Water 90.jpg", "1 Krone Water 180.jpg", "1 Krone Water 270.jpg",
        "4Krone1Sand.jpg",
        "4Krone1Sand90.jpg", "4Krone1Sand180.jpg", "4Krone1Sand270.jpg",
        "8Krone1Sand.jpg",
        "8Krone1Sand90.jpg","8Krone1Sand180.jpg","8Krone1Sand270.jpg",
        "9Krone1Sand.jpg",
        "9Krone1Sand90.jpg", "9Krone1Sand180.jpg", "9Krone1Sand270.jpg"
    ]
    templates = []

    for template_file in template_files:
        template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
        template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
        templates.append(template)

    # Perform template matching
    rectangle_coords = match_templates(img_gray, templates, 0.8)

    #NMS NON MAXIMUM SUPRESSON
    # Apply non-max suppression to reduce overlapping detections
    rectangle_coords = np.array([[
        rect[0][0], rect[0][1], rect[3][0], rect[3][1]
    ] for rect in rectangle_coords])  # Convert to (x1, y1, x2, y2) format

    if len(rectangle_coords) > 0:
        rectangle_coords = non_max_suppression_fast(rectangle_coords, 0.4)

    # Convert back to original (top-left, top-right, bottom-left, bottom-right) format
    rectangle_coords = [
        [(rect[0], rect[1]), (rect[2], rect[1]), (rect[0], rect[3]), (rect[2], rect[3])]
        for rect in rectangle_coords
    ]

    # Print matched rectangle coordinates
    # print("Matched Rectangle Coordinates:", np.array(rectangle_coords))

    rows, cols = 5,5
    # Divide the image into a grid
    grid_coords = divide_into_grid(img_rgb, 5, 5)

    # Map the crowns to their corresponding grid cells

    crown_count, crown_ids = crowns_to_grid(rectangle_coords, grid_coords, rows, cols)

    # Print crown count and IDs
    print("Crown count in each grid cell:")
    for row in crown_count:
        print(row)
    print("Crown IDs with their respective grid positions:")
    for crown_id, position in crown_ids.items():
        print(f"Crown ID {crown_id} at grid position {position}")

    # Display the image with matched template rectangles and grid
    display_image_with_rectangles_and_grid(img_rgb.copy(), rectangle_coords, grid_coords)


def point_calculator(image_path, grid, templates):
    from pythonProject.burn import ignite
    # Step 1: Count the connected blocks using `countpoints`.
    connected_blocks = []
    currentId = 0

    # Step 1: Count the connected blocks
    for y, rows in enumerate(grid):
        for x, cell in enumerate(rows):
            if cell[2] is None:
                label = cell[1]
                size, connected_tiles = ignite(label, y, x, grid, currentId)
                connected_blocks.append((size, connected_tiles))  # Store size and connected block tiles
                currentId += 1

    # Step 2: Detect crowns
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    crown_coords = match_templates(img_gray, templates)

    total_sum = 0

    # Step 3: For each connected block, multiply its size by the number of crowns within it
    for size, tiles in connected_blocks:
        crown_count = 0
        for tile in tiles:
            y, x = tile
            for crown in crown_coords:
                top_left, top_right, bottom_left, bottom_right = crown
                # Check if the tile falls within the crown's bounding box
                if top_left[0] <= x <= bottom_right[0] and top_left[1] <= y <= bottom_right[1]:
                    crown_count += 1

        # If there are crowns in this block, multiply block size by the crown count and add to total sum
        if crown_count > 0:
            block_value = size * crown_count
            print(f"Block of size {size} has {crown_count} crowns, value: {block_value}")
            total_sum += block_value

    print(f"Total sum: {total_sum}")
    return total_sum