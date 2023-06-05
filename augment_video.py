import cv2 as cv
from collections import deque
from augment_frame import run_augment_frame

def run_augment_video(source):
    source_feed = cv.VideoCapture(source)
    source_success, source_frame = source_feed.read()

    source_buffer = deque(maxlen=128)
    source_buffer.appendleft(source_frame)

    webcam_feed = cv.VideoCapture(0, cv.CAP_DSHOW)
    webcam_feed.set(cv.CAP_PROP_FRAME_WIDTH, 960)
    webcam_feed.set(cv.CAP_PROP_FRAME_HEIGHT, 540)
    
    while len(source_buffer) > 0:
        _, webcam_frame = webcam_feed.read()
        augmented_frame = run_augment_frame(source_frame, webcam_frame)

        if augmented_frame is not None:
            result_frame = augmented_frame
            source_frame = source_buffer.popleft()
        else:
            result_frame = webcam_frame

        if len(source_buffer) < source_buffer.maxlen:
            source_success, next_source_frame = source_feed.read()
            if source_success:
                source_buffer.append(next_source_frame)

        cv.imshow("Feed", result_frame)
        key = cv.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    webcam_feed.release()
    cv.destroyAllWindows()
