# With this sample program, you can obtain and save the 2D image in OpenCV format from a camera.

import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
import cv2
from source import Common


class CaptureColorMap(object):
    def __init__(self):
        self.device = Device()

    def capture_color_map(self):
        color_map = self.device.capture_color()
        color_file = "ColorMap.png"
        cv2.imencode('.png', color_map.data())[1].tofile(color_file)
        print("Capture and save color image : {}".format(color_file))

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.capture_color_map()


if __name__ == '__main__':
    a = CaptureColorMap()
    a.main()
