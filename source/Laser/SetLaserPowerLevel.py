# With this sample program, you can set the output power of the laser projector in percentage of max
# power. This affects the intensity of the laser light.

import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class SetLaserPowerLevel(object):
    def __init__(self):
        self.device = Device()

    def set_laser_power_level(self):
        mode_dec = {0: "Fast", 1: "Accurate"}
        laser_settings = self.device.get_laser_settings()
        print("Old power level: {}".format(laser_settings.power_level()))
        Common.show_error(self.device.set_laser_settings(mode_dec[laser_settings.fringe_coding_mode()],
                                                  laser_settings.frame_range_start(),
                                                  laser_settings.frame_range_end(),
                                                  laser_settings.frame_partition_count(),
                                                  80))

        laser_settings = self.device.get_laser_settings()
        print("New power level: {}".format(laser_settings.power_level()))

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.set_laser_power_level()


if __name__ == '__main__':
    a = SetLaserPowerLevel()
    a.main()
