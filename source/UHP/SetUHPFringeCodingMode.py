import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class SetLaserFrameRange(object):
    def __init__(self):
        self.device = Device()

    def set_uhp_fringe_coding_mode(self):
        fringe_coding_mode = {0: "Fast", 1: "Accurate"}

        uhp_settings = self.device.get_uhp_fringe_coding_mode()
        print("Old fringe coding mode: {}.".format(fringe_coding_mode[uhp_settings]))

        Common.show_error(self.device.set_uhp_fringe_coding_mode("Accurate"))

        uhp_settings = self.device.get_uhp_fringe_coding_mode()
        print("New fringe coding mode: {}.".format(fringe_coding_mode[uhp_settings]))

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.set_uhp_fringe_coding_mode()


if __name__ == '__main__':
    a = SetLaserFrameRange()
    a.main()
