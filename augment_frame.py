import cv2 as cv
import numpy as np
from remove_bg import overlay_two_image_v2

CORNER_IDS = (1, 3, 2, 0)
CACHED_REF_PTS = None

def get_ref_pts(corners, ids):
    ids = np.array([]) if len(corners) != 4 else ids.flatten()
    ref_pts = []
	
    for i in CORNER_IDS:
        j = np.squeeze(np.where(ids == i))
        if j.size == 0:
            continue

        corner = np.squeeze(corners[j])
        ref_pts.append(corner)

    if len(ref_pts) != 4:
        if CACHED_REF_PTS is not None:
            ref_pts = CACHED_REF_PTS
        else:
            return None
        
    return ref_pts

def get_frame_corners(source_frame, webcam_frame):
    global CACHED_REF_PTS

    aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
    aruco_params =  cv.aruco.DetectorParameters()
    corners, ids, _ = cv.aruco.detectMarkers(webcam_frame, aruco_dict, parameters=aruco_params)
        
    ref_pts = get_ref_pts(corners, ids)
    if ref_pts is None:
        return None
    CACHED_REF_PTS = ref_pts

    top_left, top_right, bottom_right, bottom_left = ref_pts
    webcam_corners = np.array([top_left[0], top_right[1], bottom_right[2], bottom_left[3]])

    source_height, source_width = source_frame.shape[:2]
    source_corners = np.array([[0, 0], [source_width, 0], [source_width, source_height], [0, source_height]])

    return source_corners, webcam_corners

def draw_over_corners(source_frame, webcam_frame, source_corners, webcam_corners):
    homography, _ = cv.findHomography(source_corners, webcam_corners)

    webcam_height, webcam_width = webcam_frame.shape[:2]
    warped_frame = cv.warpPerspective(source_frame, homography, (webcam_width, webcam_height))

    # mask = np.zeros((webcam_height, webcam_width), dtype=np.uint8)
    # cv.fillConvexPoly(mask, np.int32([webcam_corners]), (255, 255, 255), cv.LINE_AA)

    # mask_scaled = mask.copy() / 255.0
    # mask_scaled = np.dstack([mask_scaled] * 3)

    # warped_multiplied = cv.multiply(warped_frame.astype(float), mask_scaled)
    # image_multiplied = cv.multiply(webcam_frame.astype(float), 1.0 - mask_scaled)
    # augmented_frame = cv.add(warped_multiplied, image_multiplied)
    # augmented_frame = augmented_frame.astype(np.uint8)
    augmented_frame = overlay_two_image_v2(webcam_frame, warped_frame)

    return augmented_frame

def run_augment_frame(source_frame, webcam_frame):
    try:
        source_corners, webcam_corners = get_frame_corners(source_frame, webcam_frame)
        return draw_over_corners(source_frame, webcam_frame, source_corners, webcam_corners)
    except TypeError:
        return None
