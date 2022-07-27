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


class CaptureCloudFromDepth(object):
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

        color = self.device.capture_color()
        color_data = color.data()
        depth = self.device.capture_depth()
        depth_data = depth.data()
        device_intrinsic = self.device.get_device_intrinsic().depth_camera_intrinsic()

        point_cloud_xyz = o3d.geometry.PointCloud()
        points_xyz = np.zeros(
            (depth.width() * depth.height(), 3), dtype=np.float64)

        width = depth.width()
        for i, d in enumerate(depth_data):
            for j, dd in enumerate(d):
                points_xyz[width * i + j][0] = (j - device_intrinsic.camera_matrix_cx()
                                                ) * dd / device_intrinsic.camera_matrix_fx()
                points_xyz[width * i + j][1] = (i - device_intrinsic.camera_matrix_cy()
                                                ) * dd / device_intrinsic.camera_matrix_fy()
                points_xyz[width * i + j][2] = dd

        point_cloud_xyz.points = o3d.utility.Vector3dVector(points_xyz)
        o3d.visualization.draw_geometries([point_cloud_xyz])
        o3d.io.write_point_cloud("PointCloudXYZ.ply", point_cloud_xyz)
        print("Point cloud saved to path PointCloudXYZ.ply")

        point_cloud_xyz_rgb = o3d.geometry.PointCloud()
        point_cloud_xyz_rgb.points = o3d.utility.Vector3dVector(points_xyz)
        points_rgb = np.zeros(
            (depth.width() * depth.height(), 3), dtype=np.float64)

        pos = 0
        for dd in np.nditer(color_data):
            points_rgb[int(pos / 3)][int(2 - (pos % 3))] = dd / 255
            pos = pos + 1

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
    a = CaptureCloudFromDepth()
    a.main()
