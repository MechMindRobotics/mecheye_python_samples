import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
import cv2
from MechEye import Device
from source import Common


class CaptureDepthMap(object):
    def __init__(self):
        self.device = Device()

    def connect_device_info(self):
        depth_map = self.device.capture_depth()
        depth_file = "DepthMap.tiff"
        cv2.imencode('.tiff', depth_map.data())[1].tofile(depth_file)
        print("Capture and save depth image : {}".format(depth_file))

        self.device.disconnect()
        print("Disconnect from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.connect_device_info()


if __name__ == '__main__':
    a = CaptureDepthMap()
    a.main()
