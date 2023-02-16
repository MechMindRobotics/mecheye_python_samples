import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class ConnectToCamera(object):
    def __init__(self):
        self.device = Device()

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.device.disconnect()
            print("Disconnected from the Mech-Eye device successfully.")

if __name__ == '__main__':
    a = ConnectToCamera()
    a.main()
