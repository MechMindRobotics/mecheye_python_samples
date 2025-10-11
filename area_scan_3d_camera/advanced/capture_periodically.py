# With this sample, you can obtain and save 2D images, depth maps and point clouds
# periodically for the specified duration from a camera.

import time
import cv2

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *

# Set the camera capture interval to 10 seconds and the total duration of image capturing to 5 minutes.
capture_time = 5  # minutes
capture_period = 10  # seconds


class CapturePeriodically(object):
    def __init__(self):
        self.camera = Camera()

    def capture_timed_and_periodically(self):
        frame_all_2d_3d = Frame2DAnd3D()
        start = time.time()
        capture_count = 0
        # Perform image capturing periodically according to the set interval for the set total duration.
        while time.time() - start < capture_time * 60:
            before = time.time()
            print("Start capturing.")

            status = self.camera.capture_2d_and_3d(frame_all_2d_3d)
            show_error(status)
            if not status.is_ok():
                return
            capture_count = capture_count + 1

            # Save the obtained data with the set filenames.
            color_map = frame_all_2d_3d.frame_2d().get_color_image()
            color_file = "2DImage_" + str(capture_count) + ".png"
            cv2.imwrite(color_file, color_map.data())

            depth_map = frame_all_2d_3d.frame_3d().get_depth_map()
            depth_file = "DepthMap_" + str(capture_count) + ".tiff"
            cv2.imwrite(depth_file, depth_map.data())

            point_cloud_file = "TexturedPointCloud_" + \
                str(capture_count) + ".ply"
            show_error(frame_all_2d_3d.save_textured_point_cloud(
                FileFormat_PLY, point_cloud_file))

            print("Paused capturing.")

            after = time.time()
            time_used = after - before
            if time_used < capture_period:
                time.sleep(capture_period - time_used)
            else:
                print(
                    "The actual capture time is longer than the set capture interval. Please increase the capture interval.")

            time_remaining = int(capture_time * 60 - (time.time() - start))
            print("Remaining time: {0} minutes {1} seconds".format(
                int(time_remaining / 60), time_remaining % 60))

        print("Capturing for {} minutes is completed.".format(capture_time))

    def main(self):
        if find_and_connect(self.camera):
            if not confirm_capture_3d():
                return
            self.capture_timed_and_periodically()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = CapturePeriodically()
    a.main()
