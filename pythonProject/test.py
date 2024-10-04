import cv2
import numpy as np

# Load the image
image_path = 'Croppedandperspectivecorrectedboards/3.jpg'
img = cv2.imread(image_path)

# Convert to HSV color space
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define grid dimensions
rows, cols = 5, 5
height, width, _ = img.shape
cube_height = height // rows
cube_width = width // cols

# Define color ranges for detecting houses
house_color_ranges = {
    "Red House": ((0, 100, 100), (20, 255, 255)),  # Reddish-Brown range for houses
    "Yellow": ((25, 100, 100), (35, 200, 200)),  # Yellow range for houses
    "Mine": ((25, 100, 35), (25, 255, 60)),    # Brown range for mines
    "Bronw": ((10, 100, 100), (22, 200, 150)),    # Brown range for mines
    
}


# Function to detect house color in the specified region
def detect_houses(house_cube):
    avg_color = cv2.mean(house_cube)[:3]  # Get average HSV for the house cube
    for label, (lower, upper) in house_color_ranges.items():
        if all(lower[i] <= avg_color[i] <= upper[i] for i in range(3)):
            return label
    return None


# Processing the grid for house detection only
for row in range(rows):
    for col in range(cols):
        x_start, x_end = col * cube_width, (col + 1) * cube_width
        y_start, y_end = row * cube_height, (row + 1) * cube_height

        # Check for houses in a larger region around the center of the block
        center_x, center_y = (x_start + x_end) // 2, (y_start + y_end) // 2
        house_cube = img_hsv[max(0, center_y - 20):min(height, center_y + 15),
                     max(0, center_x - 20):min(width, center_x + 15)]  # Larger region for house detection

        house_label = detect_houses(house_cube)  # Check for houses in the center

        # Draw a rectangle if a house is detected
        if house_label:
            cv2.rectangle(img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)  # Draw rectangle
            cv2.putText(img, house_label, (x_start + 5, y_start + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                        1)

# Show the final image with detected house labels
cv2.imshow('Detected Houses', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
