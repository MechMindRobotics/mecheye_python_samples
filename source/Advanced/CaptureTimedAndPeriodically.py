from MechEye import Device
import time

capture_time = 5  # minutes
capture_period = 10  # seconds


def to_seconds(minutes):
    return minutes * 60


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


class CaptureTimedAndPeriodically(object):
    def __init__(self):
        self.device = Device()

    def find_camera_list(self):
        print("Find Mech-Eye devices...")
        self.device_list = self.device.get_device_list()
        if len(self.device_list) == 0:
            print("No Mech-Eye device found.")
            quit()
        for i, info in enumerate(self.device_list):
            print_device_info(i, info)

    def choose_camera(self):
        while True:
            user_input = input(
                "Please enter the device index you want to connect: ")
            if user_input.isdigit() and len(self.device_list) > int(user_input) and int(user_input) >= 0:
                self.index = int(user_input)
                break
            print("Input invalid!")

    def connect_device_info(self):
        status = self.device.connect(self.device_list[self.index])
        if not status.ok():
            show_error(status)
            quit()
        print("Connected to the Mech-Eye device successfully.")

        start = time.time()

        while (time.time() - start < to_seconds(capture_time)):
            before = time.time()
            print("Start capturing.")

            color = self.device.capture_color()
            depth = self.device.capture_depth()
            point_xyz = self.device.capture_point_xyz()
            point_xyz_rgb = self.device.capture_point_xyz_bgr()

            print("paused capturing.")

            after = time.time()
            time_used = after - before
            if (time_used < capture_period):
                time.sleep(capture_period - time_used)
            else:
                print(
                    "Your capture time is longer than your capture period. Please increase your capture period.")

            time_remaining = int(to_seconds(
                capture_time) - (time.time() - start))
            print("Remaining time: {0} minutes {1} seconds".format(
                int(time_remaining / 60), time_remaining % 60))

        print("Capturing completed for {} minutes".format(capture_time))

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        self.find_camera_list()
        self.choose_camera()
        self.connect_device_info()


if __name__ == '__main__':
    a = CaptureTimedAndPeriodically()
    a.main()
