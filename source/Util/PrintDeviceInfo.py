import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class ConnectAndCaptureImage(object):
    def __init__(self):
        self.device = Device()

    def connect_device_info(self):
        device_info = self.device.get_device_info()
        Common.print_device_info(device_info)

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.connect_device_info()


if __name__ == '__main__':
    a = ConnectAndCaptureImage()
    a.main()
