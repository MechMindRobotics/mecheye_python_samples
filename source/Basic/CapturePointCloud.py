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

    def capture_point_cloud(self):
        points_xyz = self.device.capture_point_xyz()
        points_xyz_data = points_xyz.data()
        points_xyz_o3d = o3d.geometry.PointCloud()
        points_xyz_o3d.points = o3d.utility.Vector3dVector(points_xyz_data.reshape(-1, 3) * 0.001)

        o3d.visualization.draw_geometries([points_xyz_o3d])
        o3d.io.write_point_cloud("PointCloudXYZ.ply", points_xyz_o3d)
        print("Point cloud saved to path PointCloudXYZ.ply")

    def capture_color_point_cloud(self):
        points_xyz_bgr = self.device.capture_point_xyz_bgr()
        points_xyz_bgr_data = points_xyz_bgr.data()
        points_xyz_bgr_data_array = np.array(points_xyz_bgr_data.reshape(-1,1)[:, 0].tolist())
        points_xyz_rgb_points = points_xyz_bgr_data_array.reshape(-1, 6)[:, :3] * 0.001
        point_xyz_rgb_colors = points_xyz_bgr_data_array.reshape(-1, 6)[:, 3:6] [:, ::-1] / 255
        points_xyz_rgb_o3d = o3d.geometry.PointCloud()
        points_xyz_rgb_o3d.points = o3d.utility.Vector3dVector(points_xyz_rgb_points)
        points_xyz_rgb_o3d.colors = o3d.utility.Vector3dVector(point_xyz_rgb_colors)

        o3d.visualization.draw_geometries([points_xyz_rgb_o3d])
        o3d.io.write_point_cloud("PointCloudXYZRGB.ply", points_xyz_rgb_o3d)
        print("Color point cloud saved to path PointCloudXYZRGB.ply")

        

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.capture_point_cloud()
            self.capture_color_point_cloud()
            self.device.disconnect()
            print("Disconnected from the Mech-Eye device successfully.")


if __name__ == '__main__':
    a = CapturePointCloud()
    a.main()
