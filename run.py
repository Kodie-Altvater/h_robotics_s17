#import the necessary modules
import freenect
import cv2
import time
import numpy as np
import cv
 
#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array
    
def pretty_depth(depth):
    """Converts depth into a 'nicer' format for display
    This is abstracted to allow for experimentation with normalization
    Args:
        depth: A numpy array with 2 bytes per pixel
    Returns:
        A numpy array that has been processed whos datatype is unspecified
    """
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth


def pretty_depth_cv(depth):
    """Converts depth into a 'nicer' format for display
    This is abstracted to allow for experimentation with normalization
    Args:
        depth: A numpy array with 2 bytes per pixel
    Returns:
        An opencv image who's datatype is unspecified
    """
    depth = pretty_depth(depth)
    image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 1)
    cv.SetData(image, depth.tostring(),
               depth.dtype.itemsize * depth.shape[1])
    return image


def video_cv(video):
    """Converts video into a BGR format for opencv
    This is abstracted out to allow for experimentation
    Args:
        video: A numpy array with 1 byte per pixel, 3 channels RGB
    Returns:
        An opencv image who's datatype is 1 byte, 3 channel BGR
    """
    video = video[:, :, ::-1]  # RGB -> BGR
    image = cv.CreateImageHeader((video.shape[1], video.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 3)
    cv.SetData(image, video.tostring(),
               video.dtype.itemsize * 3 * video.shape[1])
    return image
       
 
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        frame = get_video()
        
        #get a frame from depth sensor
        depth = get_depth()
        
        #display RGB image
        cv2.imshow('RGB image',frame)
        #display depth image
        cv2.imshow('Depth image',depth)
        
        time.sleep(.1)
 
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()