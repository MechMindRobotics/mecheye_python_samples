from MechEye import Device
import cv2


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


class CaptureDepthMap(object):
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
            self.user_input = input(
                "Please enter the device index you want to connect: ")
            if self.user_input.isdigit() and len(self.device_list) > int(self.user_input):
                break
            print("Input invalid! Please enter the device index you want to connect: ")

    def connect_device_info(self):
        status = self.device.connect(self.device_list[int(self.user_input)])
        if not status.ok():
            show_error(status)
            return -1
        print("Connect Mech-Eye Success.")

        depth_map = self.device.capture_depth()
        depth_file = "DepthMap.png"
        cv2.imwrite(depth_file, depth_map.data())
        print("Capture and save depth image : {}".format(depth_file))

    def main(self):
        self.find_camera_list()
        self.choose_camera()
        self.connect_device_info()


if __name__ == '__main__':
    a = CaptureDepthMap()
    a.main()
