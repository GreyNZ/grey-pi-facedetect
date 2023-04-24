import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import sys
from helpers import adj_detect_face, slicer
# %matplotlib inline

class MagicWindow:

    def __init__(self, background_image: str, display_size: tuple[int, int], detecter=adj_detect_face):
        self.background_image = self._set_background_image(background_image)
        self.display_size = display_size
        self.current_vid_frame = None
        self.display_bkg_frame = None
        self.camera_res = None
        self.camera_fps = None
        self.background_center = None
        self.detecter = detecter


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
            face_img, centroid = self.detect_face(self.detecter)
            cv2.imshow('Face image', face_img)

            # Transpose center pixel onto background and slice window
            centroid_x, centroid_y = centroid
            vid_frame_height, vid_frame_width, _ = self.current_vid_frame.shape
            norm_centroid_x = centroid_x / vid_frame_width
            norm_centroid_y = centroid_y / vid_frame_height

            # Display window
            inverted_centroid_y = norm_centroid_x
            inverted_centroid_x = 1 - norm_centroid_y

            x_scaler = self.background_image.shape[0] - self.display_size[0]
            y_scaler = self.background_image.shape[1] - self.display_size[1]
            x1 = int(0 + x_scaler * inverted_centroid_x)
            x2 = int(x1 + self.display_size[0])
            y1 = int(0 + y_scaler * inverted_centroid_y)
            y2 = int(y1 + self.display_size[1])
            print((x1, x2, y1, y2))
            
            img_slice = slicer(self.background_image, (x1, x2, y1, y2))
            cv2.imshow('Magic window', img_slice)

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
        face_img, centroid = detecter(self.current_vid_frame)
        return face_img, centroid



magic_window = MagicWindow('src\magic_window\hobbiton.jpeg', (300, 300))
# magic_window.printer()
# magic_window.stream_video()
# magic_window._set_background_center()
magic_window.stream_video()
