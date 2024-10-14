'''
    WHAT NEEDS TO BE DONE:
    -   CROWNS
    -   NMS

    -   COLOURS MATCHED PERFECTLY!

    -   RAPPORT

    - HIGH FIVE
'''
from pythonProject.New import load_and_process_image
from pythonProject.burn import countpoints
from pythonProject.target import crown

# Usage example
image_path = 'Croppedandperspectivecorrectedboards/4.jpg'

# Load and process the image
img, img_hsv = load_and_process_image(image_path)

countpoints(image_path)

crown(image_path)