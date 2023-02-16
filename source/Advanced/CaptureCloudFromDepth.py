import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from source import Common
from MechEye import Device
import numpy as np
import open3d as o3d

class CaptureCloudFromDepth(object):
    def __init__(self):
        self.device = Device()

    def capture_cloud_from_depth(self):
        depth = self.device.capture_depth()
        depth_data = depth.data()
        device_intrinsic = self.device.get_device_intrinsic().depth_camera_intrinsic()

        point_cloud_xyz = o3d.geometry.PointCloud()
        points_xyz = np.zeros((depth.width() * depth.height(), 3), dtype=np.float64)

        width = depth.width()
        print("Depth map element size is: {}".format(depth_data.size))
        for i, d in enumerate(depth_data):
            for j, dd in enumerate(d):
                points_xyz[width * i + j][0] = (j - device_intrinsic.camera_matrix_cx()) * dd / device_intrinsic.camera_matrix_fx()
                points_xyz[width * i + j][1] = (i - device_intrinsic.camera_matrix_cy()) * dd / device_intrinsic.camera_matrix_fy()
                points_xyz[width * i + j][2] = dd

        point_cloud_xyz.points = o3d.utility.Vector3dVector(points_xyz)
        o3d.visualization.draw_geometries([point_cloud_xyz])
        o3d.io.write_point_cloud("PointCloudXYZ.ply", point_cloud_xyz)
        print("Point cloud saved to path PointCloudXYZ.ply")

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.capture_cloud_from_depth()


if __name__ == '__main__':
    a = CaptureCloudFromDepth()
    a.main()
