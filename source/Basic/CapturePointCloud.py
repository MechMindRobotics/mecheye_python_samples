from MechEye import Device
import open3d as o3d
import numpy as np
from struct import unpack


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


class CapturePointCloud(object):
    def __init__(self):
        self.device = Device()

    def find_camera_list(self):
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

        color = self.device.capture_color()
        color_data = color.data()
        point_xyz = self.device.capture_point_xyz()
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

        self.device.disconnect()

    def main(self):
        print("Find Mech-Eye device...")
        self.find_camera_list()
        self.choose_camera()
        self.connect_device_info()


if __name__ == '__main__':
    a = CapturePointCloud()
    a.main()
