# import the necessary modules
import freenect
from socket_tcp import *
import cv2
import time
import numpy as np
from os.path import realpath, normpath


# function to get RGB image from kinect
def get_video():
    array, _ = freenect.sync_get_video( )
    array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    return array


# function to get depth image from kinect
def get_depth():
    array, _ = freenect.sync_get_depth( )
    array = array.astype(np.uint8)
    return array


# function to classify image and spit image back
def get_image(img_data):
    # Set path to classifiers found in OpenCV install directory
    path = normpath(realpath(cv2.__file__) + '../../../../../share/OpenCV/haarcascades')

    # get a frame from RGB camera
    img = get_video()

    # get a frame from depth sensor
    #depth = get_depth()

    # These are the haargrave classifiers that are needed for image detection
    face_cascade = cv2.CascadeClassifier(path + '/haarcascade_frontalface_default.xml')
    eye_cascade  = cv2.CascadeClassifier(path + '/haarcascade_eye.xml')

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # detects face location
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray  = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    # continously outputs image to screen for viewing
    cv2.imshow('img',img)
    k = cv2.waitKey(5) & 0xFF

    time.sleep(.1)
    cv2.destroyAllWindows()

    return img


if __name__ == '__main__':

    while 1:
        data = tcp_data('127.0.0.1',50000)
        print data
        #get_image()