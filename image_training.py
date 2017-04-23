# Kodie Altvater
# Image training and classification
# April 22nd, 2017
# Designed for Human Robotics Course project, JHU

# import the necessary modules
import freenect
import socket
from socket_tcp import *
import cv2
import time
import numpy as np
from os.path import realpath, normpath


# function to get RGB image from kinect
def get_video():
    array, _ = freenect.sync_get_video()
    #array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    return array


# function to get depth image from kinect
def get_depth():
    array, _ = freenect.sync_get_depth( )
    array = array.astype(np.uint8)
    return array


# function to classify image and spit image back
def detect_image(img):
    # Set path to classifiers found in OpenCV install directory
    path = normpath(realpath(cv2.__file__) + '../../../../../share/OpenCV/haarcascades')

    # converts data to image that viewer wants
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # These are the haargrave classifiers that are needed for image detection
    face_cascade = cv2.CascadeClassifier(path + '/haarcascade_frontalface_default.xml')
    eye_cascade  = cv2.CascadeClassifier(path + '/haarcascade_eye.xml')

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # detects face location
    faces = face_cascade.detectMultiScale(img, 1.2, 5)

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

# creates socket
def setup_socket(ip,port):
    TCP_IP = ip
    TCP_PORT = port
    BUFFER_SIZE = 5  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    return s

def detect(conn):

    # function that reads data from socket and interprets it as image data
    # also closes the connection so it must be reopened in sending program accordingly
    img = read_data(conn)

    # THIS TOOK ME FOREVER TO FIGURE OUT. RESHAPE IS NOT THE SAME
    # IN MATLAB AS IT IS IN PYTHON. MEMORY IS STORED DIFFERENTLY AND
    # THUS PYTHON IS C LIKE (ROW WISE) and MATLAB IS (COLUMN WISE)
    img = np.reshape(img, (480, 640, -1), order='F').astype(np.uint8)

    # apply classifier and image detection on image
    detect_image(img)
    #print "detected image"
    time.sleep(1)


if __name__ == '__main__':
    s = setup_socket('127.0.0.1',60000)
    conn, addr = s.accept()
    i = 1;

    while 1:

        type = feature2do(conn)

        # simple API implemented for various functions
        if type == 1: # send depth data
            img = get_depth()
            send_data(conn, img)

        elif type == 2: # send color data
            img = get_video()
            send_data(conn,img)

        elif type == 3: # detect using color data
            detect(conn)

        elif type == 4: # close and exit
            conn.close()
            break
        elif type == 5:
            # write image
            img = get_video()
            array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imwrite("./images/image" + str(i) + ".jpg", array)
            time.sleep(.3)
            i = i + 1;

        # uses 480 x 640 image and applies classifier and plots
        #detect(conn)

        #data = np.array([1,2,3,4]).astype(np.uint8)
        #send_data(s, data)

        #img = get_depth()
        #send_data(conn,img)


    #from_matlab_detect(conn)
    #conn.close()
