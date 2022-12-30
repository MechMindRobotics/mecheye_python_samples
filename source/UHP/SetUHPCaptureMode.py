import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class SetLaserFrameRange(object):
    def __init__(self):
        self.device = Device()

    def connect_device_info(self):
        capture_mode_dic = {0: "Camera1", 1: "Camera2", 2: "Merge"}

        uhp_settings = self.device.get_uhp_capture_mode()
        print("Old capture mode: {}.".format(capture_mode_dic[uhp_settings]))

        Common.show_error(self.device.set_uhp_capture_mode("Camera1"))

        uhp_settings = self.device.get_uhp_capture_mode()
        print("New capture mode: {}.".format(capture_mode_dic[uhp_settings]))

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.connect_device_info()


if __name__ == '__main__':
    a = SetLaserFrameRange()
    a.main()
