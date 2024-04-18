# With this sample, you can set the parameters specific to laser cameras (the DEEP and LSR series).

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect


class SetParametersOfLaserCameras(object):
    def __init__(self):
        self.camera = Camera()

    def set_laser_partition_count(self):
        current_user_set = self.camera.current_user_set()
        error, laser_partition_count = current_user_set.get_int_value(
            LaserFramePartitionCount.name)
        show_error(error)
        print("Old frame partition count: {}".format(laser_partition_count))

        # Set the laser scan partition count. If the set value is greater than 1, the scan of the entire FOV
        # will be partitioned into multiple parts. It is recommended to use multiple parts for
        # extremely dark objects.
        error = current_user_set.set_int_value(
            LaserFramePartitionCount.name, 2)
        show_error(error)
        error, laser_partition_count = current_user_set.get_int_value(
            LaserFramePartitionCount.name)
        show_error(error)
        print("New frame partition count: {}".format(laser_partition_count))

    def set_laser_frame_range(self):
        current_user_set = self.camera.current_user_set()
        error, laser_frame_range = current_user_set.get_range_value(
            LaserFrameRange.name)
        show_error(error)
        print("Old frame range: {} to {}.".format(
            laser_frame_range.min, laser_frame_range.max))

        # Set the laser scan range. The entire projector FOV is from 0 to 100.
        laser_frame_range.min = 20
        laser_frame_range.max = 80
        error = current_user_set.set_range_value(
            LaserFrameRange.name, laser_frame_range)
        show_error(error)
        error, laser_frame_range = current_user_set.get_range_value(
            LaserFrameRange.name)
        show_error(error)
        print("New frame range: {0} to {1}.".format(laser_frame_range.min,
                                                    laser_frame_range.max))

    def set_laser_fringe_coding_mode(self):
        current_user_set = self.camera.current_user_set()
        error, laser_fringe_coding_mode = current_user_set.get_enum_value_string(
            LaserFringeCodingMode.name)
        print("Old fringe coding mode: {}.".format(laser_fringe_coding_mode))

        # Set the "Fringe Coding Mode" parameter, which controls the pattern of the structured light. The "Fast" mode enhances the
        # capture speed but provides lower depth data accuracy. The "Accurate" mode provides better depth data accuracy but reduces the capture speed.
        error = current_user_set.set_enum_value(
            LaserFringeCodingMode.name, LaserFringeCodingMode.Value_Accurate)
        show_error(error)
        error, laser_fringe_coding_mode = current_user_set.get_enum_value_string(
            LaserFringeCodingMode.name)
        show_error(error)
        print("New fringe coding mode: {}.".format(laser_fringe_coding_mode))

    def set_laser_power_level(self):
        current_user_set = self.camera.current_user_set()
        error, laser_power_level = current_user_set.get_int_value(
            LaserPowerLevel.name)
        show_error(error)
        print("Old power level: {}".format(laser_power_level))

        # Set the "Laser Power" parameter, which is the output power of the projector as a percentage of the maximum output power. This affects the
        # intensity of the projected structured light.
        laser_power_level = 80
        error = current_user_set.set_int_value(
            LaserPowerLevel.name, laser_power_level)
        show_error(error)
        error, laser_power_level = current_user_set.get_int_value(
            LaserPowerLevel.name)
        show_error(error)
        print("New power level: {}".format(laser_power_level))

    def main(self):
        if find_and_connect(self.camera):
            self.set_laser_power_level()
            self.set_laser_fringe_coding_mode()
            self.set_laser_frame_range()
            self.set_laser_partition_count()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = SetParametersOfLaserCameras()
    a.main()
