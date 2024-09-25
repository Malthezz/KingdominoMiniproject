import cv2
import numpy as np

# Open picture
input_image = cv2.imread("Croppedandperspectivecorrectedboards/12.jpg")

hsv_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

# Here we make the colour channels; blue, green and red (RGB).
blue = input_image[:, :, 0]
green = input_image[:, :, 1]
red = input_image[:, :, 2]

blueThreshold = 50
greenThreshold = 150
redThreshold = 150

blue[blue < blueThreshold] = 0
green[green < greenThreshold] = 0
red[red < redThreshold] = 0

# Merge the channels back into a single image
new_image = cv2.merge([blue, green, red])

hsv_imageNEW = cv2.cvtColor(new_image, cv2.COLOR_BGR2HSV)

# Show the processed images
# cv2.imshow('Blue', blue)
# cv2.imshow('Green', green)
# v2.imshow('Red', red)
cv2.imshow('New Image', new_image)
cv2.imshow('NewHSV', hsv_imageNEW)

# Wait for key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()

#split the image into its three channels
(b_channel, g_channel, r_channel) = cv2.split(input_image)

# red = input_image[:,:,2]
# green = input_image[:,:,1]
# blue = input_image[:,:,0]

blank = np.zeros(input_image.shape[:2], dtype="uint8")
blueimg = cv2.merge([b_channel, blank, blank])
greenimg = cv2.merge([blank, g_channel, blank])
redimg = cv2.merge([blank, blank, r_channel])

# Display the picture
cv2.imshow("Our window", input_image)
cv2.imshow("Red windowl", redimg)
cv2.imshow("green window", greenimg)
cv2.imshow("blue window", blueimg)
cv2.waitKey(0)



