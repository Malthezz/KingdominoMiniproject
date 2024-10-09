import cv2
import numpy as np
from cv2 import waitKey

# Load and process the image
image = 'Croppedandperspectivecorrectedboards/1.jpg'
# Have checked 1,2,3,5,6,22,26,38
img = cv2.imread(path)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert to HSV

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


# Define color range for detecting the house's red/orange roof
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# Define colour range for roofs.
mask_red = cv2.inRange(img_hsv, lower_red, upper_red)
mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

# Minimum area threshold to filter out small detected areas (tiny regions)
min_area_threshold = 100  # You can adjust this based on your needs

# Find contours for the red/orange areas (houses)
contours_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
contours_yellow = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
# Filter out small ROIs that are not significant enough to count as houses
valid_contours_red = [cnt for cnt in contours_red if cv2.contourArea(cnt) >= min_area_threshold]
valid_contours_yellow = [cnt for cnt in contours_yellow if cv2.contourArea(cnt) >= min_area_threshold]

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
    yellow_roofs_on_water = 0
    red_roofs_on_grass = 0
    brown_roofs_on_grass = 0

    detected_houses_count = 0

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

            # Check if the cube overlaps with a valid detected house (red or yellow roof)
            cube_has_red_roof = any(
                cv2.pointPolygonTest(cnt, (x_start + cube_width // 2, y_start + cube_height // 2), False) >= 0 for cnt
                in valid_contours_red)
            cube_has_yellow_roof = any(
                cv2.pointPolygonTest(cnt, (x_start + cube_width // 2, y_start + cube_height // 2), False) >= 0 for cnt
                in valid_contours_yellow)

            # Debug output: print the average HSV color
            # print(f"Average HSV color for cube ({row}, {col}): {avg_color}")

            # Predict and assign the label based on the average color
            label = label_color(avg_color)

            # Store the result
            # cube_labels.append(((row, col), label, None))
            data = [(row,col),label,None]
            row_list.append(data)

            # Move the label counting code inside the loop
            if label == "Grass":
                grass_count += 1
                if cube_has_red_roof:
                    red_roofs_on_grass += 1
                    detected_houses_count += 1

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
                if cube_has_yellow_roof:
                    yellow_roofs_on_water += 1
                    detected_houses_count += 1

            elif label == "Sand":
                sand_count += 1
            elif label == "Castle":
                castle += 1
            elif label == "Table":
                table += 1
            else:
                label = label_color(avg_color, has_structure=(cube_has_red_roof or cube_has_yellow_roof))


            # print(f"Cube at position ({row}, {col}) labeled as {label}")

            # Update the text to include the water and house counts
            label_text = (f"{label}"
                          f"YR {yellow_roofs_on_water}")
            # stuff
            print(f"Yellow roofs on water: {yellow_roofs_on_water}")
            print(f"Red roofs on grass: {red_roofs_on_grass}")
            print(f"Detected houses count: {detected_houses_count}")
            cube_labels.append(row_list)
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




