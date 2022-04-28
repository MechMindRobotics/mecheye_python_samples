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


def print_dist_coeffs(name, coeffs):
    print("{}: k1: {},k2: {},p1: {},p2: {},k3: {}".
          format(name, coeffs.dist_coeffs_k1(), coeffs.dist_coeffs_k2(),
                 coeffs.dist_coeffs_p1(), coeffs.dist_coeffs_p2(), coeffs.dist_coeffs_k3()))


def print_matrix(name, matrix):
    print("name: {}\n[{},{}\n{},{}]".format(name, matrix.camera_matrix_fx(), matrix.camera_matrix_fy(),
                                            matrix.camera_matrix_cx(), matrix.camera_matrix_cy()))


class GetCameraIntri(object):
    def __init__(self):
        self.device = Device()

    def find_camera_list(self):
        print("Find Mech-Eye device...")
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
            if user_input.isdigit() and len(self.device_list) > int(user_input) and int(user_input) > 0:
                self.index = int(user_input)
                break
            print("Input invalid! Please enter the device index you want to connect: ")

    def connect_device_info(self):
        status = self.device.connect(self.device_list[self.index])
        if not status.ok():
            show_error(status)
            quit()
        print("Connect Mech-Eye Success.")

        device_intrinsic = self.device.get_device_intrinsic()
        print_dist_coeffs("CameraDistCoeffs", device_intrinsic)
        print_matrix("CameraMatrix", device_intrinsic)

        self.device.disconnect()

    def main(self):
        self.find_camera_list()
        self.choose_camera()
        self.connect_device_info()


if __name__ == '__main__':
    a = GetCameraIntri()
    a.main()
