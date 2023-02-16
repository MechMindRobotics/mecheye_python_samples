import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class SetLaserFrameRange(object):
    def __init__(self):
        self.device = Device()

    def set_laser_frame_range(self):
        mode_dic = {0: "Fast", 1: "Accurate"}
        laser_settings = self.device.get_laser_settings()
        print("Old frame range: {} to {}.".format(
            laser_settings.frame_range_start(), laser_settings.frame_range_end()))
        Common.show_error(self.device.set_laser_settings(mode_dic[laser_settings.fringe_coding_mode()],
                          33,
                          90,
                          laser_settings.frame_partition_count(),
                          laser_settings.power_level()))

        laser_settings = self.device.get_laser_settings()
        print("New frame range: {0} to {1}.".format(laser_settings.frame_range_start(),
                                                    laser_settings.frame_range_end()))

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.set_laser_frame_range()


if __name__ == '__main__':
    a = SetLaserFrameRange()
    a.main()
