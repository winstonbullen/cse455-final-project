import cv2 as cv
import numpy as np
from numba import jit

def overlay_two_image_v2(image: cv.Mat, overlay: cv.Mat, ignore_color=None):
    if ignore_color is None:
        ignore_color = overlay[0, 0]

    o_shape = overlay.shape
    threshed = thresh2(overlay[..., :3], ignore_color, 115)
    threshed = np.reshape(threshed, o_shape)
    mask = threshed

    out = np.where(mask,image,overlay.astype(image.dtype))

    return out

@jit(nopython=True)
def thresh2(m1: cv.Mat, ignore_color: np.ndarray, thresh2) -> np.ndarray:
    m1 = m1.flatten()
    out = np.zeros_like(m1)
    n = len(m1) / 3

    for i in range(n):
        i = i * 3
        s = True

        for j in range(3):
            s = s and ((m1[i+j] - ignore_color[j] if m1[i+j] > ignore_color[j] else ignore_color[j] - m1[i+j]) < thresh2)  # noqa: E501
        r = s
        out[i] = r
        out[i+1] = r
        out[i+2] = r

    return out
