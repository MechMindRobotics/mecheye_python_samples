# With this sample, you can save the virtual device file.
# Note: The virtual device file can be opened with Mech-Eye Viewer.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect


class SaveVirtualDevice(object):
    def __init__(self):
        self.camera = Camera()

    def main(self):
        if find_and_connect(self.camera):
            print("Start saving the virtual device file. This may take up to a few minutes.")
             # Enter the name for the virtual device file. Please ensure that the file name is encoded in UTF-8 format. 
             # You can add a path before the name to specify the path for saving the file.
            file_name = "Camera.mraw"
            success_message = "The virtual device file has been saved."
            show_error(self.camera.save_virtual_device_file(file_name), success_message)
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")

if __name__ == '__main__':
    a = SaveVirtualDevice()
    a.main()
