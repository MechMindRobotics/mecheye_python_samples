# With this sample, you can obtain and print the camera information, such as model, serial number, firmware version, and temperatures.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, print_camera_info, print_camera_status


class PrintCameraInfo(object):
    def __init__(self):
        self.camera = Camera()
        self.camera_info = CameraInfo()
        self.camera_status = CameraStatus()

    def print_device_info(self):
        show_error(self.camera.get_camera_info(self.camera_info))
        print_camera_info(self.camera_info)
        show_error(self.camera.get_camera_status(self.camera_status))
        print_camera_status(self.camera_status)

    def main(self):
        if find_and_connect(self.camera):
            self.print_device_info()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = PrintCameraInfo()
    a.main()
