from collections import deque
from inspect import stack
from itertools import count

import cv2
import numpy as np

# Function to assign labels based on HSV value
def label_color(hsv_value, has_structure=False):
    h, s, v = hsv_value


    # Adjusted ranges for Water
    if (h >= 60 and h <= 120) and (s >= 200 and s <= 255) and (v >= 100 and v <= 255):
        return "Water"

    # Adjusted ranges for Sand
    elif (h >= 20 and h <= 40) and (s >= 100 and s <= 255) and (v >= 150 and v <= 255):
        return "Sand"

    # Adjusted ranges for Grass
    elif (h >= 40 and h <= 55) and (s >= 100 and s <= 255) and (v >= 80 and v <= 255):
        return "Grass"

    # Refined range for Rock
    elif (h >= 0 and h <= 30) and (s >= 50 and s <= 150) and (v >= 50 and v <= 150):
        return "Rock"

    # Adjusted ranges for Forest
    elif (h >= 40 and h <= 50) and (s >= 100 and s <= 255) and (v >= 0 and v <= 100):
        return "Forest"

    # Adjusted ranges for Mine
    elif (h >= 20 and h <= 40) and (s >= 100 and s <= 255) and (v >= 150 and v <= 255):
        return "Mind"

    # Return Unknown for values that don't fit any category
    else:
        return "Unknown"

# 0
grass_count = 0
forest_count = 0
wheat_count = 0
mines_count = 0
rock_count = 0
water_count = 0
sand_count = 0
unknown = 0

# Load and process the image
image_path = 'Croppedandperspectivecorrectedboards/1.jpg'
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
        elif label == "Unknown":
            unknown += 1

# Example output: cube_labels contains the positions and corresponding predicted labels
    # Output the counts for each label
    print(f"Total Grass: {grass_count}")
    print(f"Total Forest: {forest_count}")
    print(f"Total Wheat: {wheat_count}")
    print(f"Total Mines: {mines_count}")
    print(f"Total Rock: {rock_count}")
    print(f"Total Water: {water_count}")
    print(f"Total Sand: {sand_count}")
    print(f"Total Unknown: {unknown}")
cv2.imshow('Detected', img_hsv)
cv2.waitKey(0)
