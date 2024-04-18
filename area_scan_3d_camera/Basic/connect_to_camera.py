# With this sample program, you can connect to a Mech-Eye Industrial 3D Camera.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *


class ConnectToCamera(object):
    def __init__(self):
        self.camera = Camera()

    def main(self):
        print("Discovering all available cameras...")
        camera_infos = Camera.discover_cameras()

        if len(camera_infos) == 0:
            print("No cameras found.")
            return

        # Display the information of all available cameras.
        for i in range(len(camera_infos)):
            print("Camera index :", i)
            print_camera_info(camera_infos[i])

        print("Please enter the index of the camera that you want to connect: ")
        input_index = 0

        # Enter the index of the camera to be connected and check if the index is valid.
        while True:
            input_index = input()
            if input_index.isdigit() and 0 <= int(input_index) < len(camera_infos):
                input_index = int(input_index)
                break
            print(
                "Input invalid! Please enter the index of the camera that you want to connect: ")

        error_status = self.camera.connect(camera_infos[input_index])
        if not error_status.is_ok():
            show_error(error_status)
            return

        print("Connected to the camera successfully.")

        self.camera.disconnect()
        print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = ConnectToCamera()
    a.main()
