import cv2
import numpy as np
from fontTools.subset import intersect
from networkx import intersection
from numpy.ma.core import append
import torch
from target import *

for pt in pt():
    top_left = pt
    top_right = (pt[0] + w, pt[1])  # x increases by width, y remains the same
    bottom_left = (pt[0], pt[1] + h)  # x remains the same, y increases by height
    bottom_right = (pt[0] + w, pt[1] + h)  # x increases by width, y increases by height

    # Add rectangle coordinates to the list
    rectangle_coords.append([top_left, top_right, bottom_left, bottom_right])

def nms(
        predictions,
        iou_threshold,
        prob_threshold,
        box_format="corners"
):
    bboxes = rectangle_coords_np
    assert type(bboxes) == list

    bboxes = [box for box in bboxes if box[1] > prob_threshold]
    bboxes = sorted(bboxes, key=lambda x: x[1], reverse=True)
    bboxes_after_nms = []

    while bboxes:
        chosen_box = bboxes.pop(0)

        bboxes = [
            box
            # are they of different classes?
            for box in boxes
            # if they are of the same class:
            if box[0] != chosen_box[0]
            # we compare
            or intersection_over_union(
                torch.tensor(chosen_box[2:]),
                torch.tensor(chosen_box[:2]),
                box_format = box_format,
            )
            < iou_threshold
        ]

        bboxes_after_nms.append(chosen_box)

    return bboxes_after_nms