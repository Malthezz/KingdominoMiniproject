import cv2
import numpy as np
from numpy.ma.core import empty


# Function to assign labels based on HSV value
def label_color(hsv_value, has_structure=False):
    h, s, v = hsv_value

    # Adjusted ranges for Water

    if (h >= 70 and h <= 110) and (s >= 190 and s <= 255) and (v >= 115 and v <= 192):
        if has_structure:
            return "Under Structure"  # or "Obstructed Water"
        return "Water"

    # Adjusted ranges for Sand
    elif (h >= 20 and h <= 30) and (s >= 217 and s <= 255) and (v >= 141 and v <= 255):
        return "Sand"

    # Adjusted ranges for Grass
    elif (h >= 32 and h <= 48) and (s >= 184 and s <= 225) and (v >= 95 and v <= 160):
        return "Grass"

    # Refined range for Rock
    elif (h >= 20 and h <= 30) and (s >= 80 and s <= 167) and (v >= 72 and v <= 118):
        return "Rock"

    # Adjusted ranges for Mines
    elif (h >= 25 and h <= 50) and (s >= 72 and s <= 140) and (v >= 50 and v <= 80):
        return "Mines"

    # Adjusted ranges for Forrest
    elif (h >= 34 and h <= 52) and (s >= 100 and s <= 200) and (v >= 40 and v <= 76):
        return "Forest"

    # Adjusted ranges for Castle
    elif (h >= 23 and h <= 52) and (s >= 70 and s <= 135) and (v >= 71 and v <= 148):
        return "Castle"

    # Return Unknown for values that don't fit any category
    else:
        return "Table"

# 0
grass_count = 0
forest_count = 0
wheat_count = 0
mines_count = 0
rock_count = 0
water_count = 0
sand_count = 0
castle = 0
table = 0

# Load and process the image
image_path = 'Croppedandperspectivecorrectedboards/1.jpg'
# Have checked 1,2,3,5,6,22,26,38
img = cv2.imread(image_path)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert to HSV

# Define grid dimensions
rows, cols = 5, 5
height, width, _ = img.shape
cube_height = height // rows
cube_width = width // cols

# Loop through the grid and assign labels to each cube
cube_labels = []
for row in range(rows):
    for col in range(cols):
        x_start, x_end = col * cube_width, (col + 1) * cube_width
        y_start, y_end = row * cube_height, (row + 1) * cube_height
        cube = img_hsv[y_start:y_end, x_start:x_end]

        # Calculate the average color in the cube (average HSV values)
        avg_color = cv2.mean(cube)[:3]  # Get average HSV values

        # Debug output: print the average HSV color
        print(f"Average HSV color for cube ({row}, {col}): {avg_color}")

        # Predict and assign the label based on the average color
        label = label_color(avg_color)

        # Store the result
        cube_labels.append(((row, col), label))
        print(f"Cube at position ({row}, {col}) labeled as {label}")

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

# Example output: cube_labels contains the positions and corresponding predicted labels
# Output the counts for each label
    print(f"Total Grass: {grass_count}")
    print(f"Total Forest: {forest_count}")
    print(f"Total Wheat: {wheat_count}")
    print(f"Total Mines: {mines_count}")
    print(f"Total Rock: {rock_count}")
    print(f"Total Water: {water_count}")
    print(f"Total Sand: {sand_count}")
    print(f"Total Castle: {castle}")
    print(f"Total Table: {table}")
cv2.imshow('Detected', img_hsv)
cv2.waitKey(0)
