# With this sample program, you can set the range of depth values to be retained by a camera.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect


class SetDepthRange(object):
    def __init__(self):
        self.camera = Camera()

    def set_depth_range(self):
        user_set = self.camera.current_user_set()
        # Set the range of depth values to 100–1000 mm.
        depth_range = RangeInt(100, 1000)
        success_message = "\n3D scanning depth lower limit : {} mm,".format(depth_range.min) + " depth upper limit : {} mm\n".format(depth_range.max)
        show_error(user_set.set_range_value(
            Scanning3DDepthRange.name, depth_range), success_message)

    def main(self):
        if find_and_connect(self.camera):
            self.set_depth_range()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = SetDepthRange()
    a.main()
