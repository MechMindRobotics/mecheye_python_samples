# With this sample program, you can obtain and save untextured and textured point clouds (PCL format)
# of the objects in the ROI from a camera.

import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
import open3d as o3d
import numpy as np
from source import Common


class CapturePointCloudROI(object):
    def __init__(self):
        self.device = Device()

    def capture_point_cloud_roi(self):
        Common.show_error(self.device.set_scan_3d_roi(0, 0, 500, 500))

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

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.capture_point_cloud_roi()


if __name__ == '__main__':
    a = CapturePointCloudROI()
    a.main()
