

def show_error(status):
    if status.ok():
        return
    print("Error Code : {}".format(status.code()),
          ",Error Description: {}".format(status.description()))


def print_device_info(info):
    print("Camera Model Name: {}\n"
          "Camera ID: {}\n"
          "Camera IP: {}\n"
          "Hardware Version: {}\n"
          "Firmware Version: {}\n".format(info.model,
                                          info.id,
                                          info.ip,
                                          info.hardware_version,
                                          info.firmware_version,
                                         )
          )


def print_dist_coeffs(name, coeffs):
    print("{}: k1: {}, k2: {}, p1: {}, p2: {}, k3: {}".
          format(name,
                 coeffs.dist_coeffs_k1(),
                 coeffs.dist_coeffs_k2(),
                 coeffs.dist_coeffs_p1(),
                 coeffs.dist_coeffs_p2(),
                 coeffs.dist_coeffs_k3())
          )


def print_matrix(name, matrix):
    print("name: {}\n[{}, {}\n{}, {}]".format(name,
                                              matrix.camera_matrix_fx(),
                                              matrix.camera_matrix_fy(),
                                              matrix.camera_matrix_cx(),
                                              matrix.camera_matrix_cy())
          )


def to_seconds(minutes):
    return minutes * 60


def find_camera_list(classname):
    print("Find Mech-Eye devices...")
    classname.device_list = classname.device.get_device_list()
    if len(classname.device_list) == 0:
        print("No Mech-Eye device found.")
        quit()
    else:
        for i, info in enumerate(classname.device_list):
            print("Mech-Eye device index: {}\n{}".format(i, "." * 40))
            print_device_info(info)


def choose_camera_and_connect(classname):
    while True:
        user_input = input("Please enter the device index you want to connect: ")
        if user_input.isdigit() and 0 <= int(user_input) < len(classname.device_list):
            index = int(user_input)
            break
        print("Input invalid! ", end="")

    status = classname.device.connect(classname.device_list[index])
    if not status.ok():
        show_error(status)
        return False
    print("Connect Mech-Eye Successfully.")
    return True


def choose_multi_camera(classname):
    classname.indices = set()
    while True:
        user_input = input(
            "Please enter the device index you want to connect. Enter a c to terminate adding devices: ")
        if user_input == "c":
            break
        elif user_input.isdigit() and 0 <= int(user_input) < len(classname.device_list):
            classname.indices.add(int(user_input))
        else:
            print("Input invalid!")