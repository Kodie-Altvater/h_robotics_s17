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
    #print array
    print array.shape[0]
    print array.shape[1]
    print array.shape[2]

    array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    #print array.__len__()
    return array


# function to get depth image from kinect
def get_depth():
    array, _ = freenect.sync_get_depth( )
    print array
    print array.__len__( )
    array = array.astype(np.uint8)
    return array


# function to classify image and spit image back
def get_image(img_data):
    # Set path to classifiers found in OpenCV install directory
    path = normpath(realpath(cv2.__file__) + '../../../../../share/OpenCV/haarcascades')

    # get a frame from RGB camera
    #img = get_video()
    img = img_data

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

    # Setup Socket parameters
    TCP_IP = '127.0.0.1'
    TCP_PORT = 51031
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    # try to open socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    # listen/grab image data from matlab
    #data = tcp_data(s)

    # close the socket
    #s.close()
    while 1:
        img_data = tcp_data(s)
        tmpdata = []
        for i in img_data:
            tmpdata.append(ord(i))
        #print "received data:", tmpdata

        array = np.array(tmpdata)
        array = np.reshape(array, (400,400,3))
        #random_image = np.random.random([500, 500])
        #print random_image

        #linear1 = np.linspace(0, 255, 7500).reshape((50,50,3)).astype(np.uint8)
        #linear1 = cv2.cvtColor(linear1, cv2.COLOR_RGB2BGR)

        #print linear1
        #print linear1.shape[0]
        #print linear1.shape[1]
        #print linear1.shape[2]

        time.sleep(1)
        #array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        array = array.astype(np.uint8)
        #print array
        get_image(array)

    #while 1:
    #    print 'hey'
    #    time.sleep(5)