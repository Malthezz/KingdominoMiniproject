import cv2
import numpy as np

# Read the main image

img_rgb = cv2.imread('Croppedandperspectivecorrectedboards/5.jpg')

# Convert it to grayscale
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

# List of template file names
template_files = [
    "1_Krone1_Desert.jpg",
    "1_Krone1_Grass.jpg",
    "1_Krone2_Desert.jpg",
    "1_Krone2_Grass.jpg",
    "1_Krone3_Desert.jpg",
    "1_Krone3_Grass.jpg",
    "1_Krone_Skov.jpg",
    "1_Krone_Water.jpg"
]

# List to store the grayscale templates
templates = []

# Read each template in grayscale and append to the list
for template_file in template_files:
    template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
    templates.append(template)

# best current results (30,30) and (3,3) and thresh = 7!!
# template = cv2.resize(template, (30,30))
# template = cv2.GaussianBlur(template, (3, 3), 10,10,10, cv2.BORDER_DEFAULT)

cv2.imshow('crown_blur', template)

# Store width and height of template in w and h
w, h = template.shape[::-1]

# Perform match operations.
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

# Specify a threshold
threshold = 0.7

# Store the coordinates of matched area in a numpy array
loc = np.where(res >= threshold)

# Draw a rectangle around the matched region.
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

# Show the final image with the matched area.
cv2.imshow('Detected', img_rgb)
cv2.waitKey(0)