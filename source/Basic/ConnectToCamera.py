import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class ConnectToCamera(object):
    def __init__(self):
        self.device = Device()

    def connect_device_info(self):

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def connect_by_ip(self):
        status = self.device.connect_by_ip("127.0.0.1")
        if not status.ok():
            Common.show_error(status)
            quit()

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.connect_device_info()

        #self.connect_by_ip()

if __name__ == '__main__':
    a = ConnectToCamera()
    a.main()
