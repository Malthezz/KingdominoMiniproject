import cv2
import numpy as np
from numpy.ma.core import append

# Read the main image
images_files = [
"1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg", "11.jpg", "12.jpg", "13.jpg", "14.jpg", "15.jpg", "16.jpg", "17.jpg", "18.jpg", "19.jpg", "20.jpg", "21.jpg", "22.jpg", "23.jpg", "24.jpg", "25.jpg", "26.jpg", "27.jpg", "28.jpg", "29.jpg", "30.jpg", "31.jpg", "32.jpg", "33.jpg", "34.jpg", "35.jpg", "36.jpg", "37.jpg", "38.jpg", "39.jpg", "40.jpg", "41.jpg", "42.jpg", "43.jpg", "44.jpg", "45.jpg", "46.jpg", "47.jpg", "48.jpg", "49.jpg", "50.jpg", "51.jpg", "52.jpg", "53.jpg", "54.jpg", "55.jpg", "56.jpg", "57.jpg", "58.jpg", "59.jpg", "60.jpg", "61.jpg", "62.jpg", "63.jpg", "64.jpg", "65.jpg", "66.jpg", "67.jpg", "68.jpg", "69.jpg", "70.jpg", "71.jpg", "72.jpg", "73.jpg", "74.jpg"
]

img_rgb = cv2.imread('Croppedandperspectivecorrectedboards/1.jpg')

# Convert it to grayscale
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

# List of template file names
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
    "1 Krone Water 90.jpg", "1 Krone Water 180.jpg", "1 Krone Water 270.jpg"
]

# List to store the grayscale templates
templates = []

for template_file in template_files:
    template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
    template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
    templates.append(template)

# best current results (30,30) and (3,3) and thresh = 7!!
# template = cv2.resize(template, (30,30))
# template = cv2.GaussianBlur(template, (3, 3), 10,10,10, cv2.BORDER_DEFAULT)

# cv2.imshow('crown_blur', template)

# Store width and height of template in w and h
w, h = template.shape[::-1]

# Perform match operations.
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

# Specify a threshold
threshold = 0.6

# Store the coordinates of matched area in a numpy array
loc = np.where(res >= threshold)

rectangle_coords = []

# Draw a rectangle around the matched region.
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

    # Define the rectangle points
    top_left = pt
    top_right = pt
    bottom_left = (pt[0], pt[1] + h)
    bottom_right = (pt[0] + w, pt[1] + h)

    rectangle_coords.append([top_left[0], top_right[1], bottom_left[0], bottom_right[1]])

rectangle_coords_np = np.array(rectangle_coords)

print("Rectangle Coordinates:", rectangle_coords_np)


# Show the final image with the matched area.
cv2.imshow('Detected', img_rgb)
cv2.waitKey(0)