# imports
import math
import cv2 as cv
import numpy as np
from numba import jit
# from numpy import ndarray
from typing import List

def overlay_two_image_v2(image: cv.Mat, overlay: cv.Mat, ignore_color=None):
    if ignore_color is None:
        ignore_color = overlay[0, 0]
    # ignore_color = np.asarray(ignore_color)

    # print("ignoring color:", ignore_color)
    # print(overlay.shape)
    # mask = (overlay == ignore_color).all(-1,keepdims=True)
    # threshed = color_thresh(overlay, ignore_color)
    # o_shape = (overlay.shape[0], overlay.shape[1])
    o_shape = overlay.shape
    # threshed = thresh(overlay[..., :4] - ignore_color, 15)
    threshed = thresh2(overlay[..., :4], ignore_color, 120)
    # print(threshed)
    threshed = np.reshape(threshed, o_shape)
    # print("threshed", threshed)
    # mask = (color_thresh(overlay, ignore_color)).all(-1,keepdims=True)
    mask = threshed
    # print(mask)

    out = np.where(mask,image,overlay.astype(image.dtype))
    return out

@jit(nopython=True)
def thresh2(m1: cv.Mat, ignore_color: np.ndarray, thresh2) -> np.ndarray:
    m1 = m1.flatten()
    out = np.zeros_like(m1)
    n = len(m1) / 4
    # n = len(m1)
    for i in range(n):
        i = i * 4
        s = True
        # if all are within thresh2 of the bg color, remove it
        for j in range(4):
            # print(abs(m1[i+j] - ignore_color[j]))
            s = s and ((m1[i+j] - ignore_color[j] if m1[i+j] > ignore_color[j] else ignore_color[j] - m1[i+j]) < thresh2)  # noqa: E501
        r = s
        out[i] = r
        out[i+1] = r
        out[i+2] = r
        out[i+3] = r

    return out

# BG_REMOVAL_THRESH = 1000
@jit(nopython=True)
def thresh(m1: cv.Mat, bg_removal_thresh = 40) -> np.ndarray:
    # d = m1[..., :4] - color
    # print("d", d)
    m1 = m1.flatten()
    # out = [[] for _ in range(m1.shape[1]) for _ in range(m1.shape[0])]
    # for i in range(m1.shape[1]):
    #     col = m1[i]
    #     for j in range(m1.shape[0]):
    #         row = col[j]
    #         diff = m1[col][row]
    #         s = 0
    #         for k in range(4):
    #             x = diff[k]
    #             s += x**2
    #         out[i][j] += [s < bg_removal_thresh] * 4
    out = np.zeros_like(m1, np.bool_)
    n = len(m1) / 4
    # n = len(m1)
    for i in range(n):
        i = i * 4
        s = 0
        for j in range(4):
            s += m1[i]**2
        r = math.sqrt(s) < bg_removal_thresh
        out[i] += r
        out[i+1] += r
        out[i+2] += r
        out[i+3] += r

    # return np.array([[[Math.sqrt(sum([x**2 for x in diff] for diff in row)) < BG_REMOVAL_THRESH] * 4 for row in diff] for diff in m1[..., :4] - color])
    return out