import cv2 as cv
import numpy as np

img_rgb = cv.imread('Croppedandperspectivecorrectedboards/10.jpg')
assert img_rgb is not None, "File could not be read"
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

template = cv.imread('Crown.png', cv.IMREAD_GRAYSCALE)
assert template is not None, "File could not be read"

w,h = template.shape[ : :-1]

res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
threshold = 0.4
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv.imshow('Detected', img_rgb)
cv.waitKey(0)

