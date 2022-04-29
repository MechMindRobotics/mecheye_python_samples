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


class CaptureSequentiallyMultiCamera(object):
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
        self.indices = set()
        while True:
            user_input = input(
                "Please enter the device index you want to connect. Enter a c to terminate adding devices: ")
            if user_input == "c":
                break
            elif user_input.isdigit() and len(self.device_list) > int(user_input) and int(user_input) >= 0:
                self.indices.add(int(user_input))
            else:
                print("Input invalid!")

    def connect_device_info(self):
        for index in self.indices:
            device = Device()
            error_status = device.connect(self.device_list[index])
            if (not error_status.ok()):
                print(error_status.description())
                quit()

            device_info = device.get_device_info()
            print("Camera {} start capturing.".format(device_info.id()))

            color = device.capture_color()
            depth = device.capture_depth()
            point_xyz = device.capture_point_xyz()
            point_xyz_rgb = device.capture_point_xyz_bgr()

            device.disconnect()
            print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        self.find_camera_list()
        self.choose_camera()
        self.connect_device_info()


if __name__ == '__main__':
    a = CaptureSequentiallyMultiCamera()
    a.main()
