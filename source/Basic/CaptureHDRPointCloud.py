from MechEye import Device
import open3d as o3d
import numpy as np
from struct import unpack

device = Device()
device_list = device.get_device_list()


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

user_input = input("Please enter the device index you want to connect: ")

show_error(device.connect(device_list[int(user_input)]))
show_error(device.set3D_exposure([5.0, 10.0]))


color = device.capture_color()
color_data = color.data()
point_xyz = device.capture_point_xyz()
point_xyz_data = point_xyz.data()

point_cloud_xyz = o3d.geometry.PointCloud()
points_xyz = np.zeros(
    (point_xyz.width() * point_xyz.height(), 3), dtype=np.float64)

for i, d in enumerate(point_xyz_data):
    for j, dd in enumerate(d):
        points_xyz[point_xyz.width() * i + j][0] = 0.001 * dd[0]
        points_xyz[point_xyz.width() * i + j][1] = 0.001 * dd[1]
        points_xyz[point_xyz.width() * i + j][2] = 0.001 * dd[2]

point_cloud_xyz.points = o3d.utility.Vector3dVector(points_xyz)
o3d.visualization.draw_geometries([point_cloud_xyz])
o3d.io.write_point_cloud("PointCloudXYZ.ply", point_cloud_xyz)
print("Point cloud saved to path PointCloudXYZ.ply")

point_cloud_xyz_rgb = o3d.geometry.PointCloud()
point_cloud_xyz_rgb.points = o3d.utility.Vector3dVector(points_xyz)
points_rgb = np.zeros(
    (point_xyz.width() * point_xyz.height(), 3), dtype=np.float64)

for i, d in enumerate(color_data):
    for j, dd in enumerate(d):
        points_rgb[point_xyz.width() * i + j][0] = dd[2] / 255
        points_rgb[point_xyz.width() * i + j][1] = dd[1] / 255
        points_rgb[point_xyz.width() * i + j][2] = dd[0] / 255

point_cloud_xyz_rgb.colors = o3d.utility.Vector3dVector(points_rgb)
o3d.visualization.draw_geometries([point_cloud_xyz_rgb])
o3d.io.write_point_cloud("PointCloudXYZRGB.ply", point_cloud_xyz_rgb)
print("Color point cloud saved to path PointCloudXYZRGB.ply")

device.disconnect()
