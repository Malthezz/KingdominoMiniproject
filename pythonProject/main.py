'''
    WHAT NEEDS TO BE DONE:
    -   CROWNS - check
    -   NMS - check

    -   COLOURS MATCHED PERFECTLY!

    -   RAPPORT - meh

    - HIGH FIVE
'''
from pythonProject.New import load_and_process_image
from pythonProject.burn import countpoints
from pythonProject.target import crown

# Set the image path to the specific image you want to calculate :))
image_path = 'Croppedandperspectivecorrectedboards/6.jpg'

# Load and process the image
img, img_hsv = load_and_process_image(image_path)

countpoints(image_path)

crown(image_path)

