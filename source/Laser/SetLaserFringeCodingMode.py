import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class SetLaserFringeCodingMode(object):
    def __init__(self):
        self.device = Device()

    def connect_device_info(self):
        mode_dec = {0: "Fast", 1: "Accurate"}
        laser_settings = self.device.get_laser_settings()
        print("Old fringe coding mode: {}.".format(mode_dec[laser_settings.fringe_coding_mode()]))
        Common.show_error(self.device.set_laser_settings("Accurate",
                                                         laser_settings.frame_range_start(),
                                                         laser_settings.frame_range_end(),
                                                         laser_settings.frame_partition_count(),
                                                         laser_settings.power_level()))

        laser_settings = self.device.get_laser_settings()
        print("New fringe coding mode: {}.".format(mode_dec[laser_settings.fringe_coding_mode()]))

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.connect_device_info()


if __name__ == '__main__':
    a = SetLaserFringeCodingMode()
    a.main()
