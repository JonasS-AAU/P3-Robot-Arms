#requires raspberry pi camera to function
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2

class Camera:
    def __init__(self):
        pass

    def capture_image(self):
        camera = PiCamera()
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)      
        camera.capture(rawCapture,format='bgr')
        image = rawCapture.array
        return image

    def save_image(self,image,filename):
        cv2.imwrite(filename,image)

