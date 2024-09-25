import cv2

# Open picture
input_image = cv2.imread("Croppedandperspectivecorrectedboards/12.jpg")
red = input_image[:,:,2]
green = input_image[:,:,1]
blue = input_image[:,:,0]

# Display the picture
cv2.imshow("Our window", input_image)
cv2.imshow("Red windowl", red)
cv2.imshow("green window", green)
cv2.imshow("blue window", blue)
cv2.waitKey(0)

redred = cv2. split(input_image)
cv2.imshow("Our window", input_image)