from MechEye import Device
import time
from struct import unpack

capture_time = 5  # minutes
capture_period = 10  # seconds


def to_seconds(minutes):
    return minutes * 60


device = Device()
device_list = device.get_device_list()


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

user_input = input("Please enter the device index you want to connect: ")

error = device.connect(device_list[int(user_input)])
if error.ok():
    print("connect success")
else:
    print(error.description())

start = time.time()

while (time.time() - start < to_seconds(capture_time)):
    before = time.time()

    color = device.capture_color()
    depth = device.capture_depth()
    point_xyz = device.capture_point_xyz()
    point_xyz_rgb = device.capture_point_xyz_bgr()

    after = time.time()
    time_used = after - before
    if (time_used < capture_period):
        time.sleep(capture_period - time_used)
    else:
        print("Your capture time is longer than your capture period. Please increase your capture period.")

    time_remaining = int(to_seconds(capture_time) - (time.time() - start))
    print("Remaining time: {0} minutes {1} seconds".format(
        int(time_remaining / 60), time_remaining % 60))

print("Capturing completed for {} minutes".format(capture_time))

device.disconnect()
