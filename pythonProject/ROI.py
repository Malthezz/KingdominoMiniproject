import cv2
import numpy as np


# Function to assign labels based on HSV value
def label_color(hsv_value):
    h, s, v = hsv_value

    # Adjusted ranges for Water
    if (h >= 70 and h <= 110) and (s >= 190 and s <= 255) and (v >= 120 and v <= 190):
        return "Water"

    # Adjusted ranges for Sand
    elif (h >= 20 and h <= 30) and (s >= 230 and s <= 255) and (v >= 170 and v <= 255):
        return "Sand"

    # Adjusted ranges for Grass
    elif (h >= 32 and h <= 44) and (s >= 190 and s <= 220) and (v >= 120 and v <= 155):
        return "Grass"

    # Refined range for Rock
    elif (h >= 0 and h <= 30) and (s >= 50 and s <= 150) and (v >= 50 and v <= 150):
        return "Rock"

    # Adjusted ranges for Forrest
    elif (h >= 35 and h <= 50) and (s >= 100 and s <= 200) and (v >= 40 and v <= 100):
        return "Forest"

    # Adjusted ranges for Mines
    elif (h >= 0 and h <= 30) and (s >= 40 and s <= 150) and (v >= 0 and v <= 160):
        return "Mines"


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
image_path = 'Croppedandperspectivecorrectedboards/2.jpg'
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

        # Define ROI size (example: 50x50 pixels)
        roi_size = 55
        center_x = (x_start + x_end) // 2
        center_y = (y_start + y_end) // 2

        # Define the ROI coordinates
        roi_x_start = max(center_x - roi_size // 2, 0)
        roi_x_end = min(center_x + roi_size // 2, width)
        roi_y_start = max(center_y - roi_size // 2, 0)
        roi_y_end = min(center_y + roi_size // 2, height)

        if roi_x_start < roi_x_end and roi_y_start < roi_y_end:
            # Extract the ROI
            roi = img[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

        # Optional: Display or process the ROI as needed
        # For example, you can show the ROI (comment out if you don't want to display)
        cv2.imshow(f'ROI ({row}, {col})', roi)
        cv2.waitKey(20)
    else:
        print(f"Invalid ROI for cube ({row}, {col})")

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

def checkROI(roi, hsv_value, threshold_percentage):
    h, s, v = hsv_value
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # Create a mask that identifies pixels in the color range
    mask = cv2.inRange(hsv_roi, hsv_value)
    # Calculate the percentage of pixels in the ROI that match the color range
    matching_pixels = np.sum(mask > 0)
    total_pixels = roi.shape[0] * roi.shape[1]
    percentage = (matching_pixels / total_pixels) * 100

    # Return True if percentage exceeds the threshold
    return percentage > threshold_percentage

colour_ranges = {
        "Castle": (np.array([0,0,50]), np.array([0,0,0])),
        "Mill": (np.array([0, 0, 50]), np.array([0, 0, 0])),
        "Mine": (np.array([0, 0, 50]), np.array([0, 0, 0])),
        "Red": (np.array([0, 0, 50]), np.array([0, 0, 0])),
        "Yellow": (np.array([0, 0, 50]), np.array([0, 0, 0])),
    }

def labelROI(roi):
    for label, colour in colour_ranges.items():
        if checkROI(roi, hsv_value=colour, threshold_percentage=50):
            return label
        return "Unknown"



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
