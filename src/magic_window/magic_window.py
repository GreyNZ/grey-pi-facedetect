import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import sys
# %matplotlib inline

# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class MagicWindow:

    def __init__(self, background_image: str, display_size: tuple[int, int]):
        self.background_image = self._set_background_image(background_image)
        self.display_size = display_size
        self.current_vid_frame = None
        self.display_bkg_frame = None

    def _set_background_image(self, background_image: str) -> cv2.Mat:
        assert (os.path.isfile(background_image)), f'File {background_image=} does not exist'
        try:
            img = cv2.imread(background_image)
            print(f'Loaded {background_image=} {img.shape=}')
            return img
        except Exception as e:
            print(f'Failed to load image due to {e=}')
            

    def get_background_center(self) -> tuple[int, int]:
        '''Find the center pixel coordinate of the background image'''

    def printer(self):
        while True:
            cv2.imshow("Window To Another World!", self.background_image)
            cv2.waitKey(0)
            sys.exit()

        cv2.destroyAllWindows()
    


magic_window = MagicWindow('src\magic_window\hobbiton.jpeg', (500, 500))
magic_window.printer()

