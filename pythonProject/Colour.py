import cv2
import numpy as np

# Open picture
input_image = cv2.imread("Croppedandperspectivecorrectedboards/12.jpg")
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



