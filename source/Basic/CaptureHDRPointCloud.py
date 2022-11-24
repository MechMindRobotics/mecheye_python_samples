import time

from MechEye import Device
import open3d as o3d
import numpy as np


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


class CaptureHDRPointCloud(object):
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

        show_error(self.device.set_scan_3d_exposure([5.0, 10.0]))
        start = time.time()
        xyz_bgr = self.device.capture_point_xyz_bgr()
        date = np.array(xyz_bgr.data())
        point_xyz_data = np.array(date.tolist())[:, :, 3:6]

        point_cloud_xyz = o3d.geometry.PointCloud()
        points_xyz = point_xyz_data.reshape(-1, 3) * 0.001

        point_cloud_xyz.points = o3d.utility.Vector3dVector(points_xyz)
        end = time.time()
        print(end - start)

        o3d.visualization.draw_geometries([point_cloud_xyz])
        o3d.io.write_point_cloud("PointCloudXYZ.ply", point_cloud_xyz)
        print("Point cloud saved to path PointCloudXYZ.ply")

        color_data = np.array(date.tolist())[:, :, :3]

        point_cloud_xyz_rgb = o3d.geometry.PointCloud()
        point_cloud_xyz_rgb.points = o3d.utility.Vector3dVector(points_xyz)
        points_rgb = color_data.reshape(-1, 3) / 255

        point_cloud_xyz_rgb.colors = o3d.utility.Vector3dVector(points_rgb)
        o3d.visualization.draw_geometries([point_cloud_xyz_rgb])
        o3d.io.write_point_cloud("PointCloudXYZRGB.ply", point_cloud_xyz_rgb)
        print("Color point cloud saved to path PointCloudXYZRGB.ply")

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        self.find_camera_list()
        self.choose_camera()
        self.connect_device_info()


if __name__ == '__main__':
    a = CaptureHDRPointCloud()
    a.main()
