# With this sample, you can obtain and print the camera intrinsic parameters.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, print_camera_intrinsics


class GetCameraIntrinsics(object):
    def __init__(self):
        self.camera = Camera()
        self.intrinsics = CameraIntrinsics()

    def get_device_intrinsic(self):
        show_error(self.camera.get_camera_intrinsics(self.intrinsics))
        print_camera_intrinsics(self.intrinsics)

    def main(self):
        if find_and_connect(self.camera):
            self.get_device_intrinsic()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = GetCameraIntrinsics()
    a.main()
