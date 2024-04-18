# With this sample, you can obtain and save the depth map.

import cv2

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, confirm_capture_3d


class CaptureDepthMap(object):
    def __init__(self):
        self.camera = Camera()

    def capture_depth_map(self):
        frame3d = Frame3D()
        show_error(self.camera.capture_3d(frame3d))

        depth_map = frame3d.get_depth_map()
        depth_file = "DepthMap.tiff"
        cv2.imwrite(depth_file, depth_map.data())
        print("Capture and save the depth map: {}".format(depth_file))

    def main(self):
        if find_and_connect(self.camera):
            if not confirm_capture_3d():
                return
            self.capture_depth_map()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = CaptureDepthMap()
    a.main()
