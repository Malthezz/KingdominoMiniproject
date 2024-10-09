import numpy as np
from target import *


# Function to calculate the Intersection over Union (IoU) between two boxes
def calculate_iou(box1, box2):
    # Use top-left and bottom-right coordinates to calculate the IoU
    x1 = max(box1[0][0], box2[0][0])
    y1 = max(box1[0][1], box2[0][1])
    x2 = min(box1[1][0], box2[1][0])
    y2 = min(box1[1][1], box2[1][1])

    # Area of overlap
    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    # Areas of both the boxes
    area_box1 = (box1[1][0] - box1[0][0]) * (box1[1][1] - box1[0][1])
    area_box2 = (box2[1][0] - box2[0][0]) * (box2[1][1] - box2[0][1])

    # Union area
    union = area_box1 + area_box2 - intersection

    # IoU score
    return intersection / union


# Non-Maximum Suppression (NMS) function
def nms(boxes, threshold):
    # Sort the boxes by their confidence scores in descending order
    boxes = sorted(boxes, key=lambda x: x[4], reverse=True)

    nms_boxes = []

    while len(boxes) > 0:
        # Select the box with the highest score
        chosen_box = boxes.pop(0)
        nms_boxes.append(chosen_box)

        boxes = [
            box for box in boxes
            if calculate_iou((chosen_box[0], chosen_box[3]), (box[0], box[3])) < threshold
        ]

    return nms_boxes


# Example bounding boxes (top-left, top-right, bottom-left, bottom-right, score)
boxes = [
    top_left, top_right, bottom_left, bottom_right, score
]

# Apply NMS
threshold = 0.5
filtered_boxes = nms(boxes, threshold)

# Output the filtered boxes
print(filtered_boxes)
