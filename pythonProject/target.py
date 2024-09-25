import cv2
import numpy as np

# Read the main image
img_rgb = cv2.imread('Croppedandperspectivecorrectedboards/4.jpg')

# Convert it to grayscale
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

# Read the template
template = cv2.imread('Crown.png', cv2.IMREAD_GRAYSCALE)

# best current results (30,30) and (3,3) and thresh = 7
template = cv2.resize(template, (30,30))
template = cv2.GaussianBlur(template, (3, 3), 10,10,10, cv2.BORDER_DEFAULT)

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