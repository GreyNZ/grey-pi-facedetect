import cv2
import os
import numpy as np
#from numba import jit

def where_am_i():
    print(os.getcwd())
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        print(f)

#where_am_i()

FILE_NAME = 'haarcascade_frontalface_default.xml'
assert (os.path.isfile(FILE_NAME))
FACE_CASCADE = cv2.CascadeClassifier(FILE_NAME)


#@jit
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
    
#@jit
def get_largest_face(face_img, face_rects):
    x, y, _ = face_img.shape
    centroid = (x // 2, y // 2)   # Set default centroid to the center of screen
    largest = [0,0,0,0]
    for x, y, w, h in face_rects:
        largest = return_largest(largest, [x, y, w, h])
    x, y, w, h = largest
    if (len(face_rects)):   # If there were face_rects present, update the centroid
        centroid = int(x+w/2), int(y+h/2)
    return centroid
    
#@jit
def adj_detect_face(img):
    """Dectect faces in an image with no overlaps
    Arg img: an image
    
    Result: 
    face_img = image with bounding boxes
    face-rects = array of arrays, each array is corners of face bounding box
    """
    face_detected = False
    face_img = img.copy()
    face_rects = FACE_CASCADE.detectMultiScale(face_img,scaleFactor=1.2, minNeighbors=5) 
    for (x,y,w,h) in face_rects: 
        cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 10)
    face_centroid = get_largest_face(face_img, face_rects)
    if (len(face_rects)):
        face_detected = True
    return face_img, face_centroid, face_detected
    
#@jit 
def slicer(img, coords):
    x1,x2,y1,y2 = coords
    img_shape = np.shape(img)
    
    # Check we are not trying to slice outside of ary
    if x1 < 0 or y1 < 0:
        raise Exception(f"Sorry, cannot slice below 0, out of array range, {x1=}, {y1=}") 
        
    if x2 > img_shape[0] or y2 > img_shape[1]:
        raise Exception(f"Sorry, cannot slice out of range, {img_shape=}, {x2=}, {y2=}") 
    
    #swap x/y around as np/cv is weird with images
    img_slice = img[x1:x2, y1:y2]
    # img_slice = img[y1:y2, x1:x2]
    
    return img_slice