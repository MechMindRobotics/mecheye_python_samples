import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
import open3d as o3d
import numpy as np
from source import Common


class CapturePointCloud(object):
    def __init__(self):
        self.device = Device()

    def connect_device_info(self):
        color = self.device.capture_color()
        color_data = color.data()
        point_xyz = self.device.capture_point_xyz()
        point_xyz_data = point_xyz.data()

        point_cloud_xyz = o3d.geometry.PointCloud()
        points_xyz = point_xyz_data.reshape(-1, 3) * 0.001

        point_cloud_xyz.points = o3d.utility.Vector3dVector(points_xyz)
        o3d.visualization.draw_geometries([point_cloud_xyz])
        o3d.io.write_point_cloud("PointCloudXYZ.ply", point_cloud_xyz)
        print("Point cloud saved to path PointCloudXYZ.ply")

        point_cloud_xyz_rgb = o3d.geometry.PointCloud()
        point_cloud_xyz_rgb.points = o3d.utility.Vector3dVector(points_xyz)

        points_rgb = color_data.reshape(-1, 3)[:, ::-1]/255

        point_cloud_xyz_rgb.colors = o3d.utility.Vector3dVector(points_rgb)
        o3d.visualization.draw_geometries([point_cloud_xyz_rgb])
        o3d.io.write_point_cloud("PointCloudXYZRGB.ply", point_cloud_xyz_rgb)
        print("Color point cloud saved to path PointCloudXYZRGB.ply")

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.connect_device_info()


if __name__ == '__main__':
    a = CapturePointCloud()
    a.main()
