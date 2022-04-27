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


class ConnectAndCaptureImage(object):
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

        device_intrinsic = self.device.get_device_intrinsic()
        print_dist_coeffs("CameraDistCoeffs", device_intrinsic)
        print_matrix("CameraMatrix", device_intrinsic)

        row, col = 222, 222
        color_map = self.device.capture_color()
        print("Color map size is width: {}, ".format(color_map.width()),
              "height: {}".format(color_map.height()))
        color_data = color_map.data()
        RGB = [color_data[int(row)][int(col)][i] for i in range(3)]
        print("Color map element at ({},{}) is R:{},G:{},B{}\n".
              format(row, col, RGB[0], RGB[1], RGB[2]))

        depth_map = self.device.capture_depth()
        print("Depth map size is width: {}, ".format(depth_map.width()),
              "height: {}".format(depth_map.height()))
        print("Depth map element at ({},{}) is depth :{}mm\n".
              format(row, col, depth_map.data()[int(row)][int(col)]))

        point_xyz_map = self.device.capture_point_xyz()
        print("PointXYZ map size is width: {}, ".format(point_xyz_map.width()),
              "height: {}".format(point_xyz_map.height()))
        point_xyz_data = point_xyz_map.data()
        print("PointXYZ map element at ({},{}) is X: {}mm , Y: {}mm, Z: {}mm\n".
              format(row, col, point_xyz_data[int(row)][int(col)][0],
                     point_xyz_data[int(row)][int(col)][1],
                     point_xyz_data[int(row)][int(col)][2]))

    def main(self):
        self.find_camera_list()
        self.choose_camera()
        self.connect_device_info()


if __name__ == '__main__':
    a = ConnectAndCaptureImage()
    a.main()
