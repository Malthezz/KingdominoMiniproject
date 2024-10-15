'''
    WHAT NEEDS TO BE DONE:
    -   CROWNS - check
    -   NMS - check

    -   COLOURS MATCHED PERFECTLY!

    -   RAPPORT - meh

    - HIGH FIVE
'''
from pythonProject.New import load_and_process_image, tileGrid
from pythonProject.burn import countpoints, ignite
from pythonProject.target import crown, divide_into_grid, match_templates, load_templates
from pythonProject.target import point_calculator  # Import the new function

# Set the image path to the specific image you want to calculate
image_path = 'Croppedandperspectivecorrectedboards/1.jpg'

# Original functionality preserved
# Load and process the image
img, img_hsv = load_and_process_image(image_path)

# Call the original `countpoints` function
countpoints(image_path)

# Call the original `crown` function
crown_detect = crown(image_path)
print(crown_detect)

# --- New functionality starts here ---

# Step 1: Generate a grid using `tileGrid`
grid = tileGrid(img, img_hsv)

# Step 2: Load crown templates (update paths to crown template images as needed)
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
        "1 Krone Water 90.jpg", "1 Krone Water 180.jpg", "1 Krone Water 270.jpg",
        "4Krone1Sand.jpg",
        "4Krone1Sand90.jpg", "4Krone1Sand180.jpg", "4Krone1Sand270.jpg",
        "8Krone1Sand.jpg",
        "8Krone1Sand90.jpg","8Krone1Sand180.jpg","8Krone1Sand270.jpg",
        "9Krone1Sand.jpg",
        "9Krone1Sand90.jpg", "9Krone1Sand180.jpg", "9Krone1Sand270.jpg"
    ]  # Update with actual paths
templates = load_templates(template_files)

# Step 3: Call the new function to multiply connected blocks with crowns
result = point_calculator(image_path, grid, templates)

# Print the new result
print(f'Total multiplier (connected blocks * crowns): {result}')
