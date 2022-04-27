from MechEye import Device
from struct import unpack
import threading


class CaptureThread (threading.Thread):
    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device

    def run(self):
        device_info = device.get_device_info()
        print("Camera {} start capturing.".format(device_info.id()))
        color = device.capture_color()
        depth = device.capture_depth()
        point_xyz = device.capture_point_xyz()
        point_xyz_rgb = device.capture_point_xyz_bgr()
        device.disconnect()


first_device = Device()
device_list = first_device.get_device_list()


def show_error(status):
    if status.ok():
        return
    print("Error Code : {}".format(status.code()),
          ",Error Description: {}".format(status.description()))


def print_device_info(info):
    print("Camera Model Name: " + info.model())
    print("Camera ID: " + info.id())
    print("Camera IP: " + info.ip())
    print("Hardware Version: " + info.hardware_version())
    print("Firmware Version: " + info.firmware_version())
    print(" ")


for i, info in enumerate(device_list):
    print("Mech-Eye device index : " + str(i))
    print_device_info(info)

indices = set()
while (True):
    user_input = input(
        "Please enter the device index you want to connect. Enter a c to terminate adding devices: ")
    if (user_input == "c"):
        break
    elif (int(user_input) > 0 and int(user_input) < len(device_list)):
        indices.add(int(user_input))
    else:
        print("Invalid input!")

devices = []
for index in indices:
    device = Device()
    error_status = device.connect(device_list[index])
    if (not error_status.ok()):
        print(error_status.description())
        quit()
    devices.append(device)

for device in devices:
    capture_thread = CaptureThread(device)
    capture_thread.start()
