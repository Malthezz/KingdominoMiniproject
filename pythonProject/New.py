import cv2
import numpy as np

# Function to assign labels based on HSV value
def label_color(hsv_value, has_structure=False):
    h, s, v = hsv_value

    # Adjusted ranges for Water
    if (h >= 70 and h <= 100) and (s >= 200 and s <= 255) and (v >= 100 and v <= 255):
        if has_structure:
            return "Under Structure"  # or "Obstructed Water"
        return "Water"

    # Adjusted ranges for Sand
    elif (h >= 20 and h <= 40) and (s >= 100 and s <= 255) and (v >= 50 and v <= 255):
        return "Sand"

    # Adjusted ranges for Grass
    elif (h >= 40 and h <= 70) and (s >= 100 and s <= 255) and (v >= 50 and v <= 255):
        return "Grass"

    # Refined range for Rock
    elif (h >= 0 and h <= 30) and (s >= 50 and s <= 150) and (v >= 50 and v <= 150):
        return "Rock"

    # Adjusted ranges for Forrest
    elif (h >= 0 and h <= 110) and (s >= 0 and s <= 255) and (v >= 10 and v <= 187):
        return "Forrest"

    # Return Unknown for values that don't fit any category
    else:
        return "Unknown"


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

# Example output: cube_labels contains the positions and corresponding predicted labels
cv2.imshow('Detected', img_hsv)
cv2.waitKey(0)
