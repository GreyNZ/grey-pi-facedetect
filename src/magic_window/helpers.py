import cv2
import os

FILE_NAME = 'src/magic_window/haarcascade_frontalface_default.xml'
assert (os.path.isfile(FILE_NAME))
FACE_CASCADE = cv2.CascadeClassifier(FILE_NAME)

def return_largest(a,b):
    """Compare a,b and reutrn largest"""
    
    def calculate_delta(x):
        """calculate the size of face"""
        _,_,w,h = x
        return w * h
    
    if calculate_delta(a) > calculate_delta(b):
        return a
    else:
        return b
    
def adj_detect_face(img):
    """Dectect faces in an image with no overlaps
    Arg img: an image
    
    Result: 
    face_img = image with bounding boxes
    face-rects = array of arrays, each array is corners of face bounding box
    """
    face_img = img.copy()
    face_rects = FACE_CASCADE.detectMultiScale(face_img,scaleFactor=1.2, minNeighbors=5) 
    for (x,y,w,h) in face_rects: 
        cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 10) 
    return face_img, face_rects