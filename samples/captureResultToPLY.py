from MechEye import Device
import sys
import cv2
import pcl
import numpy as np
import open3d
import ctypes
from struct import unpack
import json
from pcl import pcl_visualization

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


colo = device.capture_color()
color_data = colo.data()
point_xyz = device.capture_point_xyz()
point_xyz_data = point_xyz.data()

point_cloud_xyz = pcl.PointCloud()
points_xyz = np.zeros((point_xyz.width() * point_xyz.height(), 3), dtype=np.float32)

for i, d in enumerate(point_xyz_data):
    for j,dd in enumerate(d):
        points_xyz[point_xyz.width() * i + j][0] = 0.001 * dd[0]
        points_xyz[point_xyz.width() * i + j][1] = 0.001 * dd[1]
        points_xyz[point_xyz.width() * i + j][2] = 0.001 * dd[2]

point_cloud_xyz.from_array(points_xyz)
pcl.save(point_cloud_xyz,"pointCloudXYZ.ply")

point_cloud_xyz_rgb = pcl.PointCloud_PointXYZRGB()
points_xyz_rgb = np.zeros((point_xyz.width() * point_xyz.height(), 4), dtype=np.float32)

for i, d in enumerate(point_xyz_data):
    for j,dd in enumerate(d):
        points_xyz_rgb[point_xyz.width() * i + j][0] = 0.001 * dd[0]
        points_xyz_rgb[point_xyz.width() * i + j][1] = 0.001 * dd[1]
        points_xyz_rgb[point_xyz.width() * i + j][2] = 0.001 * dd[2]

for i, d in enumerate(color_data):
    for j,dd in enumerate(d):
        points_xyz_rgb[point_xyz.width() * i + j][3] = dd[0] | dd[1] | dd[2]


point_cloud_xyz_rgb.from_array(points_xyz_rgb)
pcl.save(point_cloud_xyz_rgb,"pointCloudXYZRGB.ply")

device.disconnect()