import cv2
import numpy as np

from pythonProject.Targetv2 import img_rgb

# Read the main image
images_files = [
"1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg", "11.jpg", "12.jpg", "13.jpg", "14.jpg", "15.jpg", "16.jpg", "17.jpg", "18.jpg", "19.jpg", "20.jpg", "21.jpg", "22.jpg", "23.jpg", "24.jpg", "25.jpg", "26.jpg", "27.jpg", "28.jpg", "29.jpg", "30.jpg", "31.jpg", "32.jpg", "33.jpg", "34.jpg", "35.jpg", "36.jpg", "37.jpg", "38.jpg", "39.jpg", "40.jpg", "41.jpg", "42.jpg", "43.jpg", "44.jpg", "45.jpg", "46.jpg", "47.jpg", "48.jpg", "49.jpg", "50.jpg", "51.jpg", "52.jpg", "53.jpg", "54.jpg", "55.jpg", "56.jpg", "57.jpg", "58.jpg", "59.jpg", "60.jpg", "61.jpg", "62.jpg", "63.jpg", "64.jpg", "65.jpg", "66.jpg", "67.jpg", "68.jpg", "69.jpg", "70.jpg", "71.jpg", "72.jpg", "73.jpg", "74.jpg"
]

# img_rgb = cv2.imread('Croppedandperspectivecorrectedboards/5.jpg')

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

for images_file in images_files:
    img_rgb = cv2.imread(images_file, cv2.COLOR_BGR2GRAY)
    # Read each template in grayscale and append to the list
    for template_file in template_files:
        template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
        templates.append(template)

# Convert it to grayscale
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

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