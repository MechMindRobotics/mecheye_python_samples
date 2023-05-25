# With this sample program, you can construct and save untextured and textured point clouds (PCL
# format) generated from a depth map and masked 2D image.

import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from MechEye.color import Color
import open3d as o3d
import numpy as np
from source import Common

class CapturePointCloudFromTextureMask(object):
    def __init__(self):
        self.device = Device()

    def contains(self, row ,col, roi):
        return row >= roi[1] and row <= roi[1] + roi[3] and col >= roi[0] and col <= roi[0] + roi[2]

    def generate_texture_mask(self, color, roi1, roi2):
        color_data = color.data()

        for row, complex in enumerate(color_data):
            for col, RGB in enumerate(complex):
                if not self.contains(row, col, roi1) and not self.contains(row, col, roi2):
                    color_data[row, col, 0] = 0
                    color_data[row, col, 1] = 0
                    color_data[row, col, 2] = 0
                else:
                    color_data[row, col, 0] = 1
                    color_data[row, col, 1] = 1
                    color_data[row, col, 2] = 1
                

        color_mask = Color(color.from_numpy(color_data))
        return color_mask


    def capture_point_cloud_from_texture_mask(self):

        # capture frame
        color = self.device.capture_color()
        depth = self.device.capture_depth()
        device_intrinsic = self.device.get_device_intrinsic()

        # geneter texture mask
        roi1 = (color.width()/5, color.height()/5, color.width() / 2, color.height() / 2)
        roi2 = (color.width() * 2 / 5, color.height() * 2 / 5, color.width() / 2, color.height() / 2)
        color_mask = self.generate_texture_mask(color, roi1, roi2)

        #generate point cloud
        points_xyz = self.device.get_cloud_from_texture_mask(depth.impl(), color_mask.impl(), device_intrinsic.impl())
        points_xyz_data = points_xyz.data()
        points_xyz_o3d = o3d.geometry.PointCloud()
        points_xyz_o3d.points = o3d.utility.Vector3dVector(points_xyz_data.reshape(-1, 3) * 0.001)
        o3d.visualization.draw_geometries([points_xyz_o3d])
        o3d.io.write_point_cloud("PointCloudXYZ.ply", points_xyz_o3d)
        print("Point cloud saved to path PointCloudXYZ.ply")

        #generate colored point cloud
        points_xyz_bgr = self.device.get_bgr_cloud_from_texture_mask(depth.impl(), color_mask.impl(), color.impl(), device_intrinsic.impl())
        points_xyz_bgr_data = points_xyz_bgr.data()
    
        points_xyz_rgb_points = points_xyz_bgr_data.reshape(-1, 6)[:, :3] * 0.001
        point_xyz_rgb_colors = points_xyz_bgr_data.reshape(-1, 6)[:, 3:6] [:, ::-1] / 255
        points_xyz_rgb_o3d = o3d.geometry.PointCloud()
        points_xyz_rgb_o3d.points = o3d.utility.Vector3dVector(points_xyz_rgb_points.astype(np.float64))
        points_xyz_rgb_o3d.colors = o3d.utility.Vector3dVector(point_xyz_rgb_colors.astype(np.float64))
        o3d.visualization.draw_geometries([points_xyz_rgb_o3d])
        o3d.io.write_point_cloud("PointCloudXYZRGB.ply", points_xyz_rgb_o3d)
        print("Color point cloud saved to path PointCloudXYZRGB.ply")

        # disconnect
        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.capture_point_cloud_from_texture_mask()


if __name__ == '__main__':
    a = CapturePointCloudFromTextureMask()
    a.main()
