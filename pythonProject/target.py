import cv2
import numpy as np

def crown(image):

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
        "1 Krone Water 90.jpg", "1 Krone Water 180.jpg", "1 Krone Water 270.jpg"
    ]

    # List to store the grayscale templates
    templates = []

    for template_file in template_files:
        template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
        template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
        templates.append(template)

    # best current results (30,30) and (3,3) and thresh = 7!!
    # template = cv2.resize(template, (30,30))
    # template = cv2.GaussianBlur(template, (3, 3), 10,10,10, cv2.BORDER_DEFAULT)

    # cv2.imshow('crown_blur', template)

    # Store width and height of template in w and h
    w, h = template.shape[::-1]

    # Perform match operations.
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    threshold = 0.6

    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)

    rectangle_coords = []

    # Draw a rectangle around the matched region.
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

        # Define the rectangle points
        top_left = pt
        top_right = (pt[0] + w, pt[1])  # x increases by width, y remains the same
        bottom_left = (pt[0], pt[1] + h)  # x remains the same, y increases by height
        bottom_right = (pt[0] + w, pt[1] + h)  # x increases by width, y increases by height

        # Add rectangle coordinates to the list
        rectangle_coords.append([top_left, top_right, bottom_left, bottom_right])

    rectangle_coords_np = np.array(rectangle_coords)

    print("Rectangle Coordinates:"
    , rectangle_coords_np)


    # Show the final image with the matched area.
    cv2.imshow('Detected', img_rgb)
    cv2.waitKey(0)

#This part loads the templates put in Crown():
def load_templates(template_files):
    templates = []
    for template_file in template_files:
        template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
        templates.append(template)
    return templates

#This functions matches the templates from above into the image in Crown():
def match_templates(img_gray, templates, threshold=0.6):
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
    for rect in rectangle_coords:
        top_left = rect[0]
        for grid in grid_coords:
            (row,col), (x_start, y_start, x_end, y_end) = grid

            if x_start <= top_left[0] <= x_end and y_start <= top_left[1] <= y_end:
                crown_count[row][col] += 1
                break
        #sorted_crowns = sorted(crown_grid, key=lambda grid: (row,col,rect))
        #print(sorted_crowns)
    return crown_count

#All the good stuff is put in here, so everything works elsewhere :) (hopefully)
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
        "1 Krone Water 90.jpg", "1 Krone Water 180.jpg", "1 Krone Water 270.jpg"
    ]

    # List to store the grayscale templates
    templates = []

    for template_file in template_files:
        template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
        template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
        templates.append(template)

    # Perform template matching
    rectangle_coords = match_templates(img_gray, templates, 0.8)

    # Print matched rectangle coordinates
    print("Matched Rectangle Coordinates:", np.array(rectangle_coords))

    rows, cols = 5,5
    # Divide the image into a grid
    grid_coords = divide_into_grid(img_rgb, 5, 5)

    # Map the crowns to their corresponding grid cells
    crown_count = crowns_to_grid(rectangle_coords, grid_coords, rows, cols)

    # Display the crown count grid
    print("Crown count in each grid cell:")
    for row in crown_count:
        print(row)

    # Display the image with matched template rectangles and grid
    display_image_with_rectangles_and_grid(img_rgb.copy(), rectangle_coords, grid_coords)

