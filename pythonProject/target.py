import cv2
import numpy as np
from numpy.ma.core import append
import torch

def crown(image):

    img_rgb = cv2.imread(image)

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

    # Specify a threshold
    threshold = 0.6
    rectangle_coords = []

    # Store width and height of template in w and h
    for template in templates:
        w, h = template.shape[::-1]

        #perform template matching
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        # Store the coordinates of matched area in a numpy array
        loc = np.where(res >= threshold)

    # Draw a rectangle around the matched region.
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

        # Define the rectangle points
        top_left = pt
        top_right = (pt[0] + w, pt[1])  # x increases by width, y remains the same
        bottom_left = (pt[0], pt[1] + h)  # x remains the same, y increases by height
        bottom_right = (pt[0] + w, pt[1] + h)  # x increases by width, y increases by height

        # Add rectangle coordinates to the list
        rectangle_coords.append([top_left, top_right, bottom_left, bottom_right])

    rectangle_coords_np = np.array(rectangle_coords)
    print("Rectangle Coordinates:", rectangle_coords_np)

    #define the grid dimensions

    # Show the final image with the matched area.
    cv2.imshow('Detected', img_rgb)
    cv2.waitKey(0)