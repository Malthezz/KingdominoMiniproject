import cv2
import numpy as np
from cv2 import waitKey

def crown1(image):
    #picture inputs
    img = cv2.imread(image)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert to HSV

    #Crown inputs
    # Convert it to grayscale
    imageCrown = cv2.imread(image)
    img_gray = cv2.cvtColor(imageCrown, cv2.COLOR_BGR2GRAY)

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
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

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
    cv2.imshow('Detected', img)
    cv2.waitKey(0)

# -----------------------------------------------------------------------------------------

# Function to assign labels based on HSV value
def label_color(hsv_value, has_structure=False):
    h, s, v = hsv_value

    # Adjusted ranges for Water

    if (h >= 70 and h <= 110) and (s >= 190 and s <= 255) and (v >= 112 and v <= 192):
        if has_structure:
            return "Under Structure"  # or "Obstructed Water"
        return "Water"

    # Adjusted ranges for Sand
    elif (h >= 20 and h <= 30) and (s >= 216 and s <= 255) and (v >= 141 and v <= 255):
        return "Sand"

    # Adjusted ranges for Grass
    elif (h >= 31 and h <= 49) and (s >= 161 and s <= 227) and (v >= 85 and v <= 160):
        return "Grass"

    # Refined range for Rock
    elif (h >= 18.5 and h <= 29.5) and (s >= 84 and s <= 167) and (v >= 73.5 and v <= 123):
        return "Rock"

    # Adjusted ranges for Mines
    elif (h >= 28 and h <= 51) and (s >= 69 and s <= 136) and (v >= 43 and v <= 80):
        return "Mines"

    # Adjusted ranges for Forrest
    elif (h >= 29 and h <= 52) and (s >= 100 and s <= 200) and (v >= 40 and v <= 76):
        return "Forest"

    # Adjusted ranges for Castle
    elif (h >= 23 and h <= 58) and (s >= 67 and s <= 140) and (v >= 71 and v <= 148):
        return "Castle"

    # Return Unknown for values that don't fit any category
    else:
        return "Table"

# creates the tilegrid [[[ grid ]]]
def tileGrid1(image):
    img = cv2.imread(image)
    grass_count = 0
    forest_count = 0
    wheat_count = 0
    mines_count = 0
    rock_count = 0
    water_count = 0
    sand_count = 0
    castle = 0
    table = 0

    # Define grid dimensions
    rows, cols = 5, 5
    height, width, _ = image.shape
    cube_height = height // rows
    cube_width = width // cols


    # Loop through the grid and assign labels to each cube
    cube_labels = []
    for row in range(rows):
        row_list =[]
        for col in range(cols):
            x_start, x_end = col * cube_width, (col + 1) * cube_width
            y_start, y_end = row * cube_height, (row + 1) * cube_height
            cube = image[y_start:y_end, x_start:x_end]

            # Calculate the average color in the cube (average HSV values)
            avg_color = cv2.mean(cube)[:3]  # Get average HSV values

            # Debug output: print the average HSV color
            # print(f"Average HSV color for cube ({row}, {col}): {avg_color}")

            # Predict and assign the label based on the average color
            label = label_color(avg_color)

            # Store the result
            # cube_labels.append(((row, col), label, None))
            data = [(row,col),label,None]
            row_list.append(data)

            # print(f"Cube at position ({row}, {col}) labeled as {label}")
            # print(cube_labels)
            # Draw a rectangle and label the color
            cv2.rectangle(img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)  # Draw rectangle
            cv2.putText(img, label, (x_start + 5, y_start + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Move the label counting code inside the loop
            if label == "Grass":
                grass_count += 1
            elif label == "Forest":
                forest_count += 1
            elif label == "Wheat":
                wheat_count += 1
            elif label == "Mines":
                mines_count += 1
            elif label == "Rock":
                rock_count += 1
            elif label == "Water":
                water_count += 1
            elif label == "Sand":
                sand_count += 1
            elif label == "Castle":
                castle += 1
            elif label == "Table":
                table += 1
        #stuff
        cube_labels.append(row_list)
    cv2.imshow('Detected', img)
    waitKey(0)
    return cube_labels

    '''# Example output: cube_labels contains the positions and corresponding predicted labels
    # Output the counts for each label
    print(f"Total Grass: {grass_count}")
    print(f"Total Forest: {forest_count}")
    print(f"Total Wheat: {wheat_count}")
    print(f"Total Mines: {mines_count}")
    print(f"Total Rock: {rock_count}")
    print(f"Total Water: {water_count}")
    print(f"Total Sand: {sand_count}")
    print(f"Total Castle: {castle}")
    print(f"Total Table: {table}")'''



