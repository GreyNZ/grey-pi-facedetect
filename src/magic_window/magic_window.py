import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import sys
from helpers import adj_detect_face
# %matplotlib inline

class MagicWindow:

    def __init__(self, background_image: str, display_size: tuple[int, int]):
        self.background_image = self._set_background_image(background_image)
        self.display_size = display_size
        self.current_vid_frame = None
        self.display_bkg_frame = None
        self.camera_res = None
        self.camera_fps = None
        self.background_center = None

    def _set_background_image(self, background_image: str) -> cv2.Mat:
        assert (os.path.isfile(background_image)), f'File {background_image=} does not exist'
        try:
            img = cv2.imread(background_image)
            print(f'Loaded {background_image=} {img.shape=}')
            return img
        except Exception as e:
            print(f'Failed to load image due to {e=}')

    def _set_background_center(self):
        '''Find the center pixel coordinate of the background image'''
        x, y, _ = self.background_image.shape
        half_x, half_y = x // 2, y // 2
        print(f'Background center pixel: ({half_x},{half_y})')
        self.background_center = (half_x, half_y)

    def printer(self):
        while True:
            cv2.imshow("Window To Another World!", self.background_image)
            cv2.waitKey(0)
            sys.exit()
        cv2.destroyAllWindows()

    def stream_video(self):
        try:
            cap = cv2.VideoCapture(0)
        except Exception as e:
            print(f'Failed to load camera {e=}')

        while True:
            ret, self.current_vid_frame = cap.read(0)
            if (self.camera_res is None):
                self.camera_res = np.shape(self.current_vid_frame)
                self._set_fps(cap)
            # cv2.imshow('Video camera', frame)   # Uncomment me to show the video feed

            # Process video frame to extract center pixel of face
            face_img, face_rects = self.detect_face(adj_detect_face)
            cv2.imshow('Face image', face_img)

            # Transpose center pixel onto background and slice window
            # Display window
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def _set_fps(self, cap):
        # https://learnopencv.com/how-to-find-frame-rate-or-frames-per-second-fps-in-opencv-python-cpp/
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        if int(major_ver) < 3:
            self.camera_fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
            print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(self.camera_fps))
        else:
            self.camera_fps = cap.get(cv2.CAP_PROP_FPS)
            print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(self.camera_fps))
    
    def detect_face(self, detecter):
        face_img, face_rects = detecter(self.current_vid_frame)
        return face_img, face_rects



magic_window = MagicWindow('src\magic_window\hobbiton.jpeg', (500, 500))
# magic_window.printer()
# magic_window.stream_video()
# magic_window._set_background_center()
magic_window.stream_video()
