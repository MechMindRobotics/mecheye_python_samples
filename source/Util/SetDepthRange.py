import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class SetDepthRange(object):
    def __init__(self):
        self.device = Device()

    def connect_device_info(self):
        Common.show_error(self.device.set_depth_range(4, 888))
        depth_range = self.device.get_depth_range()
        print("\n3D scanning depth Lower Limit : {} mm,".format(depth_range.lower()),
              "depth upper limit : {} mm\n".format(depth_range.upper()))

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.connect_device_info()


if __name__ == '__main__':
    a = SetDepthRange()
    a.main()
