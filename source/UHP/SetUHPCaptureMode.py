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


class SetLaserFrameRange(object):
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

        capture_mode_dic = {0: "Camera1", 1: "Camera2", 2: "Merge"}

        uhp_settings = self.device.get_uhp_capture_mode()
        print("Old capture mode: {}.".format(capture_mode_dic[uhp_settings]))

        show_error(self.device.set_uhp_capture_mode("Camera1"))

        uhp_settings = self.device.get_uhp_capture_mode()
        print("New capture mode: {}.".format(capture_mode_dic[uhp_settings]))

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        self.find_camera_list()
        self.choose_camera()
        self.connect_device_info()


if __name__ == '__main__':
    a = SetLaserFrameRange()
    a.main()
