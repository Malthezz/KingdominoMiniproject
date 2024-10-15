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

# Set the image path to the specific image you want to calculate
image_path = 'Croppedandperspectivecorrectedboards/1.jpg'

# Original functionality preserved
# Load and process the image
img, img_hsv = load_and_process_image(image_path)

# Call the original `countpoints` function
countpoints(image_path)

# Call the original `crown` function
crown(image_path)