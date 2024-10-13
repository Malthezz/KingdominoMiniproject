import cv2
import numpy as np
from cv2 import waitKey

# Load and process the image
image_path = 'Croppedandperspectivecorrectedboards/5.jpg'
# Have checked 1,2,3,5,6,22,26,38
img = cv2.imread(image_path)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert to HSV

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
def tileGrid(image):
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



