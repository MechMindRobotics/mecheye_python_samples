# With this sample, you can generate a point cloud from the depth map and save the point cloud.

import numpy as np

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *


class ConvertDepthMapToPointCloud(object):
    def __init__(self):
        self.camera = Camera()

    def convert_depth_map_to_point_cloud(self, depth: DepthMap, intrinsics: CameraIntrinsics, xyz: UntexturedPointCloud):
        xyz.resize(depth.width(), depth.height())

        for i in range(depth.width() * depth.height()):
            row = int(i / depth.width())
            col = int(i - row * depth.width())
            xyz[i].z = depth[i].z
            xyz[i].x = float((col - intrinsics.depth.camera_matrix.cx)
                             * depth[i].z / intrinsics.depth.camera_matrix.fx)
            xyz[i].y = float((row - intrinsics.depth.camera_matrix.cy)
                             * depth[i].z / intrinsics.depth.camera_matrix.fy)

    def capture_cloud_from_depth(self):

        camera_info = CameraInfo()
        show_error(self.camera.get_camera_info(camera_info))
        print_camera_info(camera_info)

        if not confirm_capture_3d():
            return

        frame3d = Frame3D()
        show_error(self.camera.capture_3d(frame3d))
        depth = frame3d.get_depth_map()
        intrinsics = CameraIntrinsics()
        show_error(self.camera.get_camera_intrinsics(intrinsics))

        point_cloud = UntexturedPointCloud()
        self.convert_depth_map_to_point_cloud(depth, intrinsics, point_cloud)
        point_cloud_file = "UntexturedPointCloud.ply"
        Frame3D.save_point_cloud(point_cloud, FileFormat_PLY, point_cloud_file)

        print("The point cloud contains:", point_cloud.width()
              * point_cloud.height(), "data points.")
        print("Save the point cloud to file:", point_cloud_file)

    def main(self):
        if find_and_connect(self.camera):
            self.capture_cloud_from_depth()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = ConvertDepthMapToPointCloud()
    a.main()
