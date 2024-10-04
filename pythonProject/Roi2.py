import cv2
import numpy as np

# Loop through the grid and assign labels to each cube
castle_count = 0
mill_count = 0
mine_count = 0
yellow_count = 0
red_count = 0
unknown_count = 0

# Load and process the image
image_path = 'Croppedandperspectivecorrectedboards/1.jpg'
img = cv2.imread(image_path)

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert to HSV

# Define grid dimensions
rows, cols = 5, 5
height, width, _ = img.shape
cube_height = height // rows
cube_width = width // cols

# Processing the grid
for row in range(rows):
    for col in range(cols):
        x_start, x_end = col * cube_width, (col + 1) * cube_width
        y_start, y_end = row * cube_height, (row + 1) * cube_height
        cube = img_hsv[y_start:y_end, x_start:x_end]

        # Calculate the average HSV color
        avg_color = cv2.mean(cube)[:3]  # mean returns B, G, R, A

        print(f"Average HSV color for cube ({row}, {col}): {avg_color}")

        # Define ROI size (example: 50x50 pixels)
        roi_size = 55
        center_x = (x_start + x_end) // 2
        center_y = (y_start + y_end) // 2

        # Define the ROI coordinates40
        roi_x_start = max(center_x - roi_size // 2, 0)
        roi_x_end = min(center_x + roi_size // 2, width)
        roi_y_start = max(center_y - roi_size // 2, 0)
        roi_y_end = min(center_y + roi_size // 2, height)

        if roi_x_start < roi_x_end and roi_y_start < roi_y_end:
            # Extract the ROI
            roi = img[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

            # Color ranges for label identification
            # the first is lower bound, the second is upper.
            colour_ranges = {
                "Castle": (np.array([45, 10, 15]), np.array([55, 19, 21])),
                "Mill": (np.array([0, 0, 0]), np.array([0, 0, 50])),
                "Mine": (np.array([0, 0, 0]), np.array([0, 0, 50])),
                "Red": (np.array([0,100,100]), np.array([10,255,255])),
                "Yellow": (np.array([0, 0, 0]), np.array([0, 0, 50])),
                "Unknown": (np.array([0, 0, 0]), np.array([0, 0, 0])),
            }

            # Get the label for the ROI
            label = labelROI(roi)  # Ensure this call is correct


            def labelROI(roi):
                for label, hsv_range in colour_ranges.items():
                    if label == "Red" or label == "Red_Upper":
                        if checkROI(roi, hsv_range):
                            return "Red"  # Return the label if it matches
                    else:
                        if checkROI(roi, hsv_range):
                            return label  # Return the label if it matches
                return "Unknown"  # Default return value if no match found

            def checkROI(roi, hsv_range):
                lower, upper = hsv_range
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_roi, lower, upper)

                # Calculate the percentage of pixels in the ROI that match the color range
                matching_pixels = np.sum(mask > 0)
                total_pixels = roi.shape[0] * roi.shape[1]


            cv2.imshow(f'ROI ({row}, {col}) - {label}', roi)
            cv2.waitKey(20)
        else:
            print(f"Invalid ROI for cube ({row}, {col})")


            # Count the labels
            if label == "Castle":
                castle_count += 1
            elif label == "Mill":
                mill_count += 1
            elif label == "Mine":
                mine_count += 1
            elif label == "Yellow":
                yellow_count += 1
            elif label == "Red":
                red_count += 1
            else:
                unknown_count += 1

# Output the counts for each label
print(f"Total Castles: {castle_count}")
print(f"Total Mills: {mill_count}")
print(f"Total Mines: {mine_count}")
print(f"Total Yellows: {yellow_count}")
print(f"Total Reds: {red_count}")
print(f"Total Unknown: {unknown_count}")

cv2.imshow('Detected', img_hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()
