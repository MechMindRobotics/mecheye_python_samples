import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
import time
from MechEye import Device
from source import Common

capture_time = 5  # minutes
capture_period = 10  # seconds


class CaptureTimedAndPeriodically(object):
    def __init__(self):
        self.device = Device()

    def connect_device_and_capture(self):
        start = time.time()
        while (time.time() - start < Common.to_seconds(capture_time)):
            before = time.time()
            print("Start capturing.")

            self.device.capture_color()
            self.device.capture_depth()
            self.device.capture_point_xyz()
            self.device.capture_point_xyz_bgr()

            print("Paused capturing.")

            after = time.time()
            time_used = after - before
            if time_used < capture_period:
                time.sleep(capture_period - time_used)
            else:
                print(
                    "Your capture time is longer than your capture period. Please increase your capture period.")

            time_remaining = int(Common.to_seconds(
                capture_time) - (time.time() - start))
            print("Remaining time: {0} minutes {1} seconds".format(
                int(time_remaining / 60), time_remaining % 60))

        print("Capturing completed for {} minutes".format(capture_time))

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.connect_device_and_capture()


if __name__ == '__main__':
    a = CaptureTimedAndPeriodically()
    a.main()
