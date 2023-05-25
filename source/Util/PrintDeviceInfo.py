# With this sample program, you can get and print a camera's information such as model, serial number
# and firmware version.

import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class PrintDeviceInfo(object):
    def __init__(self):
        self.device = Device()

    def print_device_info(self):
        device_info = self.device.get_device_info()
        Common.print_device_info(device_info)
        device_temperature = self.device.get_device_temperature()
        Common.print_device_temperature(device_temperature)

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.print_device_info()


if __name__ == '__main__':
    a = PrintDeviceInfo()
    a.main()
