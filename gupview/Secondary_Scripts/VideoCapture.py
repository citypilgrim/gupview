#########
#Imports#
#########

# Python Basics
import time
from threading import Lock

# Pymba SDK
from pymba import *

# Image process
import numpy as np

# Parameters
import Parameters as para


###########
#Operation#
###########

class VideoCapture:

    def __init__(self):

        # Stored image
        self.img = None

        # Open the video source
        self.vimba = Vimba()
        self.vimba.startup()
        system = self.vimba.getSystem()
        system.runFeatureCommand("GeVDiscoveryAllOnce")
        time.sleep(0.2)

        camera_ids = self.vimba.getCameraIds()

        for cam_id in camera_ids:
            print("Camera found: ", cam_id)

        self.c0 = self.vimba.getCamera(camera_ids[para.camera_index])
        print('working with cam '+camera_ids[para.camera_index])
        self.c0.openCamera()

        try:
            # gigE camera
            print(self.c0.GevSCPSPacketSize)
            print(self.c0.StreamBytesPerSecond)
            self.c0.StreamBytesPerSecond = 100000000
        except:
            # not a gigE camera
            pass

        # set pixel format
        self.c0.PixelFormat = "Mono8"
        # self.c0.ExposureTime = self.ExposureTime
        # print('ExposureTime', self.c0.ExposureTime)

        self.frame = self.c0.getFrame()
        self.frame.announceFrame()

        self.c0.startCapture()

        self.lock = Lock()

    def operate_camera(self):

            while 1:
                try:
                    self.frame.queueFrameCapture()
                    success = True
                except:
                    success = False

                self.c0.runFeatureCommand("AcquisitionStart")
                self.c0.runFeatureCommand("AcquisitionStop")
                self.frame.waitFrameCapture(1000)
                frame_data = self.frame.getBufferByteData()

                if success:
                    img = np.ndarray(buffer=frame_data,
                                     dtype=np.uint8,
                                     shape=(self.frame.height, self.frame.width, 1))

                    # img = cv2.applyColorMap(img, cv2.COLORMAP_JET)

                    img = np.squeeze(img)

                    self.lock.acquire()
                    self.img = img
                    self.lock.release()

                    break

    def get_frame(self):
        while type(self.img) == type(None): # waiting for the first frame to load
            time.sleep(1)
        else:
            return self.img
