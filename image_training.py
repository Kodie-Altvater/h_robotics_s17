# import the necessary modules
import freenect
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


if __name__ == "__main__":
    while 1:

        # Set path to classifiers found in OpenCV install directory
        path = normpath(realpath(cv2.__file__) + '../../../../../share/OpenCV/haarcascades')

        img = cv2.imread('/Users/Schmoder/Desktop/human1.jpg')
        #cv2.imshow('img', img)

        # get a frame from RGB camera
        #img = get_video()

        # get a frame from depth sensor
        #depth = get_depth()

        face_cascade = cv2.CascadeClassifier(path + '/haarcascade_frontalface_default.xml')
        eye_cascade  = cv2.CascadeClassifier(path + '/haarcascade_eye.xml')

        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #cv2.imshow('img', gray)

        faces = face_cascade.detectMultiScale(gray, 1.2, 5)


        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray  = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        cv2.imshow('img',img)
        print 'hey'


        # display RGB image
        #cv2.imshow('RGB image', video)

        # display depth image
        #cv2.imshow('Depth image', depth)

        time.sleep(.1)

        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows( )