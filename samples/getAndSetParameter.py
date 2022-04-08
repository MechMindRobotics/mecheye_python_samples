from MechEye import Device


def show_error(status):
    if status.ok():
        return
    print("Error Code : {}".format(status.code()),
          ",Error Description: {}".format(status.description()))


def print_device_info(num, info):
    print(" Mech-Eye device index: {}\n".format(str(num)),
          "Camera Model Name: {}\n".format(info.model()),
          "Camera ID: {}\n".format(info.id()),
          "Camera IP: {}\n".format(info.ip()),
          "Hardware Version: {}\n".format(info.hardware_version()),
          "Firmware Version: {}\n".format(info.firmware_version()),
          "...............................................")


class GetAndSetParameter(object):
    def __init__(self):
        self.device = Device()

    def find_camera_list(self):
        self.device_list = self.device.get_device_list()
        if len(self.device_list) == 0:
            print("No Mech-Eye device found.")
            return
        for i, info in enumerate(self.device_list):
            print_device_info(i, info)

    def choose_camera(self):
        while True:
            self.user_input = input("Please enter the device index you want to connect: ")
            if self.user_input.isdigit() and len(self.device_list) > int(self.user_input):
                break
            print("Input invalid! Please enter the device index you want to connect: ")

    def connect_device_info(self):
        status = self.device.connect(self.device_list[int(self.user_input)])
        if not status.ok():
            show_error(status)
            return -1
        print("Connect Mech-Eye Success.")

        print("All user sets : ", end='')
        user_sets = self.device.get_all_user_sets()
        for user_set in user_sets:
            print(user_set, end=' ')

        current_user_set = self.device.get_current_user_set()
        print("\ncurrent_user_set: " + str(current_user_set))

        show_error(self.device.set3D_exposure([1.0, 32.1, 99.0]))
        exposure_sequence = self.device.get3D_exposure()
        print("\nThe 3D scanning exposure multiplier:{}".format(len(exposure_sequence)))
        for i in exposure_sequence:
            print("3D scanning exposure time : {}".format(i))

        show_error(self.device.set_depth_range(1, 2))
        depth_range = self.device.get_depth_range()
        print("\n3D scanning depth Lower Limit : {} mm,".format(depth_range.get_lower()),
              "depth upper limit : {} mm\n".format(depth_range.get_upper()))

        self.device.set_3D_roi(20, 20, 1000, 1000)
        scan_3d_roi = self.device.get3D_roi()
        print("3D scanning ROI topLeftX: {},".format(scan_3d_roi.get_x()),
              "topLeftY: {},".format(scan_3d_roi.get_y()),
              "width: {},".format(scan_3d_roi.get_width()),
              "height: {}\n".format(scan_3d_roi.get_height()))

        show_error(self.device.set2D_exposure_mode("Auto"))
        show_error(self.device.set2D_exposure_time(999.0))
        exposure_mode_2d = self.device.get2D_exposure_mode()
        scan_2d_exposure_time = self.device.get2D_exposure_time()
        print("2D scanning exposure mode enum :{}, ".format(exposure_mode_2d),
              "exposure time: {}\n".format(scan_2d_exposure_time))

        show_error(self.device.set_cloud_smooth_mode("Off"))
        self.device.set_cloud_outlier_filter_mode("Off")
        cloud_smooth_mode = self.device.get_cloud_smooth_mode()
        cloud_outlier_filter_mode = self.device.get_cloud_outlier_filter_mode()
        print("Cloud smooth mode enum :{},".format(cloud_smooth_mode),
              "cloud outlier filter mode enum :{}".format(cloud_outlier_filter_mode))

        show_error(self.device.add_user_set("iii"))
        show_error(self.device.delete_user_set('iii'))

        # Parameter of laser camera, please comment out when connecting non-laser camera.
        show_error(self.device.set_laser_settings("High", 2, 50, 4, 30))
        laser_settings = self.device.get_laser_settings()
        print("\nlaser_mode: {}, range_start:{}, range_end:{}, partition_count:{}, power_level:{}".
              format(laser_settings.get_mode(), laser_settings.get_start(), laser_settings.get_end(),
                     laser_settings.get_count(), laser_settings.get_level()))

        self.device.save_all_settings_to_user_set()

    def main(self):
        self.find_camera_list()
        self.choose_camera()
        self.connect_device_info()


if __name__ == '__main__':
    a = GetAndSetParameter()
    a.main()
