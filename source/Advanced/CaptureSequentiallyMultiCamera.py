import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class CaptureSequentiallyMultiCamera(object):
    def __init__(self):
        self.device = Device()

    def connect_device_info(self):
        for index in self.indices:
            device = Device()
            error_status = device.connect(self.device_list[index])
            if not error_status.ok():
                print(error_status.description())
                quit()

            device_info = device.get_device_info()
            print("Camera {} start capturing.".format(device_info.id))

            device.capture_color()
            device.capture_depth()
            device.capture_point_xyz()
            device.capture_point_xyz_bgr()

            device.disconnect()
            print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        Common.choose_multi_camera(self)
        if len(self.indices) != 0:
            self.connect_device_info()
        else:
            print("No camera was selected.")


if __name__ == '__main__':
    a = CaptureSequentiallyMultiCamera()
    a.main()
