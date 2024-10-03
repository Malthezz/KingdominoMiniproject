import cv2
import numpy as np


# Function to assign labels based on HSV value
def label_color(hsv_value):
    h, s, v = hsv_value

    # Define color ranges for labeling
    if (60 <= h <= 120) and (200 <= s <= 255) and (100 <= v <= 255):
        return "Water"
    elif (20 <= h <= 40) and (100 <= s <= 255) and (150 <= v <= 255):
        return "Sand"
    elif (40 <= h <= 55) and (100 <= s <= 255) and (100 <= v <= 255):
        return "Grass"
    elif (0 <= h <= 30) and (50 <= s <= 150) and (50 <= v <= 150):
        return "Rock"
    elif (40 <= h <= 50) and (100 <= s <= 255) and (0 <= v <= 100):
        return "Forest"
    elif (20 <= h <= 40) and (100 <= s <= 255) and (150 <= v <= 255):
        return "Mine"
    else:
        return "Unknown"


# Flood fill algorithm to count connected tiles
def flood_fill(grid, visited, row, col, label):
    stack = [(row, col)]
    count = 0

    while stack:
        r, c = stack.pop()
        if visited[r][c]:
            continue

        visited[r][c] = True
        count += 1

        # Check neighbors (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = r + dr, c + dc
            if (0 <= new_row < len(grid) and
                    0 <= new_col < len(grid[0]) and
                    not visited[new_row][new_col] and
                    grid[new_row][new_col] == label):
                stack.append((new_row, new_col))

    return count


# Load and process the image
image_path = 'Croppedandperspectivecorrectedboards/1.jpg'
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f"Image not found at path: {image_path}")

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define grid dimensions
rows, cols = 5, 5
height, width, _ = img.shape
cube_height = height // rows
cube_width = width // cols

# Initialize grid and visited array
grid = []
visited = np.zeros((rows, cols), dtype=bool)

# Assign labels to each cube
for row in range(rows):
    grid_row = []
    for col in range(cols):
        x_start, x_end = col * cube_width, (col + 1) * cube_width
        y_start, y_end = row * cube_height, (row + 1) * cube_height

        # Ensure the slicing is within bounds
        cube = img_hsv[y_start:y_end, x_start:x_end]

        # Calculate the average color in the cube
        avg_color = cv2.mean(cube)[:3]
        label = label_color(avg_color)
        grid_row.append(label)

    # Append the filled row to the grid
    grid.append(grid_row)

# Print the grid for debugging
print("Grid of labels:")
for r in range(rows):
    print(grid[r])

# Count connected blobs (must be more than 2 connected tiles to count as a blob)
blob_counts = {}
for row in range(rows):
    for col in range(cols):
        # Check if the current position has been visited
        if not visited[row][col]:
            label = grid[row][col]  # This line could be the problem
            count = flood_fill(grid, visited, row, col, label)
            if count > 2:  # Only count as a blob if more than 2 tiles are connected
                blob_counts[label] = blob_counts.get(label, 0) + 1  # Count the blob

# Output the counts for each label
print("Blob Counts:")
for label, count in blob_counts.items():
    print(f"{label}: {count}")

# Display the processed image
cv2.imshow('Detected', img_hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()
